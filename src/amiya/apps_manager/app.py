import os
import sys
import json
import time
import psutil
import subprocess
from amiya.utils.constants import APPS_DIRECTORY
from amiya.exceptions.exceptions import *

APP_CONFIG_FILENAME = "app-config.json"

class App:
    def __init__(self, name: str, exe_path: str, tags: list = []):
        self.id         = None      # Assigned automatically by the AppManager at creation
        self.name       = name
        self.exe_path   = exe_path
        self.tags       = tags
        self.verified   = self.__verify_app()
        
        self.process    = None
    
        self.app_config_dirpath     = os.path.join(APPS_DIRECTORY, self.get_reformatted_app_name())
        self.app_config_filepath    = os.path.join(self.app_config_dirpath, APP_CONFIG_FILENAME)


    def __str__(self) -> str:
        return f"App(name='{self.name}', exe_path='{self.exe_path}', verified='{self.verified}')"
    
    
    def __repr__(self) -> str:
        return self.__str__()


    def run(self):
        if self.verified == True:
            subprocess.Popen([self.exe_path])
            
            TIMEOUT = 30
            APP_EXE_NAME = os.path.basename(self.exe_path)
            starting_time = time.time()
            while time.time() - starting_time < TIMEOUT:
                for p in psutil.process_iter():
                    if p.name() == APP_EXE_NAME:
                        try:
                            self.process = psutil.Process(p.pid)
                            return True
                        except Exception as ex:
                            print(ex.__traceback__)
                time.sleep(1)
            return False
        else:
            raise Amiya_AppInvalidPathException(path=self.exe_path)


    def to_json(self):
        return {
            "id"        : self.id,
            "name"      : self.name,
            "exe_path"  : self.exe_path,
            "tags"      : self.tags,
            "verified"  : self.verified
        }


    @staticmethod
    def read_json(app_config):
        try:
            with open(app_config, "r") as rf:
                config = json.load(rf)
                app = App(
                    config["name"], 
                    config["exe_path"], 
                    config["tags"]
                )
                app.id = config["id"]
                return app
        except Exception as ex:
            raise ex
        

    def add_tag(self, tag_name):
        self.tags.append(tag_name)
        
    def remove_tag(self, tag_name):
        self.tags.remove(tag_name)
        
        
    def get_reformatted_app_name(self):
        return self.name.lower().strip().replace(" ", "-")
    
    
    def __verify_app(self):
        return len(self.name) > 0 and os.path.isfile(self.exe_path)
