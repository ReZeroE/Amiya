import os
import time
import psutil
import subprocess
from amiya.utils.helper import *
from amiya.utils.constants import GET_FOCUSED_PID_EXE
from amiya.exceptions.exceptions import AmiyaBaseException, Amiya_AppNotFocusedException

class SafetyMonitor:
    def __init__(self, app_pid: int):
        self.app_pid = app_pid
        self.cached_pids: set[int] = set()      # Cached PID includes all the processes' PID that is created after the SafetyMonitor
        self.monitor_create_time = time.time()  # Time when the SafetyMonitor is created
    
    def app_is_focused(self) -> bool:
        '''
        Basic safety function to ensures the automation actions are only executed if the target application is focused.
        Passed into the execute() function in ActionSequence
        '''
        focused_pid = SafetyMonitor.get_focused_pid()
        
        # If PID == original APP's PID, return True
        if focused_pid == self.app_pid:
            return True
        
        # Else:
        #   Check if the PID is one of the processes that got created after this SafetyMonitor is created. If so, ignore and return True.
        #
        #   The only reason why this exist if because if the original application is a game launcher, then the launched game's PID will
        #   be untracked and this is the only way to improve safety.
        if len(self.cached_pids) == 0:
            time.sleep(10)
            self.cached_pids = self.get_possible_pids()
            focused_pid = SafetyMonitor.get_focused_pid()
            
        
        # TODO: If the application is already running when a sequence is executed, another app process will be started and that PID will be used as the app_pid. However,
        #   that process continue to exist since the app is already running, albeit a different process. In this case, we need to check to see if the app is already 
        #   running first. If so, grab the running app's process' PID. If not, then start the process and use that pid. 
        # return True # Force return true since this error exist
        
        
        # TODO: Another problem:
        #   Generally, the cached PIDs are only used to identify applications subprocesses that start after the original app has started (thus the safety monitor is created after the application is started).
        #   The safety monitor CANNOT detect any application that gets started immediately after the original applciation starts (in the case of Persona 5 X where the executable immediately starts another executable, the actual game)
        #   This limitation needs to be resolved as some application executable isn't the sole executable that gets started on callback.   
        
        # print(f"Focused {focused_pid}")
        # print(f"App: {self.app_pid}")
        # print(f"Cached: {self.cached_pids}")
        
        
        if focused_pid not in self.cached_pids:      # Return True if currently focused PID is cached (started after the SafetyMonitor is created)
            print("")
            aprint(f"Focused PID: [{focused_pid}], Original App PID: [{self.app_pid}], Cached PID: {self.cached_pids}", log_type=LogType.ERROR)
            raise Amiya_AppNotFocusedException()
    
    @staticmethod
    def get_focused_pid() -> int|None:
        result = subprocess.run([GET_FOCUSED_PID_EXE], capture_output=True, text=True)
    
        pid = None
        if result.returncode == 0:
            pid = result.stdout.strip()
        else:
            raise AmiyaBaseException(f"Embeded script 'GET_FOCUSED_PID' failed with return code {result.returncode}")
        
        try:
            pid = int(pid)
        except ValueError:
            raise AmiyaBaseException(f"Embeded script 'GET_FOCUSED_PID' failed to fetch PID. (Fetched PID {pid} cannot be converted into INT)")
    
        return pid
    
    
    def get_possible_pids(self) -> set:
        '''
        Get all PIDs from processes that got created after the monitor is created. 
        '''
        # for p in sorted(psutil.process_iter(), key=lambda x: x.create_time()):
        #     print(f"{p.name()}, {p.create_time()}, {p.pid}")
        
        
        # print(self.monitor_create_time)
        
        # print("\n\n")
        
        return {p.pid for p in psutil.process_iter(['pid']) if p.create_time() > self.monitor_create_time}