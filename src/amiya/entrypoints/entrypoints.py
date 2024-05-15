import sys
import time
import psutil
import argparse
from termcolor import colored
from amiya.entrypoints.entrypoint_handler import AmiyaEntrypointHandler
from amiya.utils.helper import aprint, verify_platform, is_admin, Printer
from amiya.exceptions.exceptions import AmiyaOSNotSupported, AmiyaExit


class AmiyaArgParser(argparse.ArgumentParser):
    def error(self, message):
        command = message.split("'")[1] if "invalid choice:" in message else None
        helpt = Printer.to_purple("help")
        aprint(f"Command not recognized: {command}\nType '{helpt}' for commands list")
        self.exit(2)
        

def start_amiya():
    entrypoint_handler = AmiyaEntrypointHandler()
    
    parser = AmiyaArgParser(prog='amiya', description="Amiya CLI Automation Package")
    subparsers = parser.add_subparsers(dest='command', help='commands')

    help_parser = subparsers.add_parser('help', help='Show this help message and exit')
    help_parser.set_defaults(func=lambda args: entrypoint_handler.print_help(args, parser))

    # =================================================
    # =================| DEVELOPMENT | ================
    # =================================================

    start_parser = subparsers.add_parser('dev', help='[DEV] Developer\'s commands.')
    start_parser.add_argument('--objects', '-obj', action='store_true', help='Show all controller objects and their addresses.')
    start_parser.add_argument('--refresh', '-ref', action='store_true', help='Refresh all controller objects.')
    start_parser.add_argument('--code', '-c', action='store_true', help='Open development environment with VSCode.')
    start_parser.add_argument('--isadmin', '-ia', action='store_true', help='Show whether the main thread has admin access.')
    start_parser.set_defaults(func=entrypoint_handler.DEV)


    # =================================================
    # ====================| ABOUT | ===================
    # =================================================

    start_parser = subparsers.add_parser('version', help='Verbose module version')
    start_parser.set_defaults(func=entrypoint_handler.version)
                              
    start_parser = subparsers.add_parser('author', help='Verbose module author')
    start_parser.set_defaults(func=entrypoint_handler.author)
    
    start_parser = subparsers.add_parser('repo', help='Verbose module repository link')
    start_parser.set_defaults(func=entrypoint_handler.repo)

    # =================================================
    # ============| ADD/REMOVE/SHOW APPS | ============
    # =================================================

    start_parser = subparsers.add_parser('add-app', help='Add a new application')
    start_parser.set_defaults(func=entrypoint_handler.add_app)
    
    start_parser = subparsers.add_parser('remove-app', help='Remove an existing application')
    start_parser.add_argument('tag', nargs='?', default=None, help='Tag of the application to remove')
    start_parser.set_defaults(func=entrypoint_handler.remove_app)
    
    show_apps_parser = subparsers.add_parser('show-apps', help='Show applications')
    show_apps_parser.add_argument('--short', '-s', action='store_true', help='Only show the app ID, name, and verification status')
    show_apps_parser.add_argument('--full-path', '-f', action='store_true', help='Show the full path of the applications')
    show_apps_parser.set_defaults(func=entrypoint_handler.show_apps)


    start_parser = subparsers.add_parser('show-config', help='Show application configuration directory')
    start_parser.add_argument('tag', nargs='?', default=None, help='Tag of the application to show the configuration directory of')
    start_parser.add_argument('--all', '-a', action='store_true', help='Show all configuration directory paths (including automation)')
    start_parser.set_defaults(func=entrypoint_handler.show_app_config_dir)

    # =================================================
    # =================| START APPS | =================
    # =================================================
    
    start_parser = subparsers.add_parser('start', help='Start an application')
    start_parser.add_argument('tag', nargs='?', default=None, help='Tag of the application to start')
    start_parser.set_defaults(func=entrypoint_handler.start)
    
    
    # =================================================
    # ==============| ADD/REMOVE TAGS | ===============
    # =================================================
    
    start_parser = subparsers.add_parser('add-tag', help='Add a new tag to an application')
    start_parser.set_defaults(func=entrypoint_handler.add_tag)
    
    start_parser = subparsers.add_parser('remove-tag', help='Remove a tag from an application')
    start_parser.set_defaults(func=entrypoint_handler.remove_tag)
    
    
    # =================================================
    # ========| RECORD/LIST/RUN AUTOMATION |===========
    # =================================================
    
    start_parser = subparsers.add_parser('list-auto', help='List all the automation sequences of the application')
    start_parser.add_argument('tag', nargs='?', default=None, help='Tag of the application')
    start_parser.set_defaults(func=entrypoint_handler.list_automation_sequences)
    
    start_parser = subparsers.add_parser('record-auto', help='[Admin Permission Req.] Record an automation sequences of the application')
    start_parser.add_argument('tag', nargs='?', default=None, help='Tag of the application')
    start_parser.set_defaults(func=entrypoint_handler.record_automation_sequences)

    
    start_parser = subparsers.add_parser('run-auto', help='[Admin Permission Req.] Record an automation sequences of the application')
    start_parser.add_argument('tag', nargs='?', default=None, help='Tag of the application')
    start_parser.add_argument('seq_name', nargs='?', default=None, help='Name of the sequence to run')
    start_parser.add_argument('--global-delay', '-g', type=int, default=-1, help='Add a global delay to the sequence during execution')
    start_parser.add_argument('--terminate', '-t', default=False, action='store_true', help='Terminate the application on automation completion')
    start_parser.add_argument('--no-confirmation', '-nc', default=False, action='store_true', help='Run the automation without confirmation')
    start_parser.set_defaults(func=entrypoint_handler.run_automations_sequences)
    
    
    # =================================================
    # ==========| APP UTILITY FEATURES | ==============
    # =================================================
    
    start_parser = subparsers.add_parser('sync', help='Sync configured applications on new machine OR auto configure application executable paths')
    start_parser.set_defaults(func=entrypoint_handler.sync)
    
    start_parser = subparsers.add_parser('cleanup', help='Remove all unverified applications')
    start_parser.set_defaults(func=entrypoint_handler.cleanup)
    
    
    # =================================================
    # =============| UTILITY FEATURES | ===============
    # =================================================
    
    start_parser = subparsers.add_parser('search', help='Initiate a search on the default browser')
    start_parser.add_argument('search_content', nargs='*', default=None, help='Content of the search')
    start_parser.set_defaults(func=entrypoint_handler.search)
    
    sleep_parser = subparsers.add_parser('sleep', help='Put the PC to sleep after X seconds')
    sleep_parser.add_argument('delay', nargs='?', type=int, default=0, help='Delay in seconds before sleep')
    sleep_parser.set_defaults(func=lambda args: entrypoint_handler.sleep(args, sleep_parser))
    
    shutdown_parser = subparsers.add_parser('shutdown', help='Shutdown PC after X seconds')
    shutdown_parser.add_argument('delay', nargs='?', type=int, default=0, help='Delay in seconds before shutdown')
    shutdown_parser.set_defaults(func=lambda args: entrypoint_handler.shutdown(args, shutdown_parser))
    
    
    start_parser = subparsers.add_parser('uuid', help='Display system UUID')
    start_parser.set_defaults(func=entrypoint_handler.display_system_uuid)
    
    
    start_parser = subparsers.add_parser('pixel', help='Track cursor position and color')
    start_parser.add_argument('--color', '-c', action='store_true', help='Show pixel coordinate as well as the pixel\'s color hex value.')
    start_parser.set_defaults(func=entrypoint_handler.track_cursor)
    
    
    start_parser = subparsers.add_parser('volume', help='Open simple application volume control UI')
    start_parser.set_defaults(func=entrypoint_handler.open_volume_control_ui)
    
    start_parser = subparsers.add_parser('click', help='Continuously click mouse.')
    start_parser.add_argument('--count', '-c', type=int, default=-1, help='Number of clicks. Leave empty (default) to run forever')
    start_parser.add_argument('--delay', '-d', type=int, default=1, help=' Delay (second) between clicks')
    start_parser.add_argument('--hold-time', '-ht', type=int, default=0.1, help='Delay (second) between click press and release')
    start_parser.add_argument('--start-after', '-sa', type=int, default=3, help='Delay (second) before the clicks start')
    start_parser.add_argument('--quite', '-q', action="store_true", default=False, help='Run without verbosing progress')
    start_parser.set_defaults(func=entrypoint_handler.click_continuously)
    
    # =================================================
    # ================| SCHEDULER | ===================
    # =================================================
    
    # start_parser = subparsers.add_parser('run-scheduler', help='Start and run the scheduler')
    # start_parser.set_defaults(func=entrypoint_handler.run_scheduler)
    
    
    
    # ===========================================================================================
    # >>> BLOCKING FUNCTIONS
    # ===========================================================================================
    if verify_platform() == False:
        raise AmiyaOSNotSupported()
    
    
    sync_needed = not entrypoint_handler.apps_synced()
    if sync_needed:
        # If sync is needed, restrict all commands except 'sync'
        def blocked_func(args):
            text = colored('amiya sync', 'light_cyan')
            aprint(f"Applications under Amiya's apps manager are not fully configured to run on this machine.\n\nTo sync the apps to this machine, run `{text}`")
            raise AmiyaExit()

        for name, subparser in subparsers.choices.items():
            if name not in ["sync", "search", "sleep", "shutdown", "uuid", "show-config", "version", "author", "repo"]:
                subparser.set_defaults(func=blocked_func)
    
    
    isadmin = is_admin()
    if not isadmin:
        # Certain commands require admin permissions to execute
        def blocked_func(args):
            aprint("Insufficient permission. Please restart the terminal as an administrator.")
            raise AmiyaExit()

        for name, subparser in subparsers.choices.items():
            if name in ["record-auto", "run-auto"]:
                subparser.set_defaults(func=blocked_func)
    
    # ===========================================================================================
    # >>> PARSER DRIVER
    # ===========================================================================================
    
    # Check if no command line arguments are provided
    if len(sys.argv) == 1:
        entrypoint_handler.start_cli(parser)
    else:
        # Normal command line execution
        args = parser.parse_args()
        if hasattr(args, 'func'):
            try:
                args.func(args)
            except KeyboardInterrupt:
                print("\nKeyboard Interrupt! Amiya Exiting.")
            except AmiyaExit:
                exit()
        else:
            parser.print_help()