from amiya.apps_manager.apps_manager import AppsManager 
from amiya.exceptions.exceptions import *
from amiya.utils.helper import *
from amiya.utils.constants import DEVELOPMENT, HOME_DIRECTORY
from amiya.module_utilities.search_controller import SearchController
from amiya.module_utilities.power_controller import PowerUtils
from amiya.module_utilities.cursor_controller import CursorController

class DevController:
    def __init__(self):
        if not DEVELOPMENT:
            aprint(f"Development commands unavailable (development={DEVELOPMENT}). ")
            raise AmiyaExit()
    
    
    def verbose_objects(self, apps_manager, search_controller, power_utils, cursor_controller):
        aprint(f"{apps_manager}\n{search_controller}\n{power_utils}\n{cursor_controller}")

    def refresh_objects(self):
        apps_manager = AppsManager()
        search_controller = SearchController()
        power_utils = PowerUtils()
        cursor_controller = CursorController()
        aprint(f"Refresh Completed.\n{apps_manager}\n{search_controller}\n{power_utils}\n{cursor_controller}")

    def open_dev_env(self):
        aprint(f"Opening development environment ({HOME_DIRECTORY})...")
        os.system(f"code {HOME_DIRECTORY}")