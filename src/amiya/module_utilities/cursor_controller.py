import sys, threading, time
from pynput import mouse
import pyautogui
from amiya.utils.helper import aprint
from amiya.exceptions.exceptions import AmiyaExit
import pyscreeze
from screeninfo import get_monitors

class CursorController:
    def __init__(self):
        pass
    
    def track_cursor(self):
        stop_event = threading.Event()
        thread = threading.Thread(target=self.__verbose_cursor_info, args=(stop_event,))
        thread.start()
        
        listener = mouse.Listener(on_click=self.__on_click)
        listener.start()
        
        aprint("Cursor listener started. Click to verbose position on new line. Press Ctrl+C to stop.")
        try:
            while listener.running:
                pass
        except KeyboardInterrupt:
            listener.stop()
            stop_event.set()
            thread.join()
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



    def __verbose_cursor_info(self, stop_event: threading.Event):
        while not stop_event.is_set():
            x, y = pyautogui.position()
            buffer = " " * 4
            aprint(f"Pixel position: ({x}, {y}){buffer}", end="\r")
            time.sleep(0.01)
            
        time.sleep(0.1)
        print("")


    def __get_pixel_color(self, screenshot):
        x, y = self.get_adjusted_cursor_pos()
        
        def rgb_to_hex(rgb):
            return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])
        
        pixel_color = screenshot.getpixel((x, y))  
        hex_color = rgb_to_hex(pixel_color)
        return hex_color


    def __on_click(self, x, y, button, pressed):
        screenshot = pyautogui.screenshot()
        hex_color = self.__get_pixel_color(screenshot)
        
        if pressed:
            buffer = " " * 10
            aprint(f'Pixel clicked: ({x}, {y}) => Hex color: {hex_color}{buffer}')
            
    
    