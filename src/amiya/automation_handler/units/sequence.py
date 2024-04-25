import os
import time
from datetime import datetime
from pynput import keyboard
from amiya.automation_handler.automation_config_handler import SequenceConfigHandler
from amiya.automation_handler.units.action import Action, MouseAction, KeyboardAction
from amiya.exceptions.exceptions import AmiyaBaseException, Amiya_AppNotFocusedException
from amiya.utils.constants import DATETIME_FORMAT
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
    
    def execute(self, safety_monitor: SafetyMonitor):
        pixel_calculator = PixelCalculator(self.primary_monitor_info)
        pynput_keyboard = keyboard.Controller()
        
        for idx, action in enumerate(self.actions):
            safety_monitor.app_is_focused()                      # If the application is no longer focused, stop the automation
            
            buffer_space = " "*5                                # Verbose current action
            aprint(f"(CMD {idx+1}/{len(self.actions)}) Executing: {action.__repr__()}{buffer_space}", end="\r")
            
            time.sleep(self.global_delay)                       # Execute current action after global delay
            if isinstance(action, KeyboardAction):
                action.execute(pynput_keyboard)
            elif isinstance(action, MouseAction):
                action.execute()
            
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
    