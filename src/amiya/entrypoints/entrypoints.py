import sys
import time
import psutil
import argparse
from amiya.entrypoints.entrypoint_handler import AmiyaEntrypointHandler




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
    show_apps_parser.add_argument('--with-tag', action='store_true', help='Show applications with their tags')
    show_apps_parser.add_argument('--all', '-a', action='store_true', help='Show all applications')
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
    
    import ctypes
    def is_admin_windows():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def elevate_windows():
        if not ctypes.windll.shell32.IsUserAnAdmin():
            print("Elevating to admin privileges...")
            print(sys.executable)
            print(" ".join(sys.argv))
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            sys.exit(0)
            
    
    # =================================================
    # PARSER DRIVER
    
    # print("Elevating...")
    # elevate_windows()
    
    # time.sleep(10)
    
    args = parser.parse_args()
    if hasattr(args, 'func'):
        try:
            args.func(args)
        except KeyboardInterrupt:
            print("\n\nKeybord Interupt! Amiya Existing.")
    else:
        parser.print_help() # If no arguments were provided, show help
