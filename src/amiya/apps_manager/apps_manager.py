import os
import sys
import json
import shutil
from amiya.apps_manager.app import App, APP_CONFIG_FILENAME
from amiya.apps_manager.apps_viewer import AppsViewer
from amiya.utils.constants import APPS_DIRECTORY
from amiya.exceptions.exceptions import *
from amiya.utils.helper import *

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
        app = App(name, exe_path)                       # Create a new app object
        app.id = len(self.apps)                         # Assign ID to app (int)
        app.tags = [app.get_reformatted_app_name()]     # Assign a default tag during app creation
        
        self.print_app(app)                             # Tabulate and print app
        
        if app.verified == False:
            ipt = input(atext(f"The application's path failed to be verified (invalid path to .exe), would you like to add this app anyways? [y/n] ", log_type=LogType.WARNING))
            if ipt.lower() != "y": return
        
        if os.path.isfile(app.app_config_filepath):
            raise Amiya_AppExistsException(app.name)    
        
        self.__create_app_dir(app)                      # Create app dir if it doesn't exist already
        self.__write_app_config(app)                    # Create app config file
        self.apps[app.id] = app                         # Add to apps dict (key: app_id, value: app_obj)
    
    def create_app_automated(self):
        app_name = input(atext(f"New Application's Name: "))
        app_path = input(atext(r"New Application's Path (E:\SomePath\Application.exe): "))
        self.create_app(app_name, app_path)
    
    def __create_app_dir(self, app: App):
        if not os.path.exists(app.app_config_dirpath):
            os.mkdir(app.app_config_dirpath)
        
    def __write_app_config(self, app: App):
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
        user_input = input(atext(f"Which app would you like to DELETE? (0-{len(self.apps)-1}) "))
        
        app = self.apps[int(user_input)]
        user_input = input(atext(f"Are you sure you would like to delete app '{app.name}'? [y/n] "))
        if user_input.lower() != "y":
            return
        
        app_dir = os.path.join(APPS_DIRECTORY, app.name)
        shutil.rmtree(app_dir)
    
    
    # ======================================
    # =============| RUN APP | =============
    # ======================================
    def run_app(self):
        self.print_apps()
        user_input = input(atext(f"Which app would you like to run? (0-{len(self.apps)-1}) "))
        
        app = self.apps[int(user_input)]
        ret = app.run()
        
        if ret == True:
            aprint(f"[PID {app.process.pid}] App started successfully!")
        
    def run_app_with_tag(self, tag):
        tag = self.__parse_tag(tag)
        if self.__verify_tag_exists(tag) == False:  # Tag does not exist!
            raise Amiya_NoSuchTagException(tag)
        
        app = self.__get_app_by_tag(tag)
        ret = app.run()
        
        if ret == True:
            aprint(f"[PID {app.process.pid}] App started successfully!")
    
    
    # ======================================
    # ============| VIEW APPS | ============
    # ======================================
    def print_app(self, app: App, format="fancy_grid"):
        tabulated_apps = AppsViewer.tabulate_app(app, tablefmt=format)
        print(tabulated_apps)
    
    def print_apps(self, format="fancy_grid"):
        tabulated_apps = AppsViewer.tabulate_apps(self.apps, tablefmt=format)
        print(tabulated_apps)
    
    def print_tags(self, app: App, format="fancy_grid"):
        tabulated_tags = AppsViewer.tabulate_tags(app.tags, tablefmt=format)
        print(tabulated_tags)
    
    
    # =======================================================
    # ============| ADD/REOVE TAGS TO/FROM APP | ============
    # =======================================================
    def add_tag(self):
        self.print_apps()
        user_input = input(atext(f"Which app would you like to ADD a tag to? (0-{len(self.apps)-1}) "))
        app = self.apps[int(user_input)]                            
        
        new_tag = input(atext(f"What would be the tag? (no spaces): "))
        new_tag = self.__parse_tag(new_tag)             # Parse tag to remove leading and trailing spaces 
        if self.__verify_tag_exists(new_tag) == True:   # If tag already exists (duplicate tag), raise exception.
            raise Amiya_DuplicateTagException(
                    tag=new_tag, 
                    tagged_app_name=app.name
                )
        
        app.add_tag(new_tag)
        self.__write_app_config(app)
    
    def remove_tag(self):
        self.print_apps()
        user_input = input(atext(f"Which app would you like to REMOVE a tag from? (0-{len(self.apps)-1}) "))
        app = self.apps[int(user_input)]
        
        self.print_tags(app)
        tag_idx = input(atext(f"Which tag would you like to remove? (0-{len(app.tags)-1}): "))
        removing_tag = app.tags[int(tag_idx)]
        try:
            app.remove_tag(removing_tag)
        except ValueError:
            raise Amiya_NoSuchTagException(removing_tag)
        self.__write_app_config(app)
    
    def __parse_tag(self, tag: str):
        return tag.strip()
    
        
    # HELPER FUNCTIONS ======================
    def __initial_setup(self):
        if not os.path.isdir(APPS_DIRECTORY):
            os.mkdir(APPS_DIRECTORY)
            
    def __verify_tag_exists(self, tag):
        if self.__get_app_by_tag(tag) == None:
            return False
        return True

    def __get_app_by_tag(self, tag) -> App | None:
        for _, app in self.apps.items():
            if tag in app.tags:
                return app
        return None
    
    
    
# am = AppManager()
# am.create_app("Arknights", "abc/abc.exe")
# am.create_app("Final Fantasy XIV", "abc/abc.exe")
# print(am.apps)