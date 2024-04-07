import os
import json
from amiya.exceptions.exceptions import *

class JSONConfigHandler:
    def __init__(self, config_abs_path, config_type=dict, config_stub=None):
        self.config_file = config_abs_path
        self.config_type = config_type
        self.config_stub = config_stub
        self.initialize_config_file()
        
        self.config = self.load_config()

    def load_config(self):
        try:
            with open(self.config_file, "r") as rf:
                config = json.load(rf)
                return config
        except FileNotFoundError:
            raise AmiyaBaseException(f"Config file not found (stub did not auto generate).")

    def save_config(self, json_payload, overwrite=False):
        if self.config_exists() and not overwrite:
            raise AmiyaBaseException(f"Config file already exists and cannot be overwritten (overwrite set to False).")
        
        try:
            with open(self.config_file, "w") as wf:
                json.dump(json_payload, wf, indent=4)
        except FileNotFoundError:
            raise FileNotFoundError(f"config not found (stab did not auto generate)."); exit(1)
        return True

    def config_exists(self):
        return os.path.isfile(self.config_file)

    def initialize_config_file(self):
        if self.config_exists() == False:
            if self.config_stub != None:
                print(f"Config file not found, creating config file from stub.")
                os.system(f'type nul > {self.config_file}' if os.name == 'nt' else f'touch {self.config_file}')
                with open(self.config_file, "w") as wf:
                    wf.write(json.dumps(self.config_stub, indent=4))
            else:
                AmiyaBaseException(f"Config ({self.config_file}) doesn't exist and stub is not provided. Existing.")
        
                