from amiya.apps_manager.apps_manager import AppsManager 
from amiya.exceptions.exceptions import *
from amiya.utils.helper import *
from amiya.module_utilities.search_controller import SearchController
from amiya.module_utilities.power_controller import PowerUtils

class AmiyaEntrypointHandler:
    def __init__(self):
        self.apps_manager = AppsManager()
        self.search_controller = SearchController()
        self.power_utils = PowerUtils()

    
    # =================================================
    # ============| ADD/REMOVE/SHOW APPS | ============
    # =================================================
    
    def add_app(self, args):
        self.apps_manager.create_app_automated()
    
    def remove_app(self, args):
        self.apps_manager.delete_app(args.tag)
    
    def show_apps(self, args):
        if args.with_tag:
            aprint("With tag")
        elif args.all:
            aprint("with all")
        else:
            self.apps_manager.print_apps()
    
    
    # =================================================
    # =================| START APPS | =================
    # =================================================
    
    def start(self, args):
        self.apps_manager.run_app(args.tag)
            
           
    # =================================================
    # ==============| ADD/REMOVE TAGS | ===============
    # =================================================
     
    def add_tag(self, args):
        self.apps_manager.add_tag()
        
    def remove_tag(self, args):
        self.apps_manager.remove_tag()


    # =================================================
    # ========| RECORD/LIST/RUN AUTOMATION |===========
    # =================================================

    def list_automation_sequences(self, args):
        if args.tag:
            self.apps_manager.list_sequences_with_tag(args.tag)
        else:
            self.apps_manager.list_sequences()

    def record_automation_sequences(self, args):
        if args.tag:
            self.apps_manager.record_sequence_with_tag(args.tag)
        else:
            self.apps_manager.record_sequence()

    def run_automations_sequences(self, args):
        print("Elevating...")
        from elevate import elevate; elevate()
        if args.tag:
            if args.seq_name:
                self.apps_manager.run_sequence_with_tag(args.tag, args.seq_name)
            else:
                self.apps_manager.run_sequence_with_tag(args.tag)
        else:
            self.apps_manager.run_sequence()


    # =================================================
    # =============| UTILITY FEATURES | ===============
    # =================================================

    def search(self, args):
        if args.search_content:
            self.search_controller.search(args.search_content)
        else:
            self.search_controller.search_automated()

    def sleep(self, args, parser):
        if args.delay:
            self.power_utils.sleep_pc(args.delay)
        else:
            parser.print_help()
    
    def shutdown(self, args, parser):
        if args.delay:
            self.power_utils.shutdown_pc(args.delay)
        else:
            parser.print_help()


    # =================================================
    # ===============| OTHER HELPER | =================
    # =================================================
    def print_help(self, parser):
        print_centered(
r'''
       _    __  __ _____   __ _       ____ _     ___  
      / \  |  \/  |_ _\ \ / // \     / ___| |   |_ _| 
     / _ \ | |\/| || | \ V // _ \   | |   | |    | |  
    / ___ \| |  | || |  | |/ ___ \  | |___| |___ | |  
   /_/   \_\_|  |_|___| |_/_/   \_\  \____|_____|___| 
  
A lightweight cross-platform automation tool for daily tasks!
              https://github.com/ReZeroE/Amiya
                        By Kevin L.
''')
        
        parser.print_help()


