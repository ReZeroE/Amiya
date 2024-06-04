from amiya.utils.helper import *
from amiya.exceptions.exceptions import AmiyaExit
import webbrowser

class URLTracker:

    def __init__(self):
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.service import Service as ChromeService
            from selenium.webdriver.chrome.options import Options
            from webdriver_manager.chrome import ChromeDriverManager
            import time
        except ImportError as ex:
            aprint(f"Failed to import necessary modules: {str(ex)}", log_type=LogType.ERROR)
            raise AmiyaExit()
        
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--log-level=2")
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options, keep_alive=True)
        
        self.rounds = 1
        self.errors_count = 0

    def get_links(self, url):
        ERROR_THRESHOLD = 10
        
        try:
            import time
            from bs4 import BeautifulSoup
            
            self.driver.get(url)
            time.sleep(5)  # Wait for webpage to load
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            anchors_data = [
                {
                    "href": anchor["href"],
                    "id": anchor.get("id"),
                    "class": anchor.get("class")
                } 
                for anchor in soup.find_all('a', href=True)
            ]
            
            if self.errors_count > 0:
                self.errors_count = 0
                aprint("Recovered from error. Resetting error count.", submodule_name="URL-Tracker")
            
            return anchors_data
        except Exception as e:
            if self.errors_count > ERROR_THRESHOLD:
                aprint(f"Number of request errors has exceeded the threshold ({self.errors_count}).\nTerminating URL tracker and its associated webdriver.", log_type=LogType.ERROR)
                self.driver.quit()
                raise AmiyaExit()
            
            aprint(f"Error occurred while fetching the links: {str(e)}", log_type=LogType.ERROR)
            time.sleep(60)  # On error, wait for one min before trying again.
            self.errors_count += 1
            return []

    def safe_track_changes(self, url: str, interval: int = 0, open_when_detected: bool = False):
        if not url:
            aprint("URL must be specified with the `--url` argument.", log_type=LogType.ERROR)
        
        aprint(f"Starting tracker on URL `{url}`...", submodule_name="URL-Tracker")
        try:
            self.__track_changes(url, interval, open_when_detected)
        except KeyboardInterrupt:
            if self.rounds > 1:
                print("")
            tx = Printer.to_lightred("this may take up to 30 seconds")
            aprint(f"Keyboard interrupted. Exiting the webdriver... ({tx})")
        except Exception as ex:
            if self.rounds > 1:
                print("")
            aprint(f"An unexpected error has occurred: {str(ex)}. Exiting the webdriver... (this may take a second)", log_type=LogType.ERROR)
        finally:
            self.driver.quit()
            aprint("Webdriver exit complete.")
            raise AmiyaExit()

    def __track_changes(self, url, interval, open_when_detected):
        original_anchors = self.get_links(url)
        original_href_list = [original_anchor["href"] for original_anchor in original_anchors]
        aprint(f"Webdriver initialized. Initial fetch returned {len(original_href_list)} HREFs from the site.", submodule_name="URL-Tracker")
        self.__print_new_anchors(original_anchors, initialization=True)
        
        while True:
            import time
            
            starting_time = time.time()
            new_anchors = []
            has_diff = False
            
            # Fetch current links and iterate through the links
            current_anchors = self.get_links(url)
            for curr_anchor in current_anchors:
                # If curr link is not in the original links list, append to new_anchors to verbose later
                if curr_anchor["href"] not in original_href_list:
                    new_anchors.append(curr_anchor)
                    has_diff = True    
            
            if has_diff:  # If there is a new anchor href, verbose and reset original anchor list
                self.__print_new_anchors(new_anchors)
                original_href_list = [curr_anchor["href"] for curr_anchor in current_anchors]
                
                if open_when_detected:
                    aprint("Opening the new href links...")
                    for href_url in original_href_list:
                        webbrowser.open_new_tab(href_url)
                
            else:
                aprint(f"Rounds {self.rounds} check complete ({round(time.time() - starting_time, 2)} seconds). No anchor href change detected.    ", end="\r", flush=True, submodule_name="URL-Tracker")

            self.rounds += 1
            time.sleep(interval)
            starting_time = time.time()
    
    def __print_new_anchors(self, new_anchors: list[dict], initialization: bool = False):
        from amiya.utils.helper import DatetimeHandler, Printer
        
        # Header
        datetime_str = Printer.to_lightblue(DatetimeHandler.get_datetime_str())
        text = f"[{datetime_str}] "
        
        if initialization:
            text += "Initialized with the following HREFs:\n"
        else:
            text += Printer.to_lightgreen(f"New HREFs detected (round {self.rounds}):\n")
        
        # New anchors
        for anchor in new_anchors:
            this_href = anchor["href"]
            this_cls = anchor["class"]
            this_id = anchor["id"]
        
            plussign = Printer.to_lightgreen("+")
            text += f" {plussign} <{this_href}> class={this_cls} id={this_id}\n"
        
        if self.rounds > 1:
            print("")
        text = text.rstrip("\n")
        print(text, flush=True)
