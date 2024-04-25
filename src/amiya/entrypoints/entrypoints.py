import sys
import time
import psutil
import argparse
from termcolor import colored
from amiya.entrypoints.entrypoint_handler import AmiyaEntrypointHandler
from amiya.utils.helper import aprint


def execute_command():
    entrypoint_handler = AmiyaEntrypointHandler()
    
    parser = argparse.ArgumentParser(prog='amiya', description="Amiya CLI Automation Package")
    subparsers = parser.add_subparsers(dest='command', help='commands')

    help_parser = subparsers.add_parser('help', help='Show this help message and exit')
    help_parser.set_defaults(func=lambda args: entrypoint_handler.print_help(parser))


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
    
    start_parser = subparsers.add_parser('record-auto', help='Record an automation sequences of the application')
    start_parser.add_argument('tag', nargs='?', default=None, help='Tag of the application')
    start_parser.set_defaults(func=entrypoint_handler.record_automation_sequences)

    
    start_parser = subparsers.add_parser('run-auto', help='Record an automation sequences of the application')
    start_parser.add_argument('tag', nargs='?', default=None, help='Tag of the application')
    start_parser.add_argument('seq_name', nargs='?', default=None, help='Name of the sequence to run')
    start_parser.set_defaults(func=entrypoint_handler.run_automations_sequences)
    
    
    # =================================================
    # ==========| APP UTILITY FEATURES | ==============
    # =================================================
    
    start_parser = subparsers.add_parser('sync', help='Sync configured applications on new machine')
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
    sleep_parser.add_argument('delay', nargs='?', default=None, help='Delay in seconds before sleep')
    sleep_parser.set_defaults(func=lambda args: entrypoint_handler.sleep(args, sleep_parser))
    
    shutdown_parser = subparsers.add_parser('shutdown', help='Shutdown PC after X seconds')
    shutdown_parser.add_argument('delay', nargs='?', default=None, help='Delay in seconds before shutdown')
    shutdown_parser.set_defaults(func=lambda args: entrypoint_handler.shutdown(args, shutdown_parser))
    
    
    start_parser = subparsers.add_parser('uuid', help='Display system UUID')
    start_parser.set_defaults(func=entrypoint_handler.display_system_uuid)
    
    # =================================================
    # ================| SCHEDULER | ===================
    # =================================================
    
    start_parser = subparsers.add_parser('run-scheduler', help='Start and run the scheduler')
    start_parser.set_defaults(func=entrypoint_handler.run_scheduler)
    
    
    
    # ===========================================================================================
    # >>> BLOCKING FUNCTIONS
    # ===========================================================================================
    sync_needed = not entrypoint_handler.apps_synced()
    if sync_needed:
        # If sync is needed, restrict all commands except 'sync'
        def blocked_func(args):
            text = colored('amiya sync', 'light_cyan')
            aprint(f"Applications under Amiya's apps manager are not fully configured to run on this machine.\n\nTo sync the apps to this machine, run `{text}`")
            exit()

        for name, subparser in subparsers.choices.items():
            if name not in ["sync", "search", "sleep", "shutdown", "uuid"]:
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
        else:
            parser.print_help()