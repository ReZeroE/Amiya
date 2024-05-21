import webbrowser
from amiya.exceptions.exceptions import *
from amiya.utils.helper import *

class SearchController:
    def __init__(self):
        self.SERACH_URL = f"https://www.google.com.tr/search?q="
    
    def search(self, search_content: str|list[str]):
        search_str = None
        if isinstance(search_content, str):
            search_str = search_content
        elif isinstance(search_content, list):
            search_str = " ".join(search_content)
        else:
            raise AmiyaBaseException("Internal Error: Search Input Type Invalid.")
        
        url = f"{self.SERACH_URL}{search_str}"
        success = webbrowser.open_new_tab(url)
        
        if not success:
            aprint("Search failed due to web browser availablility or invalid request.", log_type=LogType.ERROR); raise AmiyaExit()

    def search_automated(self):
        search_content = input(atext("What would you like to search? ")).strip()
        if len(search_content) > 0:
            self.search(search_content)
