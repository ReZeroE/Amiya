import os
import json
from amiya.automation_handler.actions_controller.units.action import Action, KeyboardAction, MouseAction
from amiya.utils.json_handler import JSONConfigHandler
from amiya.exceptions.exceptions import *

class ActionsConfigHandler(JSONConfigHandler):
    def __init__(self, config_abs_path, config_type=list):
        super().__init__(
            config_abs_path,
            config_type
        )
    
    
    def validate_config(self):
        pass
    
    # def validate_config(self):
    #     for action in self.load_config():
    #         if "coordinate" in action:
    #             if not isinstance(action["coordinate"]["x"], int) or not isinstance(action["coordinate"]["y"], int):
    #                 print(f'[coordinate] Expected (int, int), but got ({type(action["coordinate"]["x"])}, {type(action["coordinate"]["x"])})')
    #             if not isinstance(action["delay"], float):
    #                 print(f'[delay] Expected float, but got {type(action["delay"])}')
    #             if not isinstance(action["click"], bool):
    #                 print(f'[click] Expected bool, but got {type(action["click"])}')
                    
    #         elif "key" in action:
    #             if not isinstance(action["key"], str):
    #                 print(f'[key] Expected str, but got {type(action["key"])}')
    #             if not isinstance(action["delay"], int):
    #                 print(f'[delay] Expected int, but got {type(action["delay"])}')
                
    #         else:
    #             raise AmiyaBaseException(f"Incorrect action config read (validation failed). \n Got: {action}")