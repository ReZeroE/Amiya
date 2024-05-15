import os
import time
import copy
from datetime import datetime
from pynput import keyboard
from amiya.automation_handler.automation_config_handler import SequenceConfigHandler
from amiya.automation_handler.units.action import Action, MouseAction, KeyboardAction
from amiya.exceptions.exceptions import AmiyaBaseException, Amiya_AppNotFocusedException
from amiya.utils.constants import FORCE_ACTIONS_DELAY, VERSION
from amiya.utils.helper import *
from amiya.apps_manager.safety_monitor import SafetyMonitor
from amiya.pixel_calculator.resolution_detector import ResolutionDetector
from amiya.pixel_calculator.pixel_calculator import PixelCalculator

class AutomationSequence:
    def __init__(
        self,
        sequence_name: str
    ):
        self.sequence_name                  = sequence_name                 # Default to None (populated during some __init__() and parse_json())
        self.date_created: datetime         = None                          # Default to None (and set at to_json() and parse_json())
        self.primary_monitor_info: dict     = None                          # Fetch PRIMARY monitor's size (width x height)
        self.other_data                     = None
        self.actions: list[Action]          = []
        
        self.global_delay                   = 0
    
    
    def __progress_bar(self, actions: list[Action], prefix="", size=40, out=sys.stdout):
        count = len(actions)
        start = time.time() # time estimate start
        total_time = self.get_runtime()
        
        
        def show(j, delay, remaining_time_str):
            x = int(size*j/count)   
            aprint(f"{prefix}|{u'█'*x}{(' '*(size-x))}| {int(j)}/{count}  -  Remaining: {remaining_time_str}", end='\r', file=out, flush=True) 
        
        def secs_to_str(secs):
            mins, sec = divmod(secs, 60)
            time_str = f"{int(mins)} mins {round(sec, 2)} secs"
            return time_str
        
        show(0.1, delay=actions[0].delay, remaining_time_str=secs_to_str(total_time)) # avoid div/0 
        for i, action in enumerate(actions):
            yield action
            
            total_time -= action.delay
            show(i+1, action.delay, secs_to_str(total_time))
            
        print("", flush=True, file=out)
    
    
    def execute(self, safety_monitor: SafetyMonitor):
        
        def verbose_action(idx: int, action: Action):
            buffer_space = " "*5                                # Verbose current action
            aprint(f"(CMD {idx+1}/{len(self.actions)}) Executing: {action.__repr__()}{buffer_space}", end="\r")
        
        def verbose_warning():
            # Verbose warning if the current action isn't suited for the pixel calculator developed in ver0.0.2+
            for action in self.actions:
                if isinstance(action, MouseAction) and action.is_valid_for_pixel_calc == False:
                    aprint(f"This automation sequence is not available for pixel calculator in version {VERSION}.")
                    return
        

        # Becuase the pixel calculator will directory modify the MouseAction's coordinates, we need a way to reset the 
        # sequence's coordinates after the sequence finishes running. Therefore, we first make a copy of the sequence
        # before it is modified by the pixel calculator and then replace the modified sequence at the end.
        actions_copy = copy.deepcopy(self.actions)
        
        verbose_warning()
        pynput_keyboard = keyboard.Controller()
        
        # for idx, action in enumerate(self.__progress_bar(self.actions, f"Running: ", 40)):
            
        for idx, action in enumerate(self.actions):
            verbose_action(idx, action)
            
            time.sleep(FORCE_ACTIONS_DELAY)
            time.sleep(action.delay)                            # Execute current action after standard action delay
            time.sleep(self.global_delay)                       # Execute current action after global delay
            
            safety_monitor.app_is_focused()                     # If the application is no longer focused, stop the automation
            
            # ====================================
            # ===========| KEYBOARD | ============
            # ====================================
            if isinstance(action, KeyboardAction):
                action.execute(pynput_keyboard)
                

            # ==================================
            # ============| MOUSE | ============
            # ==================================
            elif isinstance(action, MouseAction):
                
                if action.is_valid_for_pixel_calc == True:
                    new_coord = PixelCalculator.transform_coordinate(action.coordinate, action.window_info)
                    action.coordinate = new_coord
                
                action.execute()
            
        # Reset the modified version of the sequence (modified by the pixel calculator)
        self.actions = actions_copy

            
    def add(self, action: Action):
        assert(isinstance(action, Action))
        self.actions.append(action)

    def to_json(self):
        json_data = dict()
        json_data["metadata"] = {
            "sequence_name" : self.sequence_name,
            "date_created"  : DatetimeHandler.datetime_to_str(self.date_created),
            "monitor_info"  : ResolutionDetector.get_primary_monitor_size(),
            "other_data"    : self.other_data
        }
        json_data["actions_sequence"] = [action.to_json() for action in self.actions]
        return json_data

    @staticmethod
    def parse_config(raw_json_config: list):
        metadata        = raw_json_config["metadata"]
        sequence_name   = metadata["sequence_name"]
        
        sequence = AutomationSequence(sequence_name)
        
        sequence.date_created           = DatetimeHandler.str_to_datetime(metadata["date_created"])
        sequence.primary_monitor_info   = metadata["monitor_info"]
        sequence.other_data             = metadata["other_data"]
        
        actions_sequence = raw_json_config["actions_sequence"]
        for raw_action in actions_sequence:
            if "coordinate" in raw_action:
                mouse_action = MouseAction(
                    (
                        raw_action["coordinate"]["x"],
                        raw_action["coordinate"]["y"]
                    ),
                    raw_action["delay"],
                    raw_action["click"],
                    raw_action["window_info"]
                )
                sequence.actions.append(mouse_action)
            elif "key" in raw_action:
                keyboard_action = KeyboardAction(
                    raw_action["key"],
                    raw_action["delay"]
                )
                sequence.actions.append(keyboard_action)
            else:
                raise AmiyaBaseException(f"Action ({raw_action}) can't be interpreted!")
            
        return sequence
            
    def print_sequence(self):
        for action in self.actions:
            print(action)

    def set_date_created_to_current(self):
        self.date_created = DatetimeHandler.get_datetime()
        
    def set_global_delay(self, global_delay: int):
        self.global_delay = global_delay    
    
    def get_runtime(self):
        runtime = 0
        for action in self.actions:
            runtime += action.delay
            runtime += self.global_delay
        return round(runtime, 2)
    