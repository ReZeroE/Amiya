
import time
from amiya.automation_handler.config_controller.config_handler import ConfigHandler
from amiya.automation_handler.action_controller.actions import Action, MouseAction, KeyboardAction
from amiya.automation_handler.action_controller.mouse_recorder import ActionRecorder
from amiya.exceptions.exceptions import AmiyaBaseException

class ActionController:
    def __init__(self, config_handler: ConfigHandler):
        self.config_handler = config_handler
        self.actions: list[Action] = []
        self.__parse_config()
        
    
    def run(self):
        for action in self.actions:
            print(action.__repr__())
            action.execute()
            
    def __parse_config(self) -> list[Action]:
        for raw_action in self.config_handler.config:
            if "coor" in raw_action:
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
                
            raise AmiyaBaseException(f"Action ({raw_action}) can't be interpreted!")
        
    
    def record_actions(self):
        action_recorder = ActionRecorder()
        action_recorder.record()                                                        # Record mouse actions until "space-bar" is pressed
        json_actions = [action.to_json() for action in action_recorder.actions]         # Convert MouseActions into a list of JSON objects
        ret = self.config_handler.write_to_config(json_actions)                         # Write JSON actions to config

    