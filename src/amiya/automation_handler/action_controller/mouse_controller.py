
import time
from automation_handler.config_controller.config_handler import ConfigHandler
from automation_handler.action_controller.mouse_action import MouseAction
from automation_handler.action_controller.mouse_recorder import ActionRecorder


class MouseController:
    def __init__(self, config_handler: ConfigHandler):
        self.config_handler = config_handler
        self.mouse_actions: list[MouseAction] = []
        self.__parse_config()
        
    
    def run(self):
        for action in self.mouse_actions:
            print(action.__repr__())
            action.execute()
            
    def __parse_config(self) -> list[MouseAction]:
        
        for raw_action in self.config_handler.config:
            mouse_action = MouseAction(
                (
                    raw_action["coordinate"]["x"],
                    raw_action["coordinate"]["y"]
                ),
                raw_action["delay"],
                raw_action["click"]
            )
            self.mouse_actions.append(mouse_action)
        
    
    def record_actions(self):
        action_recorder = ActionRecorder()
        action_recorder.record()                                                        # Record mouse actions until "space-bar" is pressed
        json_actions = [action.to_json() for action in action_recorder.actions]         # Convert MouseActions into a list of JSON objects
        ret = self.config_handler.write_to_config(json_actions)                         # Write JSON actions to config

    