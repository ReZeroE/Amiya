
from tabulate import tabulate
from amiya.apps_manager.app import App
from amiya.utils.constants import APPS_DIRECTORY

class AppsViewer:
    
    @staticmethod
    def tabulate_apps(apps_dict: dict[int, App], tablefmt) -> str:
        table = [[id, app.name, app.exe_path, app.verified, ", ".join(app.tags)] for id, app in apps_dict.items()]
        table = sorted(table, key=lambda x: x[0])
        headers = ["ID", "App Name", "Path", "Verified", "Tags"]
        return tabulate(table, headers, tablefmt=tablefmt)
    
    @staticmethod
    def tabulate_app(app: App, tablefmt) -> str:
        table = [[app.name, app.exe_path, app.verified, ", ".join(app.tags)]]
        headers = ["App Name", "Path", "Verified", "Tags"]
        return tabulate(table, headers, tablefmt=tablefmt)
    
    @staticmethod
    def tabulate_tags(tags, tablefmt):
        table = [[idx, tag] for idx, tag in enumerate(tags)]
        headers = ["Index", "Tag"]
        return tabulate(table, headers, tablefmt=tablefmt)
        
