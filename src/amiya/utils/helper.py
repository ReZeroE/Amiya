import os
import re
import sys
import shutil
from enum import Enum
from termcolor import colored
from amiya.utils.constants import BASENAME # "Amiya"

def check_platform():
    """
    Verifies whether the OS is supported by the package.
    Package amiya currently only support the Windows OS.
    
    :return: true if running on Windows, false otherwise
    :rtype: bool
    """
    return os.name == "nt"

class LogType(Enum):
    NORMAL  = "white"
    SUCCESS = "green"
    WARNING = "yellow"
    ERROR   = "red"

def atext(text: str, log_type: LogType = LogType.NORMAL):
    prefix = colored(BASENAME, "cyan")
    rtext = colored(text, log_type.value)
    return f"[{prefix}] {rtext}"

def aprint(text: str, log_type: LogType = LogType.NORMAL, end="\n", new_line_no_prefix=True, file=sys.stdout, flush=True):
    # The new_line_no_prefix param coupled with \n in the text param will put the
    # text after the new line character on the next line, but without a prefix.
    if "\n" in text and new_line_no_prefix == True:
        text = text.replace("\n", f"\n        ")
    
    rtext = atext(text, log_type)
    print(rtext, end=end, file=sys.stdout)
    sys.stdout.flush()

def print_centered(text):
    terminal_width, terminal_height = shutil.get_terminal_size((80, 20))  # Default size
    
    lines = text.split('\n')
    max_width = max(len(line) for line in lines)
    left_padding = (terminal_width - max_width) // 2
    
    for line in lines:
        print(' ' * left_padding + line)
        
        
import os
import sys
import platform

def is_admin():
    try:
        # For Windows
        if platform.system().lower() == "windows":
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0

        # For Linux and MacOS
        else:
            return os.getuid() == 0  # os.getuid() returns '0' if running as root

    except Exception as e:
        print(f"Error checking administrative privileges: {e}")
        return False



import time
def progressbar(it, prefix="", size=60, out=sys.stdout):
    count = len(it)
    start = time.time() # time estimate start
    def show(j):
        x = int(size*j/count)
        remaining = ((time.time() - start) / j) * (count - j)        
        mins, sec = divmod(remaining, 60) # limited to minutes
        time_str = f"{int(mins):02}:{sec:03.1f}"
        aprint(f"{prefix}[{u'█'*x}{('.'*(size-x))}] {int(j)}/{count}  -  Est. Wait {time_str}", end='\r', file=out, flush=True)
    show(0.1) # avoid div/0 
    for i, item in enumerate(it):
        yield item
        show(i+1)
    print("", flush=True, file=out)