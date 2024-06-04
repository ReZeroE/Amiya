import sys, threading, time
from pynput import mouse
import pyautogui
from amiya.utils.helper import aprint, LogType
from amiya.exceptions.exceptions import AmiyaExit
from screeninfo import get_monitors

class CursorController:
    def __init__(self, verbose_hex: bool = False):
        if verbose_hex == True and len(get_monitors()) > 1:
            aprint("Note: pixel tracking is only supported on the primary monitor.", log_type=LogType.WARNING)
            # aprint("Pixel tracking with color is only supported on set up with one monitor.")
            # raise AmiyaExit()
        
        self.verbose_with_color_hex = verbose_hex
          
    
    def track_cursor(self):
        listener = mouse.Listener(on_click=self.__on_click)
        
        # thread.start()
        listener.start()
        
        aprint("Cursor listener started. Click to verbose position on new line. Press Ctrl+C to stop.")
        try:
            while True:
                self.__verbose_cursor_info()
                
        except KeyboardInterrupt:
            time.sleep(0.1)
            print("")
            
            listener.stop()
            raise AmiyaExit()


    def get_adjusted_cursor_pos(self):
        monitors = get_monitors()
        x, y = pyautogui.position()
        
        if len(monitors) < 2:
            return (x, y)
        
        first_monitor_width = monitors[0].width
        first_monitor_height = monitors[0].height

        if x >= first_monitor_width and y >= first_monitor_height:
            adjusted_x = x - first_monitor_width
            adjusted_y = y - first_monitor_height
            return (adjusted_x, adjusted_y)
        
        elif x >= first_monitor_width:
            adjusted_x = x - first_monitor_width
            return (adjusted_x, y)
        
        elif y >= first_monitor_height:
            adjusted_y = y - first_monitor_height
            return (x, adjusted_y)
        
        return (x, y)


    def __verbose_cursor_info(self):
        x, y = pyautogui.position()
        buffer = " " * 4
        aprint(f"Pixel position: ({x}, {y}){buffer}", end="\r")
        time.sleep(0.01)
        
        

    def __on_click(self, x, y, button, pressed):
        
        hex_text = ""
        if self.verbose_with_color_hex == True:
            try:
                screenshot = pyautogui.screenshot(allScreens=True)
                hex_color = self.__get_pixel_color(screenshot)
                hex_text = f" => Hex color: {hex_color}"
            except:
                hex_text = f" => Hex color: Failed to fetch."
        
        if pressed:
            buffer = " " * 10
            aprint(f'Pixel clicked: ({x}, {y}){hex_text}{buffer}')
            
    
    def __get_pixel_color(self, screenshot):
        x, y = self.get_adjusted_cursor_pos()
        
        def rgb_to_hex(rgb):
            return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])
        
        pixel_color = screenshot.getpixel((x, y))  
        hex_color = rgb_to_hex(pixel_color)
        return hex_color
