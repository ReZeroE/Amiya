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
        
        curr_window_width = curr_window_info["width"]
        curr_window_height = curr_window_info["height"]
        prev_window_width = prev_window_info["width"]
        prev_window_height = prev_window_info["height"]
        
        prev_coor_x = prev_coor[0]
        prev_corr_y = prev_coor[1]
        
        prev_center_x = self.prev_monitor_width / 2
        prev_center_y = self.prev_monitor_height / 2
        current_center_x = self.current_monitor_width / 2
        current_center_y = self.current_monitor_height / 2

        # Calculate the top-left corner of the centered window on each monitor
        prev_window_origin_x = prev_center_x - (prev_window_width / 2)
        prev_window_origin_y = prev_center_y - (prev_window_height / 2)
        current_window_origin_x = current_center_x - (curr_window_width / 2)
        current_window_origin_y = current_center_y - (curr_window_height / 2)

        # Calculate the absolute position of the previous coordinate on the monitor
        prev_absolute_x = prev_window_origin_x + prev_coor_x
        prev_absolute_y = prev_window_origin_y + prev_corr_y

        # Calculate the relative position of the previous coordinate within the previous monitor
        rel_x = (prev_absolute_x - prev_window_origin_x) / prev_window_width
        rel_y = (prev_absolute_y - prev_window_origin_y) / prev_window_height

        # Apply the relative position to the current window dimensions
        new_x = current_window_origin_x + (rel_x * curr_window_width)
        new_y = current_window_origin_y + (rel_y * curr_window_height)

        return (int(new_x), int(new_y))