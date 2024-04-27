from amiya.utils.helper import aprint, LogType
from amiya.pixel_calculator.resolution_detector import ResolutionDetector

class PixelCalculator:
    def __init__(self, monitor_info: dict):
        self.prev_monitor_width = monitor_info["width"]
        self.prev_monitor_height = monitor_info["height"]
    
        current_monitor_info = ResolutionDetector.get_primary_monitor_size()
        self.current_monitor_width = current_monitor_info["width"]
        self.current_monitor_height = current_monitor_info["height"]
    
    def calculate_new_coordinate(self, prev_coor: tuple, prev_window_info: dict):
        curr_window_info = ResolutionDetector.get_window_size()
        
        if curr_window_info["is_fullscreen"] == True and prev_window_info["is_fullscreen"] == True:
            
            prev_x = prev_coor[0]
            prev_y = prev_coor[1]

            new_x = self.current_monitor_width / self.prev_monitor_width * prev_x
            new_y = self.current_monitor_height / self.prev_monitor_height * prev_y  
            
            return(int(new_x), int(new_y))  
            
        else:
            print(f"\nCurrent Window: (Width {curr_window_info["width"]}) (Height {curr_window_info["height"]})")
            print(f"Current Monitor: (Width {self.current_monitor_width}) (Height {self.current_monitor_height})")
            print(f"Previous Window: (Width {prev_window_info["width"]}) (Height {prev_window_info['height']})")
            print(f"Previous Monitor: (Width {self.prev_monitor_width}) (Height {self.prev_monitor_height})")
            
            aprint("[Pixel-Calc] Window size does not match monitor size, pixel calculator returning previous coordinate.", log_type=LogType.WARNING)
            return None
    