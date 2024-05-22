import os
import sys
import json
import shutil
import time
import signal
from termcolor import colored
from amiya.apps_manager.app import App, APP_CONFIG_FILENAME
from amiya.apps_manager.apps_viewer import AppsViewer
from amiya.utils.constants import APPS_DIRECTORY, AMIYA_PID
from amiya.exceptions.exceptions import *
from amiya.utils.helper import *
from amiya.automation_handler.units.sequence import AutomationSequence
from amiya.automation_handler.automation_viewer import AutomationViewer
from amiya.apps_manager.safety_monitor import SafetyMonitor
from amiya.apps_manager.sync_controller.sync_controller import AppSyncController
from amiya.apps_manager.sync_controller.sys_uuid_controller import SYSTEM_UUID
from amiya.module_utilities.power_controller import PowerUtils

# from elevate import elevate; elevate()

class AppsManager:
    os.system("")  # Enables ANSI escape characters in terminal
    
    def __init__(self, verbose=True):
        self.__initial_setup()
        self.apps : dict[int, App] = self.__read_apps()
        self.verbose = verbose


    # ======================================
    # ============| READ APPS | ============
    # ======================================
    def __read_apps(self) -> dict[int, App]:
        apps_name_list = os.listdir(APPS_DIRECTORY)
        apps_dict: dict[int, App] = dict()
        
        for app_name in apps_name_list:
            app_config = os.path.join(APPS_DIRECTORY, app_name, APP_CONFIG_FILENAME)
            if os.path.isfile(app_config):
                app = App.read_json(app_config)
                app = self.__update_hash(app)
                apps_dict[app.id] = app

        return apps_dict
    
    def __update_hash(self, app: App):
        # Updates application executable's hash value automatically every time when the apps are loaded.
        # 
        # Syncing logic with hash:
        # If the hash is different, path is the same: auto update exe hash
        # Elif hash is the same, path is different (exe_name the same): force `sync`
        # Elif both the hash and path are different (exe_name the same): force `sync`
        # Elif hash is null: unable to `sync`
        
        if app.verified:
            curr_app_exe_hash = HashCalculator.calculate_file_hash(app.exe_path)
            if curr_app_exe_hash != app.exe_hash:
                app.exe_hash = curr_app_exe_hash
                app.save_app_config()
        else:
            # If the application's path does not exist on the current machine, do nothing.
            # When the apps are loaded, if a path doesn't exist, then the previous hash should
            # presist until the path is corrected and then the hash will automatically reset.
            # If the hash is set to None on app load, then the application won't be synced 
            # properly the next run. 
            pass

        return app
   
   
    # ======================================
    # ===========| CREATE APPS | ===========
    # ======================================
    
    def create_app(self, name, exe_path):
        app = App(name, exe_path, new=True)             # Create a new app object
        app.id = self.__get_next_app_id()               # Assign ID to app (int)
        app.tags = [app.get_reformatted_app_name()]     # Assign a default tag during app creation
        
        self.print_app(app)                             # Tabulate and print app

        self.__verify_app_existance(app)                # Verify that the app doesn't already exist
        self.__verify_path_validity(app)                # Asks the user if the exe path is invalid
        
        app.create_app()                                # Create the app and save to config
        self.apps[app.id] = app                         # Add to apps dict (key: app_id, value: app_obj)
        
        cmd = color_cmd(f"amiya start {app.get_reformatted_app_name()}")
        aprint(f"Application '{name}' has been successfully created and configured!\n\nTo start the app, run `{cmd}`")
        print("")
    
    def create_app_automated(self):
        app_name = input(atext(f"New Application's Name: "))
        app_path = input(atext(r"New Application's Path (E:\SomePath\Application.exe): "))
        self.create_app(app_name, app_path)


    def __verify_app_existance(self, app: App):
        if os.path.isfile(app.app_config_filepath):
            aprint(f"An app with name '{app.name}' already exist. Exiting.", log_type=LogType.ERROR); raise AmiyaExit()
    
    def __verify_path_validity(self, app: App):
        if app.verified == False:
            aprint(f"The application's path failed to be verified (invalid path to .exe). Would you like to add this app anyways? [y/n] ", log_type=LogType.WARNING, end="")
            if input("").lower()!= "y": 
                raise AmiyaExit()
    
    
    # ======================================
    # ===========| DELETE APP | ============
    # ======================================
    
    def delete_app(self, tag: str = None):
        self.__verify_non_empty_apps_dir()
        
        app = None
        
        if tag == None:                             # If no application tag is inputted by user
            self.print_apps()
            user_input = input(atext(f"Which app would you like to DELETE? (0-{len(self.apps)-1}) "))
            app = self.apps[int(user_input)]
        else:                                       # If user inputted an application tag tag
            tag = self.__parse_tag(tag)
            app = self.get_app_by_tag(tag)
        
        user_input = input(atext(f"Are you sure you would like to delete app '{app.name}'? [y/n] "))
        if user_input.lower() != "y":
            return
        
        self.__safe_delete_app(app)
        aprint(f"The app '{app.name}' has been deleted.")
    
    def __safe_delete_app(self, app: App):
        self.__purge_app(app)
        self.__reset_apps_id(app.id)
    
    def __safe_delete_multiple_apps(self, apps: list[App]):
        # All apps must be deleted at once before the app ID is reset
        for app in apps:
            aprint(f"Deleting app '{app.name}'...  ", end="")
            self.__purge_app(app)
            print("Done\u2713")
            
        max_id = max([app.id for app in apps])
        self.__reset_apps_id(max_id)
    
    def __purge_app(self, app: App):
        try:
            app_dir = os.path.join(APPS_DIRECTORY, app.get_reformatted_app_name())
            shutil.rmtree(app_dir)
        except FileNotFoundError:
            raise AmiyaBaseException("Application directory does not exist or has already been deleted.")
        
        removed_value = self.apps.pop(app.id, None) 
        if removed_value == None: # If application cannot be found in self.apps
            raise AmiyaBaseException(f"App '{app.name}' can't be found in the apps dict.")
        
    def __reset_apps_id(self, max_id=0):
        self.apps = {new_app_id+1: app for new_app_id, (old_app_id, app) in enumerate(self.apps.items())}       # Reset app IDs
        for new_id, app in self.apps.items():                                                                   # Save each app's new config
            if new_id >= max_id:                                                                                # ONLY write config if the new ID is >= the max_ID of the application removed
                app.id = new_id
                app.save_app_config()
        time.sleep(1)
    
    # ======================================
    # =============| RUN APP | =============
    # ======================================
    def run_app(self, tag: str = None):
        self.__verify_non_empty_apps_dir()      # Verify that the apps dir is not empty
        
        app = None
        
        if tag == None:                         # If user did not provide a tag
            self.print_apps()
            user_input = input(atext(f"Which app would you like to run? (0-{len(self.apps)-1}) "))
            app = self.apps[int(user_input)]
        else:                                   # If user provided an application tag
            tag = self.__parse_tag(tag)
            app = self.get_app_by_tag(tag)
        
        self.__safe_start_app(app)
    
    
    def __safe_start_app(self, app: App):
        aprint(f"Starting application {app.name}...", end="\r")
        
        try:
            ret = app.run()
        except Amiya_AppInvalidPathException as ex:    # Application path invalid
            aprint(ex.message, log_type=LogType.ERROR); raise AmiyaExit()
        
        if ret == True:
            aprint(f"[PID {app.process.pid}] Application '{app.name}' started successfully!")
        else:
            aprint(f"Application '{app.name}' failed to start.", log_type=LogType.ERROR); raise AmiyaExit()
            
            
    # ======================================
    # ==========| TERMINATE APP | ==========
    # ======================================
    
    def __safe_terminate_current_app(self):
        pid = SafetyMonitor.get_focused_pid()
        
        try:
            app_process = psutil.Process(pid)
            app_name = app_process.name()
        except:
            aprint("Unable to terminate application because it is already closed.", log_type=LogType.ERROR); raise AmiyaExit()
        
        try:
            if app_process.is_running():
                app_parent_pid = app_process.ppid()                                 # Get current focused process' parent PID
                
                app_process.kill()                                                  # Terminate the app process
                aprint(f"Application `{app_name}` (PID {pid}) has been closed.")
                
                # if AMIYA_PID != app_parent_pid:                                     # Get PPID != module PID, kill parent PID (most likely a launcher of sort)
                #     time.sleep(3)
                #     success = ProcessHandler.kill_pid(app_parent_pid)

        except OSError as ex:
            aprint(f"Failed to terminate process with PID {pid}: {ex}", log_type=LogType.ERROR); raise AmiyaExit()


    # ======================================
    # ============| SHOW APPS | ============
    # ======================================

    def show_apps(self):
        self.__verify_non_empty_apps_dir()
        self.print_apps()


    # ======================================
    # ============| VIEW APPS | ============
    # ======================================
    def print_app(self, app: App, format="fancy_grid"):
        tabulated_apps = AppsViewer.tabulate_app(app, tablefmt=format)
        print(tabulated_apps)
    
    def print_apps(self, format="fancy_grid"):
        tabulated_apps = AppsViewer.tabulate_apps(self.apps, tablefmt=format)
        print(tabulated_apps)
        
    def print_apps_list(self, apps: list[App], format="fancy_grid"):
        tabulated_apps = AppsViewer.tabulate_apps_list(apps, tablefmt=format)
        print(tabulated_apps)
    
    def print_tags(self, app: App, format="fancy_grid"):
        tabulated_tags = AppsViewer.tabulate_tags(app.tags, tablefmt=format)
        print(tabulated_tags)
    
    
    # =======================================================
    # ============| ADD/REOVE TAGS TO/FROM APP | ============
    # =======================================================
    def add_tag(self):
        self.__verify_non_empty_apps_dir()
        
        def tag_exists(tag):
            try:
                self.get_app_by_tag(tag)
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
        app.save_app_config()
    
    def remove_tag(self):
        self.__verify_non_empty_apps_dir()
        
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
        app.save_app_config()
    
    def __parse_tag(self, tag: str):
        return tag.strip()
    
        
    # HELPER FUNCTIONS ======================
    def verbose_app_config(self, tag: str = None, show_all: bool = False):
        app = None
        if tag == None:                             # If no application tag is inputted by user
            self.print_apps()
            user_input = input(atext(f"Which app would you like to DELETE? (0-{len(self.apps)-1}) "))
            app = self.apps[int(user_input)]
        else:                                       # If user inputted an application tag tag
            tag = self.__parse_tag(tag)
            app = self.get_app_by_tag(tag)
            
        text = f"Application Configuration:"
        text += f"\nApp Name: {app.name}"
        text += f"\nApp ID: {app.id}"  
        text += f"\nApp Tags: {app.tags}"
        text += f"\nApp Config Directory: {app.app_config_dirpath}" 
        text += f"\nApp Executable Hash: {app.exe_hash}"
        text += f"\nApp Configuration System UUID: {app.sys_uuid}"  
        aprint(text)
        
    
    def __initial_setup(self):
        if not os.path.isdir(APPS_DIRECTORY):
            os.mkdir(APPS_DIRECTORY)
            
    def __get_next_app_id(self) -> int:
        return max(self.apps.keys()) + 1

    def get_app_with_id(self, user_input_id: str) -> App:
        try:
            app = self.apps[int(user_input_id)]
        except KeyError:
            aprint(f"Your input (ID {user_input_id}) does not correspond to any apps.", log_type=LogType.ERROR); raise AmiyaExit()
        except ValueError:
            aprint(f"Expected an ID (such as 0 or 1) but got '{user_input_id}'.", log_type=LogType.ERROR); raise AmiyaExit()
        return app
    
    def get_app_by_tag(self, tag) -> App:
        for _, app in self.apps.items():
            if tag in app.tags:
                return app
        raise Amiya_NoSuchTagException(tag)
            
    def __verify_non_empty_apps_dir(self):
        if len(self.apps) == 0:
            cmd = color_cmd("amiya add-app")
            aprint(f"No application is configured. To add/configure an application, run `{cmd}`")
            raise AmiyaExit()
    
      
    # =====================================================================================================================================
    # >>>>> AUTOMATION RELATED
    
    # =================================================
    # ===============| LIST SEQUENCES | ===============
    # =================================================
    def list_sequences(self, tag: str = None):
        self.__verify_non_empty_apps_dir()
        
        if tag != None:
            tag = self.__parse_tag(tag)
            app = self.get_app_by_tag(tag)
        else:
            self.print_apps()
            user_input_id = input(atext(f"Which app would you like to see the automation sequences of? (0-{len(self.apps)-1}) "))
            app = self.get_app_with_id(user_input_id)
        
        sequence_list = app.automation_controller.get_all_sequences()
        self.__print_sequences(sequence_list)

    
    # =================================================
    # ==============| RECORD SEQUENCES | ==============
    # =================================================
    def record_sequence(self, tag: str = None):
        self.__verify_non_empty_apps_dir()
        
        if tag != None:
            tag = self.__parse_tag(tag)
            app = self.get_app_by_tag(tag)
        else:
            self.print_apps()
            user_input_id = input(atext(f"Which app would you like to RECORD A NEW AUTOMATION SEQUENCE of? (0-{len(self.apps)-1}) "))
            app = self.get_app_with_id(user_input_id)
        
        new_sequence_name = input(atext(f"Name of the new automation sequence (i.e. start-game): "))
        self.__start_app_and_record(app, new_sequence_name)
    
    def __start_app_and_record(self, app: App, new_sequence_name: str):
        self.__safe_start_app(app)
        safety_monitor = SafetyMonitor(app.process)
        
        new_sequence_recorded = app.automation_controller.record_sequence(
            new_sequence_name, 
            safety_monitor
        )
        self.__print_sequence(new_sequence_recorded)
        

    # =================================================
    # ================| RUN SEQUENCES | ===============
    # =================================================
    def run_sequence(
        self, tag: str = None, 
        seq_name: str = None, 
        global_delay: int = 0, 
        terminate_on_finish: bool = False, 
        no_confirmation: bool = False,
        sleep_afterward: bool = False,
        shutdown_afterward: bool = False
    ):
        self.__verify_non_empty_apps_dir()
        
        if tag != None:
            tag = self.__parse_tag(tag)
            app = self.get_app_by_tag(tag)
        else:
            self.print_apps()
            user_input_id = input(atext(f"Which app would you like to RUN AN AUTOMATION SEQUENCE of? (0-{len(self.apps)-1}) "))
            app = self.get_app_with_id(user_input_id)
        
        # ================ GET SEQUENCE ================
        sequence_list = app.automation_controller.get_all_sequences()
        
        if seq_name == None:
            self.__print_sequences(sequence_list)                             # Verbose all sequences in the CLI and wait for user selection
            seq_name = input(atext(f"Which sequence would you like to run (i.e. start-game)? "))
        sequence: AutomationSequence = self.__safe_get_sequence(app, seq_name)
        
        # ============== GET GLOBAL DELAY ==============
        global_delay = 0
        if global_delay == -1:                                                # If global_delay == -1, then the argument -g is used but no time is specified (in entrypoints.py)
            aprint(f"Add global delay to all actions (seconds) [leave empty to default to 0]: ", end="")
            user_input = input().lower().strip()
            if user_input:
                global_delay = self.__parse_int(user_input)                   # If user inputted global delay
        sequence.set_global_delay(global_delay)
        
        # ============== RUN CONFIRMATION ==============
        if not no_confirmation:
            terminate_text = " Terminate on finish." if terminate_on_finish else ""
            aprint(f"The sequence '{sequence.sequence_name}' will run for {sequence.get_runtime()} seconds.{terminate_text} Continue? [y/n] ", log_type=LogType.WARNING, end="")
            if input().lower() != "y": return                                  # Verbose runtime and wait for user confirmation to run
        
        # =============== START RUNNING ===============
        aprint(f"[Automation {sequence.sequence_name}] Running...")
        self.__safe_start_app(app);                                            # Starts the application for the sequence
        app_process = app.get_app_process()                                    # Get application's process
        safety_monitor = SafetyMonitor(app_process)                            # Creates a safety monitor object for sequence execution safety (must be created after the app is started)
        self.__safe_execute_sequence(sequence, safety_monitor)                 # Runs the sequence (with the safety monitor)

        print("")
        aprint(f"[Automation {sequence.sequence_name}] Run Completed!", log_type=LogType.SUCCESS)
        
        # ============== AFTER FINISHING ==============
        if terminate_on_finish:
            self.__safe_terminate_current_app()
        
        if sleep_afterward:
            power_utils = PowerUtils()
            power_utils.sleep_pc(delay=10)
        elif shutdown_afterward:
            power_utils = PowerUtils()
            power_utils.shutdown_pc(delay=10)
            
        
    def __safe_execute_sequence(self, sequence: AutomationSequence, safety_monitor: SafetyMonitor):
        try:
            sequence.execute(safety_monitor)
        except Amiya_AppNotFocusedException:
            aprint("[Safety-Monitor] The application is unfocused during an automation run. Automation terminated.", log_type=LogType.ERROR)
            raise AmiyaExit()
     
    def __safe_get_sequence(self, app: App, sequence_name: str) -> AutomationSequence:
        sequence = app.automation_controller.get_sequence(sequence_name)
        if sequence == None:
            aprint(f"No sequence with name '{sequence_name}' exists. Exiting.", log_type=LogType.ERROR); raise AmiyaExit()
        return sequence

    def __parse_int(self, delay) -> int:
        if isinstance(delay, int):
            return delay
        
        if isinstance(delay, str):
            try:
                return int(delay.strip())
            except ValueError:
                aprint("Please input an integer as the delay."); raise AmiyaExit()
        
        raise AmiyaBaseException(f"Type {type(delay)} ({delay}) delay not supported.")
    
    
    # ===================================================
    # ================| SEQUENCE HELPER | ===============
    # ===================================================
    def __print_sequences(self, sequence_list: list[AutomationSequence], tablefmt="fancy_grid"):
        if len(sequence_list) == 0:
            aprint("No Sequence Recorded For Application."); return
        
        viewer = AutomationViewer()
        print(viewer.tabulate_multi_sequences(sequence_list, tablefmt))
    
    def __print_sequence(self, sequence: AutomationSequence, tablefmt="fancy_grid"):
        viewer = AutomationViewer()
        print(viewer.tabulate_sequence(sequence, tablefmt))
    
    

    
    # =====================================================================================================================================
    # >>>>> UTILITY APP FUNCTIONS
    
    # =================================================
    # ==================| SYNC APPS | =================
    # =================================================
    
    def sync_apps(self, verbose=True):
        self.__verify_non_empty_apps_dir()
        
        if verbose:
            aprint(f"Sync {len(self.apps)} applications on this machine? (This may take a while) [y/n] ", log_type=LogType.WARNING, end="")
            if input().strip().lower() != "y": return
        
        sync_controller = AppSyncController()

        apps = list(self.apps.values())
        for app in apps:
            aprint(f"Syncing application `{app.name}`... ", end="")
            synced_app = sync_controller.sync(app)
            self.apps[app.id] = synced_app
            print("Done")
        self.print_apps()
        
        found = len([app for app in self.apps.values() if app.verified == True])
        cmd = color_cmd("amiya cleanup")
        aprint(f"Sync Complete - successfully synced {found}/{len(apps)} applications.\n\nTo cleanup unverified applications (unavailable on this machine), run '{cmd}'\n")
        
    def verify_apps_synced(self) -> bool: 
        # Verify whether applications configured with Amiya's apps manager needs to be synced with the current machine.
        # Sync is only required when transferring the apps manager's configuration data (apps) on to a new machine.
        for app in self.apps.values():
            if SYSTEM_UUID != app.sys_uuid:
                aprint(f"App not synced: {app.name} ({app.sys_uuid})")
                return False
        return True
        
    def cleanup_apps(self):
        unverified_apps = [app for app in self.apps.values() if app.verified == False]
        if len(unverified_apps) == 0:
            aprint('There is no unverified application to cleanup!'); return
        self.print_apps_list(unverified_apps)
        
        aprint(f"Are you sure you want to remove all these unverified apps? [y/n] ", log_type=LogType.WARNING, end="")
        if input().strip().lower() != "y": return
        
        self.__safe_delete_multiple_apps(unverified_apps)
        aprint("Cleanup Complete.", log_type=LogType.SUCCESS)
        
        
        
    # =====================================================================================================================================
    # >>>>> SCHEDULER FUNCTIONS
    
    # def sequence_exists(self, app: App, sequence_name: str):
    #     sequences: list[AutomationSequence] = []
    #     sequences = app.automation_controller.load_all_sequences()
    #     self.get_sequence_with_name(sequence_name, sequences)
    
            
        