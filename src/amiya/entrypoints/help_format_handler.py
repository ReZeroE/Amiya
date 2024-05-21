import argparse
from amiya.utils.helper import *

class HelpFormatHandler:
    def print_help(self, args, parser):
        for group in parser.groups:
            
            if group['description']:
                print(f"\n{Printer.to_lightred("☆ " + group['title'])}{Printer.to_lightgrey(" : " + group['description'])}")
            else:
                print(f"\n{Printer.to_lightred("☆ " + group['title'])}")
                
            for subparser in group['parsers']:
                prog_cmd = Printer.to_lightblue(subparser.prog)
                print(f"  {prog_cmd}: {subparser.description or 'No description available.'}")
                for action in subparser._actions:
                    if action.option_strings:
                        print(f"    {Printer.to_purple(', '.join(action.option_strings))}: {Printer.to_lightgrey(action.help)}")
                    else:
                        print(f"    {Printer.to_purple(action.dest)}: {Printer.to_lightgrey(action.help)}")
                print("")