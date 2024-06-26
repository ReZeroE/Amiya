import multiprocessing
import getpass
import subprocess
import argparse
import readline

from amiya.apps_manager.apps_manager import AppsManager
from amiya.module_utilities.search_controller import SearchController
from amiya.module_utilities.power_controller import PowerUtils
from amiya.module_utilities.cursor_controller import CursorController
from amiya.module_utilities.continuous_click_controller import ContinuousClickController
from amiya.module_utilities.url_tracker import URLTracker
from amiya.module_utilities.dev_features import DevController
from amiya.module_utilities.internet_speed import InternetSpeedTest

from amiya.raw_automation_manager.raw_auto_manager import RawAutoManager

from amiya.exceptions.exceptions import *
from amiya.utils.helper import *

from amiya.scheduler.scheduler import AmiyaScheduler
from amiya.apps_manager.sync_controller.sys_uuid_controller import SysUUIDController
from amiya.utils import constants
from amiya.utils.constants import COMMAND, VERSION, VERSION_DESC, AUTHOR, AUTHOR_DETAIL, REPOSITORY
from amiya.module_utilities.volume_controller import AmiyaVolumeControllerUI, start_volume_control_ui


class AmiyaEntrypointHandler:
    def __init__(self):
        self.apps_manager       = AppsManager()
        self.raw_auto_manager   = RawAutoManager()
        self.search_controller  = SearchController()
        self.power_utils        = PowerUtils()
       
        # self.scheduler = AmiyaScheduler()


    # =================================================
    # =================| DEVELOPMENT | ================
    # =================================================

    def DEV(self, args):
        # If "DEVELOPMENT" variable in constants is False, the dev controller cannot be created.
        self.dev_controller = DevController()
        
        if args.objects:
            self.dev_controller.verbose_objects(
                self.apps_manager,
                self.search_controller,
                self.power_utils
            )
        if args.refresh:
            self.dev_controller.refresh_objects()
        if args.code:
            self.dev_controller.open_dev_env()
        if args.isadmin:
            self.dev_controller.is_admin()
        if args.home_dir:
            self.dev_controller.verbose_home_dir()
    
    
    # =================================================
    # ====================| ABOUT | ===================
    # =================================================
    
    def version(self, args):
        aprint(f"Amiya {VERSION_DESC}-{VERSION}")
    
    def author(self, args):
        aprint(AUTHOR_DETAIL)
    
    def repo(self, args):
        aprint(REPOSITORY)
    
    # def print_help(self, args, parser):
    #     # help_cmd = color_cmd("help", with_quotes=True)
    #     # aprint(f"Command {help_cmd} is not implemented.")
        
    #     parser.print_help()
        

    
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
            global_delay=args.global_delay,
            terminate_on_finish=args.terminate,
            no_confirmation=args.no_confirmation,
            sleep_afterward=args.sleep,
            shutdown_afterward=args.shutdown
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
        self.power_utils.sleep_pc(args.delay)
    
    def shutdown(self, args, parser):
        self.power_utils.shutdown_pc(args.delay)

    def display_system_uuid(self, args):
       SysUUIDController.print_uuid()

    def open_volume_control_ui(self, args):
        # A new process is used because on closing the UI, a whole bunch of nonsense if printed 
        # in stdout (only happens when using this as an module entrypoint apparantly)
        gui_process = multiprocessing.Process(target=start_volume_control_ui)
        gui_process.start()
        gui_process.join()
    
    def track_cursor(self, args):
        if args.color:
            self.cursor_controller = CursorController(verbose_hex=True)
        else:
            self.cursor_controller = CursorController(verbose_hex=False)
        
        self.cursor_controller.track_cursor()

    def click_continuously(self, args):
        cc_controller = ContinuousClickController()
        cc_controller.click_continuously(args.count, args.interval, args.randomize_by, args.hold_time, args.start_after, args.quiet)

    def elevate(self, args):
        if is_admin():
            aprint("Already running as admin.")
            return
        
        if args.explain:
            text = """Certain applications requires the 'amiya' process to have admin 
privileges to replay or record mouse and keyboard actions. To help with this, 
the 'elevate' command is available to elevate amiya's permissions to an 
administrative level.

By invoking the elevate command, you are granting `amiya` admin access.
"""
            aprint(text)
            ui = input(atext("Proceed to elevate? [y/n] "))
            if ui.lower() != "y":
                return
        
        script = os.path.abspath(sys.argv[0])
        params = ' '.join([script])
        try:
            # \k keeps the terminal open after the user exits the amiya cli env
            cmd_command = f'cmd /k "{COMMAND}"'
            result = subprocess.run(["powershell", "-Command", f'Start-Process cmd -ArgumentList \'/k {cmd_command}\' -Verb RunAs'])
            
            if result.returncode == 0:
                aprint("Permissions granted. Please use the new terminal with the Amiya-CLI that opened.")
            else:
                aprint(f"Command 'amiya elevate' permission denied.", log_type=LogType.ERROR)
            
            # subprocess.run(["powershell", "-Command", f"Start-Process -Verb runAs {params}"])
            
        except Exception as e:
            aprint(f"Failed to elevate privileges: {e}")
        raise AmiyaExit()

    def track_url(self, args):
        url_monitor = URLTracker()
        url_monitor.safe_track_changes(args.url, args.interval, args.open)

    def internet_speed_test(self, args):
        aprint("Command internet-speed is still in development.", LogType.WARNING)
        if DEVELOPMENT:
            InternetSpeedTest.run()


    # =================================================
    # ================| SCHEDULER | ===================
    # =================================================

    # def run_scheduler(self, args):
    #     self.scheduler.run_scheduler()
    
    
    # =================================================
    # =============| RAW AUTOMATIONS | ================
    # =================================================
    
    def testrawauto(self, args):
        assert(self.raw_auto_manager.raw_sequences_dict != None)

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
        username = getpass.getuser()
        isadmin = "ADMIN" if is_admin() else "USER"
        
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
            
            exit_cmd = color_cmd("exit", with_quotes=True)
            print(f"Terminal cleared. Type {exit_cmd} to quit.")
            return 1
        
        if user_input.strip() == '':
            return 1
    
        return 0
    

    def setup_key_bindings(self):
        readline.parse_and_bind(r'"\C-w": backward-kill-word')
        readline.parse_and_bind(r'"\C-a": beginning-of-line')
        readline.parse_and_bind(r'"\C-e": end-of-line')
        readline.parse_and_bind(r'"\C-u": unix-line-discard')
        readline.parse_and_bind(r'"\C-k": kill-line')
        readline.parse_and_bind(r'"\C-y": yank')
        readline.parse_and_bind(r'"\C-b": backward-char')
        readline.parse_and_bind(r'"\C-f": forward-char')
        readline.parse_and_bind(r'"\C-p": previous-history')
        readline.parse_and_bind(r'"\C-n": next-history')
        readline.parse_and_bind(r'"\C-b": backward-word')
        readline.parse_and_bind(r'"\C-f": forward-word')


    def start_cli(self, parser: argparse.ArgumentParser):
        
        # =============| SET CLI MODE |==============
        constants.CLI_MODE = True
        
        
        # ============| SETUP READLINE |=============
        self.setup_key_bindings()

        
        # ==============| PRINT TITLE |==============
        clear_screen()
        self.print_title()
        self.print_init_help()
        
        cli_env_alert = False
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
                
                # Verify that the stdout and stderr aren't closed
                if sys.stdout.closed or sys.stderr.closed:
                    text = "STDOUT and STDERR" if sys.stdout.closed and sys.stderr.closed \
                        else "STDOUT" if sys.stdout.closed \
                        else "STDERR"
                    aprint(f"System {text} has been closed unexpectedly. Exiting Amiya CLI environment...")
                    sys.exit()
                
                # =============| PARSE ARGUMENT |=============
                if user_input.startswith(COMMAND):
                    user_input = user_input.lstrip(COMMAND).strip() 
                    
                    if not cli_env_alert:
                        aprint(Printer.to_lightgrey(f"Currently in the Amiya CLI environment. You may call `{user_input}` directly without the `amiya` prefix."))
                        cli_env_alert = not cli_env_alert
                    
                args = parser.parse_args(user_input.split())
                if hasattr(args, 'func'):
                    try:
                        args.func(args)
                    except AmiyaExit:
                        continue
                    # except Exception as ex:
                    #     aprint(f"{type(ex)}: {ex}. Exiting...", log_type=LogType.ERROR)
                    #     exit()
                else:
                    parser.print_help()
            
        # ==============| ON EXCEPTION |==============
            except KeyboardInterrupt:
                # print("\nNote: Type 'exit' to quit.")
                print("")
                continue
            except SystemExit:
                continue