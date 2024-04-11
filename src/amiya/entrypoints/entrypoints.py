import sys
import time
import psutil
import argparse
from amiya.apps_manager.apps_manager import AppsManager 
from amiya.exceptions.exceptions import *
from amiya.utils.helper import *
from amiya.search_handler.search_handler import SearchHandler

class AmiyaEntrypointHandler:
    def __init__(self):
        self.apps_manager = AppsManager()
        self.search_handler = SearchHandler()
    
    
    def add_app(self, args):
        self.apps_manager.create_app_automated()
    
    def remove_app(self, args):
        self.apps_manager.delete_app()
    
    def show_apps(self, args):
        if args.with_tag:
            aprint("With tag")
        elif args.all:
            aprint("with all")
        else:
            self.apps_manager.print_apps()
    
    
    def start(self, args):
        if args.tag:
            self.apps_manager.run_app_with_tag(tag=args.tag)
        else:
            self.apps_manager.run_app()
            
    def delete(self, args):
        self.apps_manager.delete_app()
        
            
    def add_tag(self, args):
        self.apps_manager.add_tag()
        
    def remove_tag(self, args):
        self.apps_manager.remove_tag()


    def search(self, args):
        if args.search_content:
            self.search_handler.search(args.search_content)
        else:
            self.search_handler.search_automated()


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
        if args.tag:
            if args.seq_name:
                self.apps_manager.run_sequence_with_tag(args.tag, args.seq_name)
            else:
                self.apps_manager.run_sequence_with_tag(args.tag)
        else:
            self.apps_manager.run_sequence()


def execute_command():
    entrypoint_handler = AmiyaEntrypointHandler()
    
    parser = argparse.ArgumentParser(prog='amiya', description="Amiya CLI Automation Package")
    subparsers = parser.add_subparsers(dest='command', help='commands')

    
    help_parser = subparsers.add_parser('help', help='Show this help message and exit')
    help_parser.set_defaults(func=lambda args: parser.print_help())



    start_parser = subparsers.add_parser('add-app', help='Add a new application')
    start_parser.set_defaults(func=entrypoint_handler.add_app)
    
    start_parser = subparsers.add_parser('remove-app', help='Remove an existing application')
    start_parser.set_defaults(func=entrypoint_handler.remove_app)
    
    show_apps_parser = subparsers.add_parser('show-apps', help='Show applications')
    show_apps_parser.add_argument('--with-tag', action='store_true', help='Show applications with their tags')
    show_apps_parser.add_argument('--all', '-a', action='store_true', help='Show all applications')
    show_apps_parser.set_defaults(func=entrypoint_handler.show_apps)

    
    
    start_parser = subparsers.add_parser('start', help='Start an application')
    start_parser.add_argument('tag', nargs='?', default=None, help='Tag of the application to start')
    start_parser.set_defaults(func=entrypoint_handler.start)
    
    start_parser = subparsers.add_parser('delete', help='Delete an application')
    start_parser.set_defaults(func=entrypoint_handler.delete)
    
    
    
    start_parser = subparsers.add_parser('add-tag', help='Add a new tag to an application')
    start_parser.set_defaults(func=entrypoint_handler.add_tag)
    
    start_parser = subparsers.add_parser('remove-tag', help='Remove a tag from an application')
    start_parser.set_defaults(func=entrypoint_handler.remove_tag)
    
    
    start_parser = subparsers.add_parser('search', help='Initiate a search on the default browser')
    start_parser.add_argument('search_content', nargs='*', default=None, help='Content of the search')
    start_parser.set_defaults(func=entrypoint_handler.search)
    
    
    
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
    
    
    args = parser.parse_args()
    if hasattr(args, 'func'):
        try:
            args.func(args)
        except KeyboardInterrupt:
            print("\n\nKeybord Interupt! Amiya Exited.")
    else:
        parser.print_help() # If no arguments were provided, show help
