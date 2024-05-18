import os
import time
import psutil
import subprocess
from amiya.utils.helper import *
from amiya.utils.constants import GET_FOCUSED_PID_EXE, DEVELOPMENT
from amiya.exceptions.exceptions import AmiyaBaseException, Amiya_AppNotFocusedException, AmiyaExit

class SafetyMonitor:
    def __init__(self, app_process: psutil.Process):
        self.app_process = app_process
        self.cached_pids: set[int] = set()
        self.monitor_create_time = time.time()  # Time when the SafetyMonitor is created
    
    def app_is_focused(self) -> bool:
        '''
        Basic safety function to ensures the automation actions are only executed if the target application is focused.
        Passed into the execute() function in ActionSequence
        '''
        focused_pid = SafetyMonitor.get_focused_pid()
        
        # If PID == original APP's PID, return True
        if focused_pid == self.app_process.pid:
            return True

        if focused_pid not in self.cached_pids:
            self.__update_cached_pids()  # Update the cache if PID not found initially
            
            if focused_pid not in self.cached_pids:
                if DEVELOPMENT:
                    print("")
                    aprint(f"Focused PID: {focused_pid}, Original App PID: {self.app_process.pid}, Cached PIDs: {self.cached_pids}", log_type=LogType.ERROR, new_line_no_prefix=False)
                raise Amiya_AppNotFocusedException()
            else:
                return True
        else:
            return True
        

    
    def __update_cached_pids(self):
        # If the inital process is still running
        try:
            children_pids = set(proc.pid for proc in self.app_process.children(recursive=True))                  # Get children PIDs
            parents_pids = set(proc.pid for proc in self.app_process.parents() if proc.pid != os.getpid())       # Get parent PIDs
            self.cached_pids = children_pids.union(parents_pids)
        
        # If the inital proecss is killed
        except psutil.NoSuchProcess:
            pass
        
        
    
    
    @staticmethod
    def get_focused_pid(tries: int = 3) -> int|None:
        # :param tries: specifies how many times to try on failed PID fetch attempts
        if tries <= 0:
            aprint(f"ERROR: get_focuse_pid() cannot be called with {tries} tries.", log_type=LogType.ERROR)
            raise AmiyaExit()
        
    
        pid = None
        for _ in range(tries):
            result = subprocess.run([GET_FOCUSED_PID_EXE], capture_output=True, text=True)
            if result.returncode == 0:
                pid = result.stdout.strip()
                break
            time.sleep(1)
            
        if pid == None:
            raise AmiyaBaseException(f"Embeded script 'GET_FOCUSED_PID' failed after {tries} tries with return code {result.returncode}")
        
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
        
        return {p.pid for p in psutil.process_iter(['pid']) if p.create_time() > self.monitor_create_time}