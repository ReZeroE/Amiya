import os
from datetime import datetime
from pynput import keyboard
from amiya.automation_handler.config_controller.config_handler import ActionsConfigHandler
from amiya.automation_handler.actions_controller.units.action import Action, MouseAction, KeyboardAction
from amiya.exceptions.exceptions import AmiyaBaseException, Amiya_AppNotFocusedException
from amiya.utils.constants import DATETIME_FORMAT
from amiya.utils.helper import *
from amiya.apps_manager.safty_monitor import SaftyMonitor

class ActionsSequence:
    def __init__(
        self, 
        sequence_name: str = None, 
        date_created: datetime = None
    ):
        self.sequence_name  = sequence_name
        self.date_created   = date_created
        self.other_data     = None
        self.actions: list[Action] = []
    
    def execute(self, safty_monitor: SaftyMonitor):
        pynput_keyboard = keyboard.Controller()
        for action in self.actions:
            
            # If the application is no longer focused, then the automation needs to be stopped
            focused = safty_monitor.is_focused()  
            if not focused:
                raise Amiya_AppNotFocusedException()
            
            print(action.__repr__(), end="\r")
            
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
            "sequence_name": self.sequence_name,
            "date_created": self.datetime_to_str(),
            "other_data": self.other_data
        }
        json_data["actions_sequence"] = [action.to_json() for action in self.actions]
        return json_data

    def parse_config(self, raw_json_config: list):
        metadata            = raw_json_config["metadata"]
        self.sequence_name  = metadata["sequence_name"]
        self.date_created   = self.str_to_datetime(metadata["date_created"])
        self.other_data     = metadata["other_data"]
        
        actions_sequence = raw_json_config["actions_sequence"]
        for raw_action in actions_sequence:
            if "coordinate" in raw_action:
                mouse_action = MouseAction(
                    (
                        raw_action["coordinate"]["x"],
                        raw_action["coordinate"]["y"]
                    ),
                    raw_action["delay"],
                    raw_action["click"]
                )
                self.actions.append(mouse_action)
                
            elif "key" in raw_action:
                keyboard_action = KeyboardAction(
                    raw_action["key"],
                    raw_action["delay"]
                )
                self.actions.append(keyboard_action)

            else:
                raise AmiyaBaseException(f"Action ({raw_action}) can't be interpreted!")
            
    def print_sequence(self):
        for action in self.actions:
            print(action)

    def datetime_to_str(self):
        return self.date_created.strftime(DATETIME_FORMAT)
        
    def str_to_datetime(self, datetime_str):
        return datetime.strptime(datetime_str, DATETIME_FORMAT)
        
    def set_date_created_to_current(self):
        self.date_created = datetime.now()
        
    def get_runtime(self):
        runtime = 0
        for action in self.actions:
            runtime += action.delay
        return round(runtime, 2)
    