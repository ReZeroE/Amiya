import os
import json
from abc import ABC 
from amiya.exceptions.exceptions import *

class JSONConfigHandler(ABC):
    def __init__(self, config_abs_path, config_type=dict):
        self.config_file = config_abs_path
        self.config_type = config_type

    def load_config(self):
        try:
            with open(self.config_file, "r") as rf:
                config = json.load(rf)
                return config
        except FileNotFoundError:
            raise Amiya_ConfigDoesNotExistException(config_file=self.config_file)

    def save_config(self, json_payload) -> bool:
        try:
            with open(self.config_file, "w") as wf:
                json.dump(json_payload, wf, indent=4)
        except Exception as ex:
            AmiyaBaseException(f"Config file '{self.config_file}' cannot be created due to an unknown error.")
        return True

    def config_exists(self):
        return os.path.isfile(self.config_file)
        
    def validate_config(self):
        ...