import os
import sys
import json
import shutil
from amiya.apps_manager.app import App, APP_CONFIG_FILENAME
from amiya.apps_manager.apps_viewer import AppsViewer
from amiya.utils.constants import APPS_DIRECTORY
from amiya.exceptions.exceptions import *
from amiya.utils.helper import *
from amiya.automation_handler.actions_controller.units.sequence import ActionsSequence
from amiya.automation_handler.actions_controller.actions_viewer import ActionsViewer

class AppsManager:
    os.system("")  # Enables ANSI escape characters in terminal
    
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
        app = App(name, exe_path, new=True)             # Create a new app object (new=True tells the App not to initialize the action controller just yet)
        app.id = self.__get_next_app_id()               # Assign ID to app (int)
        app.tags = [app.get_reformatted_app_name()]     # Assign a default tag during app creation
        
        self.print_app(app)                             # Tabulate and print app

        self.__verify_app_existance(app)                # Verify that the app doesn't already exist
        self.__verify_path_validity(app)                # Asks the user if the exe path is invalid
        
        app.create_app()                                # Create the app and save to config
        self.apps[app.id] = app                         # Add to apps dict (key: app_id, value: app_obj)
    
    def create_app_automated(self):
        app_name = input(atext(f"New Application's Name: "))
        app_path = input(atext(r"New Application's Path (E:\SomePath\Application.exe): "))
        self.create_app(app_name, app_path)


    def __verify_app_existance(self, app: App):
        if os.path.isfile(app.app_config_filepath):
            aprint(f"An app with name '{app.name}' already exist. Exiting.", log_type=LogType.ERROR); exit()
    
    def __verify_path_validity(self, app: App):
        if app.verified == False:
            aprint(f"The application's path failed to be verified (invalid path to .exe). Would you like to add this app anyways? [y/n] ", log_type=LogType.WARNING, end="")
            if input("").lower()!= "y": 
                exit()
    
    # ======================================
    # ===========| DELETE APP | ============
    # ======================================
    # TODO: Application ID isn't shifted forward when an app is deleted. 
    def delete_app(self):
        self.print_apps()
        user_input = input(atext(f"Which app would you like to DELETE? (0-{len(self.apps)-1}) "))
        
        app = self.apps[int(user_input)]
        user_input = input(atext(f"Are you sure you would like to delete app '{app.name}'? [y/n] "))
        if user_input.lower() != "y":
            return
        
        app_dir = os.path.join(APPS_DIRECTORY, app.get_reformatted_app_name())
        shutil.rmtree(app_dir)
        
        removed_value = self.apps.pop(app.id, None) 
        if removed_value == None: # If application cannot be found in self.apps
            raise AmiyaBaseException(f"App '{app.name}' can't be found in the apps dict.")
        
        aprint(f"The app '{app.name}' has been deleted.")
    
    
    # ======================================
    # =============| RUN APP | =============
    # ======================================
    def run_app(self):
        self.print_apps()
        user_input = input(atext(f"Which app would you like to run? (0-{len(self.apps)-1}) "))
        app = self.apps[int(user_input)]
        self.__start_app_and_verbose(app)
        
    def run_app_with_tag(self, tag):
        tag = self.__parse_tag(tag)
        app = self.__get_app_by_tag(tag)
        self.__start_app_and_verbose(app)
    
    def __start_app_and_verbose(self, app: App):
        ret = app.run()
        if ret == True:
            aprint(f"[PID {app.process.pid}] Application '{app.name}' started successfully!")
    
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
        
        def tag_exists(tag):
            try:
                self.__get_app_by_tag(tag)
                return True
            except Amiya_NoSuchTagException:
                return False
        
        self.print_apps()
        user_input = input(atext(f"Which app would you like to ADD a tag to? (0-{len(self.apps)-1}) "))
        app = self.apps[int(user_input)]                            
        
        new_tag = input(atext(f"What would be the tag? (no spaces): "))
        new_tag = self.__parse_tag(new_tag)             # Parse tag to remove leading and trailing spaces 
        if tag_exists(new_tag) == True:   # If tag already exists (duplicate tag), raise exception.
            raise Amiya_DuplicateTagException(
                    tag=new_tag, 
                    tagged_app_name=app.name
                )
        
        app.add_tag(new_tag)
        self.__save_app_config(app)
    
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
        self.__save_app_config(app)
    
    def __parse_tag(self, tag: str):
        return tag.strip()
    
        
    # HELPER FUNCTIONS ======================
    def __initial_setup(self):
        if not os.path.isdir(APPS_DIRECTORY):
            os.mkdir(APPS_DIRECTORY)
            
    def __get_next_app_id(self):
        return max(self.apps.keys()) + 1

    def __get_app_with_id(self, user_input_id: str) -> App:
        try:
            app = self.apps[int(user_input_id)]
        except KeyError:
            aprint(f"Your input (ID {user_input_id}) does not correspond to any apps.", log_type=LogType.ERROR)
        except ValueError:
            aprint(f"Expected an ID (such as 0 or 1) but got '{user_input_id}'.", log_type=LogType.ERROR)
        return app
    
    def __get_app_by_tag(self, tag) -> App | None:
        for _, app in self.apps.items():
            if tag in app.tags:
                return app
        raise Amiya_NoSuchTagException(tag)
            
    
            
    # =====================================================================================================================================
    # >>>>> AUTOMATION RELATED
    
    
    # =================================================
    # ===============| LIST SEQUENCES | ===============
    # =================================================
    def list_sequences(self):
        self.print_apps()
        user_input_id = input(atext(f"Which app would you like to see the automation sequences of? (0-{len(self.apps)-1}) "))
        app = self.__get_app_with_id(user_input_id)
          
        sequences: list[ActionsSequence] = []
        sequences = app.actions_controller.load_all_sequences()
        self.print_sequences(sequences)

    def list_sequences_with_tag(self, tag: str):
        tag = self.__parse_tag(tag)
        app = self.__get_app_by_tag(tag)
        
        sequences: list[ActionsSequence] = []
        sequences = app.actions_controller.load_all_sequences()
        print(sequences)
        self.print_sequences(sequences)
        
    def print_sequences(self, sequence_list: list[ActionsSequence], tablefmt="fancy_grid"):
        if len(sequence_list) == 0:
            aprint("No Sequence Recorded For Application."); return
        
        viewer = ActionsViewer()
        print(viewer.tabulate_multi_sequences(sequence_list, tablefmt))
        
    
    # =================================================
    # ==============| RECORD SEQUENCES | ==============
    # =================================================
    def record_sequence(self):
        self.print_apps()
        user_input_id = input(atext(f"Which app would you like to RECORD A NEW AUTOMATION SEQUENCE of? (0-{len(self.apps)-1}) "))
        app = self.__get_app_with_id(user_input_id)
        
        new_sequence_name = input(atext(f"Name of the new automation sequence (i.e. start-game): "))
        new_sequence_recorded = app.actions_controller.record_new_sequence(new_sequence_name, overwrite=False)
        
        self.print_sequence(new_sequence_recorded)

    def record_sequence_with_tag(self, tag: str):
        tag = self.__parse_tag(tag)
        app = self.__get_app_by_tag(tag)
        
        new_sequence_name = input(atext(f"Name of the new automation sequence (i.e. start-game): "))
        new_sequence_recorded = app.actions_controller.record_new_sequence(new_sequence_name, overwrite=False)
        
        self.print_sequence(new_sequence_recorded)
    
    def print_sequence(self, sequence: ActionsSequence, tablefmt="fancy_grid"):
        viewer = ActionsViewer()
        print(viewer.tabulate_sequence(sequence, tablefmt))


    # =================================================
    # ==============| RECORD SEQUENCES | ==============
    # =================================================
    def run_sequence(self):
        self.print_apps()
        user_input_id = input(atext(f"Which app would you like to RUN AN AUTOMATION SEQUENCE of? (0-{len(self.apps)-1}) "))
        app = self.__get_app_with_id(user_input_id)
        
        sequences: list[ActionsSequence] = []
        sequences = app.actions_controller.load_all_sequences()
        self.print_sequences(sequences)
        
        seq_name = input(atext(f"Which sequence would you like to run (i.e. start-game)? "))
        sequence: ActionsSequence = self.get_sequence_with_name(seq_name, sequences)
        
        aprint(f"The sequence '{sequence.sequence_name}' will run for {sequence.get_runtime()} seconds.\nContinue? [y/n] ", log_type=LogType.WARNING, end="")
        if input().lower() == "y":
            aprint(f"[{sequence.sequence_name}] Running...")
            sequence.run()
        
        aprint(f"[{sequence.sequence_name}] Sequence run completed!", log_type=LogType.SUCCESS)
        
    def run_sequence_with_tag(self, tag: str, seq_name: str = None):
        tag = self.__parse_tag(tag)
        app = self.__get_app_by_tag(tag)
        
        sequences: list[ActionsSequence] = []
        sequences = app.actions_controller.load_all_sequences()
        self.print_sequences(sequences)
        
        if seq_name == None:
            seq_name = input(atext(f"Which sequence would you like to run (i.e. start-game)? "))
        sequence: ActionsSequence = self.get_sequence_with_name(seq_name, sequences)
        
        aprint(f"The sequence '{sequence.sequence_name}' will run for {sequence.get_runtime()} seconds.\nContinue? [y/n] ", log_type=LogType.WARNING, end="")
        if input().lower() == "y":
            aprint(f"[{sequence.sequence_name}] Running...")
            sequence.run()
        
        aprint(f"[{sequence.sequence_name}] Sequence run completed!", log_type=LogType.SUCCESS)
        
    def get_sequence_with_name(self, seq_name: str, sequence_list: list[ActionsSequence]) -> ActionsSequence:
        seq_name = seq_name.strip().lower().replace(" ", "-")
        
        for seq in sequence_list:
            if seq.sequence_name == seq_name:
                return seq
        aprint(f"No sequence with name '{seq.sequence_name}' exists. Exiting.", log_type=LogType.ERROR); exit()

# am = AppManager()
# am.create_app("Arknights", "abc/abc.exe")
# am.create_app("Final Fantasy XIV", "abc/abc.exe")
# print(am.apps)