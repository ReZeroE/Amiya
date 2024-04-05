import os
import sys
import json
import time
import psutil
import subprocess
from amiya.utils.constants import APPS_DIRECTORY, FOCUS_PID_EXE
from amiya.exceptions.exceptions import *


APP_CONFIG_FILENAME = "app-config.json"

class App:
    def __init__(self, name: str, exe_path: str, tags: list = []):
        self.id         = None      # Assigned automatically by the AppManager at creation
        self.name       = name
        self.exe_path   = exe_path
        self.tags       = tags
        self.verified   = self.__verify_app_path()
        
        # Note that the process variable is a snapshot of the application's process. 
        # It is not always (and most likely not) up-to-date as the program continues to run. 
        # This variable is only updated when is_running() is called and therefore this variable 
        # should NEVER be used to identify the current activity/status of the application.
        #
        # This variable should ONLY be used to identify the initial status of the application
        # as its started since any callback to is_running() (while a new instance of the application
        # is created) will overwrite the previous process.
        self.process    = None
    
        self.app_config_dirpath     = os.path.join(APPS_DIRECTORY, self.get_reformatted_app_name())
        self.app_config_filepath    = os.path.join(self.app_config_dirpath, APP_CONFIG_FILENAME)


    def __str__(self) -> str:
        return f"App(name='{self.name}', exe_path='{self.exe_path}', verified='{self.verified}')"
    
    def __repr__(self) -> str:
        return self.__str__()

    def run(self):
        if self.verified == True:
            subprocess.Popen([self.exe_path], shell=True)
            
            TIMEOUT = 30
            APP_EXE_NAME = os.path.basename(self.exe_path)
            starting_time = time.time()
            while time.time() - starting_time < TIMEOUT:
                if self.is_running():
                    return True
                time.sleep(1)
            return False
        else:
            raise Amiya_AppInvalidPathException(path=self.exe_path)

    def is_running(self):
        APP_EXE_NAME = os.path.basename(self.exe_path)
        for p in psutil.process_iter():
            if p.name() == APP_EXE_NAME:
                try:
                    self.process = psutil.Process(p.pid)
                    if self.process.is_running():
                        return True
                    return False
                except Exception as ex:
                    print(ex.__traceback__)
                    raise AmiyaBaseException("Failed to identify the app's process.")
        return False
    
    def bring_to_foreground(self):
        if self.is_running():
            subprocess.run([FOCUS_PID_EXE, self.process.pid])
        else:
            raise AmiyaBaseException(f"The app '{self.name}' is currently not running, therefore can't be brought to foreground.")

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
    
    def __verify_app_path(self):
        return len(self.name) > 0 and os.path.isfile(self.exe_path)

