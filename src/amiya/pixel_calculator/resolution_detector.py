import win32con
import win32gui
import win32process
import win32api
import subprocess
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
        if pid == None: return None
        
        win_info_list: list[dict] = ResolutionDetector.get_window_info(pid)
        if len(win_info_list) == 0:
            raise AmiyaBaseException("Failed to fetch window size. No results returned.")
        
        win_info = win_info_list[0]
        monitor_info = ResolutionDetector.get_primary_monitor_size()
        
        if  monitor_info["width"] == win_info["width"] and \
            monitor_info["height"] == win_info["height"] and \
            win_info["top"] == 0 and win_info["left"] == 0:
            
            win_info["is_fullscreen"] = True
        else:
            win_info["is_fullscreen"] = False
            
        return win_info
        
    @staticmethod
    def get_window_info(pid) -> list[dict]:
        
        def is_real_window(hWnd):
            if not win32gui.IsWindowVisible(hWnd):
                return False
            if win32gui.GetParent(hWnd) != 0:
                return False
            hasNoOwner = win32gui.GetWindow(hWnd, win32con.GW_OWNER) == 0
            lExStyle = win32gui.GetWindowLong(hWnd, win32con.GWL_EXSTYLE)
            if (((lExStyle & win32con.WS_EX_TOOLWINDOW) == 0 and hasNoOwner)
            or ((lExStyle & win32con.WS_EX_APPWINDOW) != 0 and not hasNoOwner)):
                if win32gui.GetWindowText(hWnd):
                    return True
            return False
        
        def callback(hWnd, windows: list):
            try:
                window_pid = win32process.GetWindowThreadProcessId(hWnd)[1]
                if window_pid == pid and is_real_window(hWnd):
                    rect = win32gui.GetWindowRect(hWnd)
                    
                    window_info = {
                        "top": rect[1],
                        "left": rect[0],
                        "width": rect[2] - rect[0],
                        "height": rect[3] - rect[1],
                        "is_fullscreen": None
                    }
                    windows.append(window_info)
                    
            except win32api.error as e:
                print(f"Failed to get process for hWnd {hWnd}: {e}")

        windows = []
        win32gui.EnumWindows(callback, windows)
        return windows
    
    
