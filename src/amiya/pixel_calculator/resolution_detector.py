import subprocess
from amiya.utils.constants import GET_WINDOW_SIZE_EXE
from screeninfo import get_monitors
from amiya.exceptions.exceptions import *
from amiya.apps_manager.safty_monitor import SaftyMonitor

class ResolutionDetector:
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
        pid = SaftyMonitor.get_focused_pid()
        if pid == None: return None
        
        try:
            result = subprocess.run([GET_WINDOW_SIZE_EXE, str(pid)], capture_output=True, text=True)
            if result.returncode == 0 and result.stdout:
                width, height, is_fullscreen = map(int, result.stdout.strip().split())
                return {
                    'width': width,
                    'height': height,
                    'is_fullscreen': bool(is_fullscreen)
                }
            else:
                raise  AmiyaBaseException("Failed to get window size or no window found for PID")
        except Exception as e:
            return f"An error occurred: {str(e)}"