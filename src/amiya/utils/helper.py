import os
import sys
from enum import Enum
from termcolor import colored

def check_platform():
    """
    Verifies whether the OS is supported by the package.
    Package starrail only support Windows installations of Honkai Star Rail.
    
    :return: true if running on Windows, false otherwise
    :rtype: bool
    """
    return os.name == "nt"

class LogType(Enum):
    NORMAL  = "white"
    SUCCESS = "green"
    WARNING = "yellow"
    ERROR   = "red"

def atext(text, log_type: LogType = LogType.NORMAL):
    prefix = colored("Amiya", "cyan")
    rtext = colored(text, log_type.value)
    return f"[{prefix}] {rtext}"
    
def aprint(text, log_type: LogType = LogType.NORMAL, end="\n"):
    rtext = atext(text, log_type)
    print(rtext, end=end, file=sys.stdout)
    sys.stdout.flush()
    
aprint("hello world", log_type=LogType.SUCCESS)