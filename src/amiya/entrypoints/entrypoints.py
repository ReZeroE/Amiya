import os
import sys
import time
import psutil
import argparse

import ctypes
import subprocess

from termcolor import colored
from amiya.entrypoints.entrypoint_handler import AmiyaEntrypointHandler
from amiya.entrypoints.help_format_handler import HelpFormatHandler
from amiya.utils.helper import aprint, atext, verify_platform, is_admin, Printer, color_cmd
from amiya.utils.constants import COMMAND
from amiya.exceptions.exceptions import AmiyaOSNotSupported, AmiyaExit


class AmiyaArgParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.groups = []

    def add_group(self, title, description=None):
        group = {'title': title, 'description': description, 'parsers': []}
        self.groups.append(group)
        return group

    def add_parser_to_group(self, group, parser):
        group['parsers'].append(parser)
        
    def error(self, message):
        command = message.split("'")[1] if "invalid choice:" in message else None
        helpt = Printer.to_purple("help")
        aprint(f"Command not recognized: {command}\nType '{helpt}' for commands list")
        self.exit(2)


def start_amiya():
    entrypoint_handler = AmiyaEntrypointHandler()
    help_format_handler = HelpFormatHandler()
    
    parser = AmiyaArgParser(prog=COMMAND, description="Amiya CLI Automation Package")
    subparsers = parser.add_subparsers(dest='command', help='commands')

    help_parser = subparsers.add_parser('help', help='Show this help message and exit')
    help_parser.set_defaults(func=lambda args: help_format_handler.print_help(args, parser))

    # =================================================
    # =================| DEVELOPMENT | ================
    # =================================================
    dev_group = parser.add_group('Development', 'Developer\'s commands. Open available when [constants.DEVELOPMENT=True].')
    
    dev_parser = subparsers.add_parser('dev', 
        help='[DEV] Developer\'s commands.',
        description='[DEV] Developer\'s commands.'
    )
    dev_parser.add_argument('--objects', '-obj', action='store_true', help='Show all controller objects and their addresses.')
    dev_parser.add_argument('--refresh', '-ref', action='store_true', help='Refresh all controller objects.')
    dev_parser.add_argument('--code', '-c', action='store_true', help='Open development environment with VSCode.')
    dev_parser.add_argument('--isadmin', '-ia', action='store_true', help='Show whether the main thread has admin access.')
    dev_parser.set_defaults(func=entrypoint_handler.DEV)
    parser.add_parser_to_group(dev_group, dev_parser)

    # ================================================
    # ===================| ABOUT | ===================
    # ================================================
    
    about_group = parser.add_group('About', 'Get information about the Amiya module in general.')
    
    version_parser = subparsers.add_parser('version', help='Verbose module version', description='Verbose module version')
    version_parser.set_defaults(func=entrypoint_handler.version)
    parser.add_parser_to_group(about_group, version_parser)
                              
    author_parser = subparsers.add_parser('author', help='Verbose module author', description='Verbose module author')
    author_parser.set_defaults(func=entrypoint_handler.author)
    parser.add_parser_to_group(about_group, author_parser)
    
    repo_parser = subparsers.add_parser('repo', help='Verbose module repository link', description='Verbose module repository link')
    repo_parser.set_defaults(func=entrypoint_handler.repo)
    parser.add_parser_to_group(about_group, repo_parser)
    

    # =================================================
    # ============| ADD/REMOVE/SHOW APPS | ============
    # =================================================

    apps_group = parser.add_group('App Management', 'Add, remove, and show applications in Amiya\'s app configuration.')
    
    add_app_parser = subparsers.add_parser('add-app', help='Add a new application', description='Add a new application')
    add_app_parser.set_defaults(func=entrypoint_handler.add_app)
    parser.add_parser_to_group(apps_group, add_app_parser)
    
    remove_app_parser = subparsers.add_parser('remove-app', help='Remove an existing application', description='Remove an existing application')
    remove_app_parser.add_argument('tag', nargs='?', default=None, help='Tag of the application to remove')
    remove_app_parser.set_defaults(func=entrypoint_handler.remove_app)
    parser.add_parser_to_group(apps_group, remove_app_parser)
    
    show_apps_parser = subparsers.add_parser('show-apps', help='Show applications', description='Show applications')
    show_apps_parser.add_argument('--short', '-s', action='store_true', help='Only show the app ID, name, and verification status')
    show_apps_parser.add_argument('--full-path', '-f', action='store_true', help='Show the full path of the applications')
    show_apps_parser.set_defaults(func=entrypoint_handler.show_apps)
    parser.add_parser_to_group(apps_group, show_apps_parser)
    
    show_config_parser = subparsers.add_parser('show-config', help='Show application configuration directory', description='Show application configuration directory')
    show_config_parser.add_argument('tag', nargs='?', default=None, help='Tag of the application to show the configuration directory of')
    show_config_parser.add_argument('--all', '-a', action='store_true', help='Show all configuration directory paths (including automation)')
    show_config_parser.set_defaults(func=entrypoint_handler.show_app_config_dir)
    parser.add_parser_to_group(apps_group, show_config_parser)


    # =================================================
    # =================| START APPS | =================
    # =================================================
    
    start_apps_group = parser.add_group('Application Launcher', 'Start or terminate applications from the CLI.')
    
    start_parser = subparsers.add_parser('start', help='Start an application', description='Start an application')
    start_parser.add_argument('tag', nargs='?', default=None, help='Tag of the application to start')
    start_parser.set_defaults(func=entrypoint_handler.start)
    parser.add_parser_to_group(start_apps_group, start_parser)
    
    
    # =================================================
    # ==============| ADD/REMOVE TAGS | ===============
    # =================================================
    
    tags_group = parser.add_group('Tag Management', 'Add or remove tags associated with applications configured with Amiya.')
    
    add_tag_parser = subparsers.add_parser('add-tag', help='Add a new tag to an application', description='Add a new tag to an application')
    add_tag_parser.set_defaults(func=entrypoint_handler.add_tag)
    parser.add_parser_to_group(tags_group, add_tag_parser)
    
    remove_tag_parser = subparsers.add_parser('remove-tag', help='Remove a tag from an application', description='Remove a tag from an application')
    remove_tag_parser.set_defaults(func=entrypoint_handler.remove_tag)
    parser.add_parser_to_group(tags_group, remove_tag_parser)
    
    # =================================================
    # ========| RECORD/LIST/RUN AUTOMATION |===========
    # =================================================
    
    automation_group = parser.add_group('Automation', 'Record, show, and run automations in applications.')
    
    list_auto_parser = subparsers.add_parser('list-auto', help='List all the automation sequences of the application', description='List all the automation sequences of the application')
    list_auto_parser.add_argument('tag', nargs='?', default=None, help='Tag of the application')
    list_auto_parser.set_defaults(func=entrypoint_handler.list_automation_sequences)
    parser.add_parser_to_group(automation_group, list_auto_parser)
    
    record_auto_parser = subparsers.add_parser('record-auto', help='[Admin Permission Req.] Record an automation sequence of the application', description='[Admin Permission Req.] Record an automation sequence of the application')
    record_auto_parser.add_argument('tag', nargs='?', default=None, help='Tag of the application')
    record_auto_parser.set_defaults(func=entrypoint_handler.record_automation_sequences)
    parser.add_parser_to_group(automation_group, record_auto_parser)

    run_auto_parser = subparsers.add_parser('run-auto', help='[Admin Permission Req.] Run an automation sequence of the application', description='[Admin Permission Req.] Run an automation sequence of the application')
    run_auto_parser.add_argument('tag', nargs='?', default=None, help='Tag of the application')
    run_auto_parser.add_argument('seq_name', nargs='?', default=None, help='Name of the sequence to run')
    run_auto_parser.add_argument('--global-delay', '-g', type=int, default=-1, help='Add a global delay to the sequence during execution')
    run_auto_parser.add_argument('--terminate', '-t', default=False, action='store_true', help='Terminate the application on automation completion')
    run_auto_parser.add_argument('--no-confirmation', '-nc', default=False, action='store_true', help='Run the automation without confirmation')
    run_auto_parser.add_argument('--sleep', default=False, action='store_true', help='Put PC to sleep after automation finishes (overwrites --shutdown)')
    run_auto_parser.add_argument('--shutdown', default=False, action='store_true', help='Shutdown PC after automation finishes')
    run_auto_parser.set_defaults(func=entrypoint_handler.run_automations_sequences)
    parser.add_parser_to_group(automation_group, run_auto_parser)
    
    
    # =================================================
    # ==========| APP UTILITY FEATURES | ==============
    # =================================================
    
    app_utility_group = parser.add_group('Sync Commands', 'Sync (auto-locate) and cleanup applications across different local machines.')
    
    sync_parser = subparsers.add_parser('sync', help='Sync configured applications on new machine OR auto configure application executable paths', description='Sync configured applications on new machine OR auto configure application executable paths')
    sync_parser.set_defaults(func=entrypoint_handler.sync)
    parser.add_parser_to_group(app_utility_group, sync_parser)
    
    cleanup_parser = subparsers.add_parser('cleanup', help='Remove all unverified applications', description='Remove all unverified applications')
    cleanup_parser.set_defaults(func=entrypoint_handler.cleanup)
    parser.add_parser_to_group(app_utility_group, cleanup_parser)
    
    
    # =================================================
    # =============| UTILITY FEATURES | ===============
    # =================================================
    
    utility_group = parser.add_group('Utility', 'Other useful and easy-to-use utilities provided by the Amiya module.')
    
    search_parser = subparsers.add_parser('search', help='Initiate a search on the default browser', description='Initiate a search on the default browser')
    search_parser.add_argument('search_content', nargs='*', default=None, help='Content of the search')
    search_parser.set_defaults(func=entrypoint_handler.search)
    parser.add_parser_to_group(utility_group, search_parser)
    
    sleep_parser = subparsers.add_parser('sleep', help='Put the PC to sleep after X seconds', description='Put the PC to sleep after X seconds')
    sleep_parser.add_argument('delay', nargs='?', type=int, default=0, help='Delay in seconds before sleep')
    sleep_parser.set_defaults(func=lambda args: entrypoint_handler.sleep(args, sleep_parser))
    parser.add_parser_to_group(utility_group, sleep_parser)
    
    shutdown_parser = subparsers.add_parser('shutdown', help='Shutdown PC after X seconds', description='Shutdown PC after X seconds')
    shutdown_parser.add_argument('delay', nargs='?', type=int, default=0, help='Delay in seconds before shutdown')
    shutdown_parser.set_defaults(func=lambda args: entrypoint_handler.shutdown(args, shutdown_parser))
    parser.add_parser_to_group(utility_group, shutdown_parser)
    
    uuid_parser = subparsers.add_parser('uuid', help='Display system UUID', description='Display system UUID')
    uuid_parser.set_defaults(func=entrypoint_handler.display_system_uuid)
    parser.add_parser_to_group(utility_group, uuid_parser)
    
    pixel_parser = subparsers.add_parser('pixel', help='Track cursor position and color', description='Track cursor position and color')
    pixel_parser.add_argument('--color', '-c', action='store_true', help='Show pixel coordinate as well as the pixel\'s color hex value.')
    pixel_parser.set_defaults(func=entrypoint_handler.track_cursor)
    parser.add_parser_to_group(utility_group, pixel_parser)
    
    volume_parser = subparsers.add_parser('volume', help='Open simple application volume control UI', description='Open simple application volume control UI')
    volume_parser.set_defaults(func=entrypoint_handler.open_volume_control_ui)
    parser.add_parser_to_group(utility_group, volume_parser)
    
    click_parser = subparsers.add_parser('click', help='Continuously click mouse.', description='Continuously click mouse.')
    click_parser.add_argument('--count', '-c', type=int, default=-1, help='Number of clicks. Leave empty (default) to run forever')
    click_parser.add_argument('--interval', '-d', type=int, default=1, help='Interval delay (seconds) between clicks')
    click_parser.add_argument('--hold-time', '-ht', type=int, default=0.1, help='Delay (seconds) between click press and release')
    click_parser.add_argument('--start-after', '-sa', type=int, default=3, help='Delay (seconds) before the clicks start')
    click_parser.add_argument('--quiet', '-q', action='store_true', default=False, help='Run without verbosing progress')
    click_parser.set_defaults(func=entrypoint_handler.click_continuously)
    parser.add_parser_to_group(utility_group, click_parser)
    
    elevate_parser = subparsers.add_parser('elevate', help='Elevate `amiya` permissions.', description='Elevate `amiya` permissions.')
    elevate_parser.add_argument('--explain', action='store_true', help='Explain why this is needed and what will happen.')
    elevate_parser.set_defaults(func=entrypoint_handler.elevate)
    parser.add_parser_to_group(utility_group, elevate_parser)
    
    track_url_parser = subparsers.add_parser('track-url', help='Track URL to monitor anchor href changes.', description='Track URL to monitor anchor href changes.')
    track_url_parser.add_argument('--url', type=str, default="https://mc.kurogames.com/", help='The website URL to track')
    track_url_parser.add_argument('--interval', "-i", type=int, default=0, help='The interval duration between GET requests (seconds). Defaulted to 0.')
    track_url_parser.add_argument('--open', "-o", action='store_true', default=False, help='Open the URL when it is detected as new.')
    track_url_parser.set_defaults(func=entrypoint_handler.track_url)
    parser.add_parser_to_group(utility_group, track_url_parser)

    
    
    # # =================================================
    # # ================| SCHEDULER | ===================
    # # =================================================
    
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
            aprint(f"Applications under Amiya's apps manager are not fully configured to run on this machine.\n\nTo sync the apps to this machine, run `{text}`\n")
            raise AmiyaExit()

        for name, subparser in subparsers.choices.items():
            if name not in ["sync", "search", "sleep", "shutdown", "uuid", "show-config", "version", "author", "repo"]:
                subparser.set_defaults(func=blocked_func)
    
    
    isadmin = is_admin()
    if not isadmin:
        # Certain commands require admin permissions to execute
        def blocked_func(args):
            elevate_cmd = color_cmd("amiya elevate", with_quotes=True)
            aprint(f"Insufficient permission. Run {elevate_cmd} to elevate permissions first.")
            raise AmiyaExit()

        for name, subparser in subparsers.choices.items():
            if name in ["record-auto", "run-auto"]:
                subparser.set_defaults(func=blocked_func)
    
    
    # ===========================================================================================
    # >>> PARSER DRIVER
    # ===========================================================================================
    
    # Check if no command line arguments are provided
    if len(sys.argv) == 1:
        aprint("Loading Amiya CLI environment...")
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
            


def start_amiya_cli_as_admin():
    start_amiya()
    
    # # If process already have admin access
    # if is_admin():
    #     start_amiya()
    #     return

    # # Else, request admin permissions
    # user_input = input(atext("Amiya is not ran as admin. Would you like to run 'amiya' as admin? [y/n] "))
    # if user_input.lower() != "y":
    #     start_amiya()
    #     return
    
    # script = os.path.abspath(sys.argv[0])
    # params = ' '.join([script] + sys.argv[1:])
    # try:
    #     subprocess.run(["powershell", "-Command", f"Start-Process -Verb runAs {params}"])
    # except Exception as e:
    #     aprint(f"Failed to elevate privileges: {e}")
    # sys.exit(0)