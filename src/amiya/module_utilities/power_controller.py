import os
import time
import subprocess
from enum import Enum

from amiya.utils.helper import *
from amiya.exceptions.exceptions import *

class PowerType(Enum):
    Shutdown = 0
    Sleep    = 1


# This command requires administrator privileges and must be executed from an elevated command prompt.
class PowerUtils:
    def __init__(self):
        pass
        

    def wait(self, delay: int, type: PowerType):
        buffer_space = " "*5
        
        delay = self.__parse_int(delay)
        st_time = curr_time = time.time()
        
        while curr_time - st_time < delay:
            curr_time = time.time()
            time.sleep(0.01)
            aprint(f"{type.name} Countdown: {round(delay - (curr_time - st_time), 2)}{buffer_space}", end="\r")
        print("\n")
        
    def run_confirmation(self, delay: int, type: PowerType):
        aprint(f"This machine will {type.name.lower()} after {delay} seconds. Proceed? [y/n] ", end="")
        if input().lower().strip() == "y":
            return True
        return False
        
    def sleep_pc(self, delay: int):
        if self.run_confirmation(delay, PowerType.Sleep) == True:
            self.wait(delay, PowerType.Sleep)
            
            ret = 0
            try:
                ret = self.__sleep()
            except Exception as ex:
                raise AmiyaBaseException(f"Sleep failed to execute due to {ex} with error code {ret}")
        
    def shutdown_pc(self, delay: int):
        if self.run_confirmation(delay, PowerType.Shutdown) == True:
            self.wait(delay, PowerType.Shutdown)
            self.__shutdown()


    def __sleep(self) -> int:
        return os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

    def __shutdown(self):
        os.system(f"shutdown /s /t 0")

    def __parse_int(self, delay):
        if isinstance(delay, int):
            return delay
        
        if isinstance(delay, str):
            try:
                return int(delay.strip())
            except ValueError:
                aprint("Please input an integer as the delay."); exit()
        
        raise AmiyaBaseException(f"Type {type(delay)} ({delay}) delay not supported.")
             
    def __check_hibernation_status():
        if not is_admin():
            aprint("This command requires administrator privileges and must be executed from an elevated command prompt.", log_type=LogType.ERROR)
            return
        
        result = subprocess.run(["powercfg", "/a"], capture_output=True, text=True)
        if "Hibernate" in result.stdout:
            return True
        return False