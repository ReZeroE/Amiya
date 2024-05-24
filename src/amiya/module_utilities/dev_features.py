from amiya.apps_manager.apps_manager import AppsManager 
from amiya.exceptions.exceptions import *
from amiya.utils.helper import *
from amiya.utils.constants import DEVELOPMENT, HOME_DIRECTORY
from amiya.module_utilities.search_controller import SearchController
from amiya.module_utilities.power_controller import PowerUtils

class DevController:
    def __init__(self):
        if not DEVELOPMENT:
            aprint(f"Development commands unavailable (development={DEVELOPMENT}). ")
            raise AmiyaExit()
    
    
    def verbose_objects(self, apps_manager, search_controller, power_utils):
        aprint(f"{apps_manager}\n{search_controller}\n{power_utils}")

    def refresh_objects(self):
        apps_manager = AppsManager()
        search_controller = SearchController()
        power_utils = PowerUtils()
        aprint(f"Refresh Completed.\n{apps_manager}\n{search_controller}\n{power_utils}")

    def open_dev_env(self):
        aprint(f"Opening development environment ({HOME_DIRECTORY})...")
        os.system(f"code {HOME_DIRECTORY}")
        
    def is_admin(self):
        isadmin = bool_to_str(is_admin(), true_text="Admin", false_text="User")
        aprint(f"Persmissions: {isadmin}")
        
    def verbose_home_dir(self):
        aprint(f"Home directory: {HOME_DIRECTORY}")