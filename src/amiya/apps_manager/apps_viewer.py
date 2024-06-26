
from termcolor import colored
from tabulate import tabulate
from amiya.apps_manager.app import App
from amiya.utils.constants import APPS_DIRECTORY
from amiya.utils.helper import bool_to_str, Printer, shorten_display_path, resize_terminal


class AppsViewer:
    
    @staticmethod
    def tabulate_apps(apps_dict: dict[int, App], tablefmt) -> str:
        table = [[id, app.name, Printer.to_lightgrey(shorten_display_path(app.exe_path)), bool_to_str(app.verified), ", ".join(app.tags)] for id, app in apps_dict.items()]
        table = sorted(table, key=lambda x: x[0])
        headers = ["ID", "App Name", "Executable Path", "Path Verified", "Tags"]
        headers = [Printer.to_blue(title) for title in headers]
        tabulated_apps_table =  tabulate(table, headers, tablefmt=tablefmt)
        # tabulated_apps_table = '\n'.join('  ' + line for line in tabulated_apps_table.split('\n'))

        table_len = len(tabulated_apps_table.split("\n")[0])
        resize_terminal(table_len, 5)
        
        return tabulated_apps_table
    
    @staticmethod
    def tabulate_apps_list(apps_list: list[App], tablefmt) -> str:
        table = [[app.name, Printer.to_lightgrey(shorten_display_path(app.exe_path)), bool_to_str(app.verified), ", ".join(app.tags)] for app in apps_list]
        table = sorted(table, key=lambda x: x[0])
        
        headers = ["App Name", "Executable Path", "Verified", "Tags"]
        headers = [Printer.to_blue(title) for title in headers]
        
        return tabulate(table, headers, tablefmt=tablefmt)
    
    @staticmethod
    def tabulate_app(app: App, tablefmt) -> str:
        table = [[app.name, Printer.to_lightgrey(shorten_display_path(app.exe_path)), bool_to_str(app.verified), ", ".join(app.tags)]]
        
        headers = ["App Name", "Executable Path", "Verified", "Tags"]
        headers = [Printer.to_blue(title) for title in headers]
        
        return tabulate(table, headers, tablefmt=tablefmt)
    
 
    @staticmethod
    def tabulate_tags(tags, tablefmt):
        table = [[idx, tag] for idx, tag in enumerate(tags)]
        
        headers = ["Index", "Tag"]
        headers = [Printer.to_blue(title) for title in headers]
        
        return tabulate(table, headers, tablefmt=tablefmt)
        
