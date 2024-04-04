import sys
import time
import psutil
import argparse
from amiya.apps_manager.apps_manager import AppsManager 
from amiya.exceptions.exceptions import *
from amiya.utils.helper import *

class AmiyaEntrypointHandler:
    def __init__(self):
        self.apps_manager = AppsManager()
    
    def print_help(self, args):
        pass
    
    
    def start(self, args):
        if args.tag:
            self.apps_manager.run_app_with_tag(tag=args.tag)
        else:
            self.apps_manager.run_app()
            
    def delete(self, args):
        self.apps_manager.delete_app()
        
        
    def show_apps(self, args):
        if args.with_tag:
            aprint("With tag")
        elif args.all:
            aprint("with all")
        else:
            self.apps_manager.print_apps()
            
    def add_tag(self, args):
        self.apps_manager.add_tag()
        
    def remove_tag(self, args):
        self.apps_manager.remove_tag()


def execute_command():
    entrypoint_handler = AmiyaEntrypointHandler()

    # ======================================
    # ======== | Setup Arg Parser | ========
    # ======================================
    
    parser = argparse.ArgumentParser(prog='amiya', description="Amiya CLI Automation Package")
    subparsers = parser.add_subparsers(dest='command', help='commands')

    # Parser for 'help' command
    help_parser = subparsers.add_parser('help', help='Show this help message and exit')
    help_parser.set_defaults(func=lambda args: parser.print_help())

    # Parser for 'show-apps' command
    show_apps_parser = subparsers.add_parser('show-apps', help='Show applications')
    show_apps_parser.add_argument('--with-tag', action='store_true', help='Show applications with their tags')
    show_apps_parser.add_argument('--all', '-a', action='store_true', help='Show all applications')
    show_apps_parser.set_defaults(func=entrypoint_handler.show_apps)

    # Parser for 'start' command
    start_parser = subparsers.add_parser('start', help='Start an application')
    start_parser.add_argument('tag', nargs='?', default=None, help='Tag of the application to start')
    start_parser.set_defaults(func=entrypoint_handler.start)
    
    start_parser = subparsers.add_parser('delete', help='Delete an application')
    start_parser.set_defaults(func=entrypoint_handler.delete)
    
    start_parser = subparsers.add_parser('add-tag', help='Add a new tag to an application')
    start_parser.set_defaults(func=entrypoint_handler.add_tag)
    
    start_parser = subparsers.add_parser('remove-tag', help='Remove a tag from an application')
    start_parser.set_defaults(func=entrypoint_handler.remove_tag)
    
    
    args = parser.parse_args()
    if hasattr(args, 'func'):
        try:
            args.func(args)
        except KeyboardInterrupt:
            print("\nKeybord Interupt!")
    else:
        parser.print_help() # If no arguments were provided, show help
