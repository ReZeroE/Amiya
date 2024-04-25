import os
import sys
import json
import time
import psutil
import subprocess
from pathlib import Path
from amiya.utils.constants import APPS_DIRECTORY, FOCUS_PID_EXE
from amiya.exceptions.exceptions import *
from amiya.automation_handler.automation_controller import AutomationController
from amiya.apps_manager.sync_controller.sys_uuid_controller import SysUUIDController

APP_AUTOMATION_DIRNAME          = "automation"
APP_AUTOMATION_SEQUENCE_DIRNAME = "sequence"
APP_AUTOMATION_PLATE_DIRNAME    = "plate"
APP_CONFIG_FILENAME             = "app-config.json"

class App:
    def __init__(
        self, 
        name        : str, 
        exe_path    : str, 
        tags        : list = [], 
        sys_uuid    : str = SysUUIDController.system_uuid,
        new         : bool = False
    ):
        self.id         = None      # Assigned automatically by the AppManager at creation
        self.name       = name
        self.exe_path   = Path(self.__parse_exe_path(exe_path))
        self.tags       = tags
        self.verified   = self.__verify_app_path()
        self.sys_uuid   = sys_uuid  # Used to identify whether the application is synced with the current machine
        
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
        
        # Automation directories
        self.sequence_dirpath = os.path.join(self.app_config_dirpath, APP_AUTOMATION_DIRNAME, APP_AUTOMATION_SEQUENCE_DIRNAME)
        self.plate_dirpath = os.path.join(self.app_config_dirpath, APP_AUTOMATION_DIRNAME, APP_AUTOMATION_PLATE_DIRNAME)
        
        self.new = new
        self.automation_controller = None
        if not new:
            self.automation_controller = AutomationController(
                self.sequence_dirpath,
                self.plate_dirpath
            )



    def __str__(self) -> str:
        return f"App(name='{self.name}', exe_path='{self.exe_path}', verified='{self.verified}')"
    
    def __repr__(self) -> str:
        return self.__str__()


    # ========================================
    # ============| APP CREATOR | ============
    # ========================================
    
    def create_app(self):
        if self.new:
            self.__create_app_dir_strucure()      # Create the app directory structure to hold all the configs (base config and automation config)
            self.save_app_config()                # Write the base app config (creates the app)
            self.automation_controller = AutomationController(self.app_automation_dirpath)
        else:
            AmiyaBaseException(f"Cannot create app when app instance is not defined as new (self.new=False).")
        
    def save_app_config(self):
        try:
            with open(self.app_config_filepath, "w") as wf:
                json.dump(self.to_json(), wf, indent=4)
        except Exception as ex:
            raise ex
        
    def __create_app_dir_strucure(self):
        if not os.path.exists(self.app_config_dirpath):     # Create the base app directory (amiya/apps/<app_name>)
            os.mkdir(self.app_config_dirpath)
        if not os.path.exists(self.sequence_dirpath):       # Create the app automation sequence directory (amiya/apps/<app_name>/automation/sequence)
            os.mkdir(self.sequence_dirpath)
        if not os.path.exists(self.plate_dirpath):          # Create the app automation plate directory (amiya/apps/<app_name>/automation/plate)
            os.mkdir(self.plate_dirpath)

    # =======================================
    # ============| APP DRIVER | ============
    # =======================================

    def run(self) -> bool:
        # If the application is already running
        if self.is_running():
            self.bring_to_foreground()
            return True
        
        # If the application is not running, then start the application
        if self.verified == True:   
            subprocess.Popen([self.exe_path], shell=True)
            
            if self.started_successfully():
                self.bring_to_foreground()
                return True
            return False
        else:
            raise Amiya_AppInvalidPathException(path=self.exe_path)

    def started_successfully(self) -> bool:
        TIMEOUT = 30
        starting_time = time.time()
        while time.time() - starting_time < TIMEOUT:
            if self.is_running():
                return True
            time.sleep(1)
        return False

    def is_running(self) -> bool:
        APP_EXE_NAME = os.path.basename(self.exe_path)
        for p in psutil.process_iter():
            if APP_EXE_NAME.replace(".exe", "") in p.name():
                try:
                    self.process = psutil.Process(p.pid)
                    if self.process.is_running():
                        return True
                    return False
                except Exception as ex:
                    raise AmiyaBaseException("Failed to identify the app's process due to an unknown error.")
        return False
    
    def bring_to_foreground(self):
        try:
            if self.is_running():
                subprocess.run([FOCUS_PID_EXE, str(self.process.pid)], shell=True)
        except:
            raise AmiyaBaseException(f"The app '{self.name}' is currently not running, therefore can't be brought to foreground.")

    # ==========================================
    # ============| APP UTILITIES | ============
    # ==========================================

    def to_json(self):
        return {
            "id"        : self.id,
            "name"      : self.name,
            "exe_path"  : str(self.exe_path),
            "tags"      : self.tags,
            "verified"  : self.verified,
            "sys_uuid"  : self.sys_uuid
        }

    @staticmethod
    def read_json(app_config):
        try:
            with open(app_config, "r") as rf:
                config = json.load(rf)
                app = App(
                    config["name"], 
                    config["exe_path"], 
                    config["tags"],
                    config["sys_uuid"]
                )
                app.id = int(config["id"])
                return app
        except Exception as ex:
            raise ex
        
    def add_tag(self, tag_name):
        self.tags.append(tag_name)
        
    def remove_tag(self, tag_name):
        self.tags.remove(tag_name)
    
    def get_reformatted_app_name(self):
        # List of characters that are invalid in file and folder names for Windows and most other OS
        invalid_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
        
        sanitized_name = self.name.lower().strip()
        for char in invalid_chars:
            sanitized_name = sanitized_name.replace(char, '')
        
        sanitized_name = sanitized_name.replace(" ", "-")
        return sanitized_name
    
    def set_new_path(self, new_path):
        # Used for syncing apps across different machines only
        self.exe_path = new_path
        self.verified = self.__verify_app_path()
    
    def set_new_uuid(self):
        self.sys_uuid = SysUUIDController.get_system_uuid()
    
    # ==========================================
    # ==========| HELPER FUNCTIONS | ===========
    # ==========================================
    def __parse_exe_path(self, exe_path: str):
        return exe_path.replace('"', "").strip()
    
    def __verify_app_path(self):
        return self.exe_path.exists()


