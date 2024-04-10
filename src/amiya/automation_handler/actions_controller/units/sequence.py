import os
from pynput import keyboard
from amiya.automation_handler.config_controller.config_handler import ActionsConfigHandler
from amiya.automation_handler.actions_controller.units.action import Action, MouseAction, KeyboardAction
from amiya.exceptions.exceptions import AmiyaBaseException

class ActionsSequence:
    def __init__(self, sequence_name: str = None):
        self.sequence_name = sequence_name
        self.actions: list[Action] = []
    
    def run(self):
        pynput_keyboard = keyboard.Controller()
        
        for action in self.actions:
            if isinstance(action, KeyboardAction):
                action.execute(pynput_keyboard)
            elif isinstance(action, MouseAction):
                action.execute()
            
    def add(self, action: Action):
        assert(isinstance(action, Action))
        self.actions.append(action)

    def to_json(self):
        return [action.to_json() for action in self.actions]

    def parse_config(self, raw_json_config: list):
        for raw_action in raw_json_config:
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

        
    
    