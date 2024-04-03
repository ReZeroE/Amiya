import os
import sys
import json
import shutil
from apps_manager.app import App, APP_CONFIG_FILENAME
from apps_manager.apps_viewer import AppsViewer
from utils.constants import APPS_DIRECTORY

class AppsManager:
    def __init__(self):
        self.__initial_setup()
        self.apps : dict[int, App] = self.__read_apps()
        
    
    # ======================================
    # ============| READ APPS | ============
    # ======================================
    def __read_apps(self) -> list[App]:
        apps_name_list = os.listdir(APPS_DIRECTORY)
        apps_dict: dict[int, App] = dict()
        
        for app_name in apps_name_list:
            app_config = os.path.join(APPS_DIRECTORY, app_name, APP_CONFIG_FILENAME)
            if os.path.isfile(app_config):
                app = App.read_json(app_config)
                apps_dict[app.id] = app
                
        return apps_dict
    
    
    # ======================================
    # ===========| CREATE APPS | ===========
    # ======================================
    
    def create_app(self, name, exe_path):
        app = App(name, exe_path)          # Create a new app object
        app.id = len(self.apps)            # Assign ID to app (int)
        
        if os.path.isfile(app.app_config_filepath):
            raise Exception("App already exists. Can't be recreated.")    
        
        self.__create_app_dir(app)         # Create app dir if not exists already
        self.__create_app_config(app)      # Create app config file
        self.apps[app.id] = app            # Add to apps dict (key: app_id, value: app_obj)
    
    def __create_app_dir(self, app: App):
        if not os.path.exists(app.app_config_dirpath):
            os.mkdir(app.app_config_dirpath)
        
    def __create_app_config(self, app: App):
        try:
            with open(app.app_config_filepath, "w") as wf:
                json.dump(app.to_json(), wf, indent=4)
        except Exception as ex:
            raise ex
        
    
    # ======================================
    # ===========| DELETE APP | ============
    # ======================================
    
    def delete_app(self):
        self.print_apps()
        user_input = input(f"Which app would you like to DELETE? (0-{len(self.apps)-1}) ")
        
        app = self.apps[int(user_input)]
        user_input = input(f"Are you sure you would like to delete app '{app.name}'? [y/n] ")
        if user_input.lower() != "y":
            return
        
        app_dir = os.path.join(APPS_DIRECTORY, app.name)
        shutil.rmtree(app_dir)
    
    
    # ======================================
    # =============| RUN APP | =============
    # ======================================
    
    def run_app(self):
        self.print_apps()
        user_input = input(f"Which app would you like to run? (0-{len(self.apps)-1}) ")
        
        app = self.apps[int(user_input)]
        app.run()
        
        
    # ======================================
    # ============| VIEW APPS | ============
    # ======================================
    
    def print_apps(self, format="fancy_grid"):
        tabulated_apps = AppsViewer.tabulate_apps(self.apps, tablefmt=format)
        print(tabulated_apps)
    
    
    # HELPER FUNCTIONS ======================
    def __initial_setup(self):
        if not os.path.isdir(APPS_DIRECTORY):
            os.mkdir(APPS_DIRECTORY)
            

    
# am = AppManager()
# am.create_app("Arknights", "abc/abc.exe")
# am.create_app("Final Fantasy XIV", "abc/abc.exe")
# print(am.apps)