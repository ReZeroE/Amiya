
from tabulate import tabulate
from apps_manager.app import App
from utils.constants import APPS_DIRECTORY

class AppsViewer:
    
    @staticmethod
    def tabulate_apps(apps_dict: dict[int, App], tablefmt) -> str:
        table = [[id, app.name, app.exe_path, app.verified] for id, app in apps_dict.items()]
        table = sorted(table, key=lambda x: x[0])
        headers = ["ID", "App Name", "Path", "Verified"]
        return tabulate(table, headers, tablefmt=tablefmt)
        
