import win32process
import pygetwindow
from ctypes import windll
from screeninfo import get_monitors

from amiya.utils.constants import GET_WINDOW_SIZE_EXE
from amiya.exceptions.exceptions import *
from amiya.apps_manager.safety_monitor import SafetyMonitor


class ResolutionDetector:
    
    # THIS IS FKING MAGIC
    # I spent 4 hours trying to figure out why every package is claiming that an 4K application has 2K resolution 
    # before I came acorss this. Apparently windows isn't DPI aware unless it's specifically set to be. In other 
    # words, this will allow the return of real pixel numbers instead of scaled values.
    windll.user32.SetProcessDPIAware()
    
    @staticmethod
    def get_primary_monitor_size() -> dict|None:
        monitors = get_monitors()
        for m in monitors:
            if m.is_primary:
                monitor_info = {
                    "width": m.width,
                    "height": m.height
                }
                return monitor_info
        return None
    
    @staticmethod
    def get_window_size():
        pid = SafetyMonitor.get_focused_pid()
        # print(f"Currently focused PID: {pid}")
        if pid == None: return None
        
        win_info: dict = ResolutionDetector.get_window_info(pid)
        if win_info == None:
            raise AmiyaBaseException(f"Failed to fetch window size. No results returned (PID {pid}).")
        
        monitor_info = ResolutionDetector.get_primary_monitor_size()
        
        if  monitor_info["width"] == win_info["width"] and \
            monitor_info["height"] == win_info["height"] and \
            win_info["top"] == 0 and win_info["left"] == 0:
            
            win_info["is_fullscreen"] = True
        else:
            win_info["is_fullscreen"] = False
            
        return win_info
        
    @staticmethod
    def get_window_info(pid):
        windows = pygetwindow.getWindowsWithTitle('')  # Get all windows
        for window in windows:
            _, window_pid = win32process.GetWindowThreadProcessId(window._hWnd)
            if window_pid == pid:
                return {
                    'left'          : window.left,
                    'top'           : window.top,
                    'width'         : window.width,
                    'height'        : window.height,
                    'is_fullscreen' : None
                }
        return None
        
    
    
