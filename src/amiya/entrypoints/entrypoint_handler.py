import multiprocessing

from amiya.apps_manager.apps_manager import AppsManager 
from amiya.exceptions.exceptions import *
from amiya.utils.helper import *
from amiya.module_utilities.search_controller import SearchController
from amiya.module_utilities.power_controller import PowerUtils
from amiya.scheduler.scheduler import AmiyaScheduler
from amiya.apps_manager.sync_controller.sys_uuid_controller import SysUUIDController
from amiya.utils import constants
from amiya.utils.constants import VERSION, VERSION_DESC, AUTHOR, AUTHOR_DETAIL, REPOSITORY
from amiya.module_utilities.volume_controller import AmiyaVolumeControllerUI, start_volume_control_ui



class AmiyaEntrypointHandler:
    def __init__(self):
        self.apps_manager = AppsManager()
        self.search_controller = SearchController()
        self.power_utils = PowerUtils()
        # self.scheduler = AmiyaScheduler()

    
    # =================================================
    # ====================| ABOUT | ===================
    # =================================================
    
    def version(self, args):
        aprint(f"Amiya {VERSION_DESC}-{VERSION}")
    
    def author(self, args):
        aprint(AUTHOR_DETAIL)
    
    def repo(self, args):
        aprint(REPOSITORY)
    
    # =================================================
    # ============| ADD/REMOVE/SHOW APPS | ============
    # =================================================
    
    def add_app(self, args):
        self.apps_manager.create_app_automated()
    
    def remove_app(self, args):
        self.apps_manager.delete_app(args.tag)
    
    def show_apps(self, args):
        self.apps_manager.show_apps()
    
    def show_app_config_dir(self, args):
        self.apps_manager.verbose_app_config(args.tag)
    
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
        self.apps_manager.list_sequences(args.tag)

    def record_automation_sequences(self, args):
        self.apps_manager.record_sequence(args.tag)

    def run_automations_sequences(self, args):
        self.apps_manager.run_sequence(
            tag=args.tag, 
            seq_name=args.seq_name,
            add_global_delay=args.add_global_delay,
            terminate_on_finish=args.terminate
        )


    # =================================================
    # ==========| APP UTILITY FEATURES | ==============
    # =================================================

    def sync(self, args):
        self.apps_manager.sync_apps()
        
        
    def cleanup(self, args):
        self.apps_manager.cleanup_apps()
        
    # Blocking function
    def apps_synced(self):
        return self.apps_manager.verify_apps_synced()

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

    def display_system_uuid(self, args):
       SysUUIDController.print_uuid()

    def open_volume_control_ui(self, args):
        # A new process is used because on closing the UI, a whole bunch of nonsense if printed 
        # in stdout (only happens when using this as an module entrypoint apparantly)
        gui_process = multiprocessing.Process(target=start_volume_control_ui)
        gui_process.start()
        gui_process.join()
    

    # =================================================
    # ================| SCHEDULER | ===================
    # =================================================

    # def run_scheduler(self, args):
    #     self.scheduler.run_scheduler()

    # =================================================
    # ===============| OTHER HELPER | =================
    # =================================================
    
    def print_title(self):
        
        # columns, _ = shutil.get_terminal_size(fallback=(80, 20))
        # bar = '▬' * (columns//1 - 12)
        # bar = Printer.to_lightblue(f"▷ ▷ ▷ {bar} ◁ ◁ ◁")
        # print(bar)
        
        title = Printer.to_lightblue(
r"""
    _    __  __ _____   __ _       ____ _     ___  
   / \  |  \/  |_ _\ \ / // \     / ___| |   |_ _| 
  / _ \ | |\/| || | \ V // _ \   | |   | |    | |  
 / ___ \| |  | || |  | |/ ___ \  | |___| |___ | |  
/_/   \_\_|  |_|___| |_/_/   \_\  \____|_____|___|
""")
        
        desc = Printer.to_purple("""A lightweight cross-platform automation tool for games and daily tasks!""")
        postfix = Printer.to_lightgrey(REPOSITORY)
        author = Printer.to_lightgrey(f"By {AUTHOR}")
        
        print(center_text(title))
        print_centered(f"{desc}\n{postfix}\n{author}\n")
    
    def print_init_help(self):
        
        access_time = colored(f"Access Time: {DatetimeHandler.get_datetime_str()}", "dark_grey")
        
        quit_cmd = Printer.to_purple("exit")
        cls_cmd = Printer.to_purple("clear")
        help_cmd = Printer.to_purple("help")
        
        welcome_str = f"Welcome to the Amiya CLI Environment ({VERSION_DESC}-{VERSION})"
        exit_str = f"Type '{quit_cmd}' to quit amiya CLI"
        cls_str = f"Type '{cls_cmd}' to clear terminal"
        help_str = f"Type '{help_cmd}' to display commands list"
    
        print(f"{welcome_str}\n  {help_str}\n  {exit_str}\n  {cls_str}\n")
    
        
    # =================================================
    # ===============| CLI DRIVERS | ==================
    # =================================================
    
    def check_custom_commands(self, user_input: str):
        # Return 0 to continue loop, 1 to short-circit loop and 'continue' loop, 2 to exit loop

        if user_input.lower() in ['exit', 'quit']:
            clear_screen()
            return 2
        
        if user_input.lower() in ['clear', "cls", "reset"]:
            clear_screen()
            self.print_title()
            print("Terminal cleared. Type 'exit' to quit.")
            return 1
        
        if user_input.strip() == '':
            return 1
    
        return 0
    
    import argparse
    def start_cli(self, parser: argparse.ArgumentParser):
        
        # =============| SET CLI MODE |==============
        constants.CLI_MODE = True
        
        # ==============| PRINT TITLE |==============
        clear_screen()
        self.print_title()
        self.print_init_help()
        
        # ================| CLI LOOP |================
        while True:
            try:
                amiya_cli = colored(f"{DatetimeHandler.get_time_str()} Amiya-CLI", "dark_grey")
                print(f"[{amiya_cli}] > ", end="", flush=True)
                
                user_input = input().strip()
                continue_loop = self.check_custom_commands(user_input)
                if continue_loop == 1:
                    continue
                elif continue_loop == 2:
                    break
                
                
        # =============| PARSE ARGUMENT |=============    
                args = parser.parse_args(user_input.split())
                if hasattr(args, 'func'):
                    try:
                        args.func(args)
                    except AmiyaExit:
                        continue
                else:
                    parser.print_help()
            
            
        # ==============| ON EXCEPTION |==============
            except KeyboardInterrupt:
                # print("\nNote: Type 'exit' to quit.")
                print("")
                continue
            except SystemExit:
                continue
