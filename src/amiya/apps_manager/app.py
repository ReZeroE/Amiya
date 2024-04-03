import os
import sys
import json
import subprocess
from utils.constants import APPS_DIRECTORY

APP_CONFIG_FILENAME = "app-config.json"

class App:
    def __init__(self, name: str, exe_path: str):
        self.id         = None      # Assigned automatically by the AppManager at creation
        self.name       = name 
        self.exe_path   = exe_path
        self.verified   = self.__verify_app()
    
        self.app_config_dirpath     = os.path.join(APPS_DIRECTORY, self.get_reformatted_app_name())
        self.app_config_filepath    = os.path.join(self.app_config_dirpath, APP_CONFIG_FILENAME)

    def __str__(self) -> str:
        return f"App(name='{self.name}', exe_path='{self.exe_path}', verified='{self.verified}')"
    
    def __repr__(self) -> str:
        return self.__str__()

    def run(self):
        if self.verified == True:
            subprocess.Popen([self.exe_path])
        else:
            raise Exception("Path failed to be verified (invalid path).")

    def to_json(self):
        return {
            "id"        : self.id,
            "name"      : self.name,
            "exe_path"  : self.exe_path,
            "verified"  : self.verified
        }
        
    @staticmethod
    def read_json(app_config):
        try:
            with open(app_config, "r") as rf:
                config = json.load(rf)
                app = App(config["name"], config["exe_path"])
                app.id = config["id"]
                return app
        except Exception as ex:
            raise ex
        
    def get_reformatted_app_name(self):
        return self.name.lower().strip().replace(" ", "-")
    
    def __verify_app(self):
        return len(self.name) > 0 and os.path.isfile(self.exe_path)
