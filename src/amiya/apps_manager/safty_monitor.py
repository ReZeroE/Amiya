import os
import time
import psutil
import subprocess
from amiya.utils.helper import *
from amiya.utils.constants import GET_FOCUSED_PID_EXE
from amiya.exceptions.exceptions import AmiyaBaseException

class SaftyMonitor:
    def __init__(self, app_pid: int):
        self.app_pid = app_pid
        self.cached_pids: set[int] = set()      # Cached PID includes all the processes' PID that is created after the SaftyMonitor
        self.monitor_create_time = time.time()  # Time when the SaftyMonitor is created
    
    def is_focused(self) -> bool:
        '''
        Basic safty function to ensures the automation actions are only executed if the target application is focused.
        Passed into the execute() function in ActionSequence
        '''
        focused_pid = self.__get_focused_pid()
        
        # If PID == original APP's PID, return True
        if focused_pid == self.app_pid:
            return True
        
        # Else:
        #   Check if the PID is one of the processes that got created after this SaftyMonitor is created. If so, ignore and return True.
        #
        #   The only reason why this exist if because if the original application is a game launcher, then the launched game's PID will
        #   be untracked and this is the only way to improve safty.
        if len(self.cached_pids) == 0:
            time.sleep(10)
            self.cached_pids = self.__get_possible_pids()
            focused_pid = self.__get_focused_pid()
            
        return focused_pid in self.cached_pids
    
    
    def __get_focused_pid(self) -> int|None:
        result = subprocess.run([GET_FOCUSED_PID_EXE], capture_output=True, text=True)
    
        pid = None
        if result.returncode == 0:
            pid = result.stdout.strip()
        else:
            raise AmiyaBaseException(f"Embeded script 'GET_FOCUSED_PID' failed with return code {result.returncode}")
        
        try:
            pid = int(pid)
        except ValueError:
            raise AmiyaBaseException(f"Embeded script 'GET_FOCUSED_PID' failed to fetch PID. (Fetched PID {pid})")
    
        return pid
    
    
    def __get_possible_pids(self) -> set:
        '''
        Get all PIDs from processes that got created after the monitor is created. 
        '''
        return {p.pid for p in psutil.process_iter(['pid']) if p.create_time() > self.monitor_create_time}