import os
import re
import sys
from enum import Enum
from termcolor import colored
from amiya.utils.constants import BASENAME # "Amiya"

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

def atext(text: str, log_type: LogType = LogType.NORMAL):
    prefix = colored(BASENAME, "cyan")
    rtext = colored(text, log_type.value)
    return f"[{prefix}] {rtext}"

def aprint(text: str, log_type: LogType = LogType.NORMAL, end="\n", new_line_no_prefix=True):
    # The new_line_no_prefix param coupled with \n in the text param will put the
    # text after the new line character on the next line, but without a prefix.
    if "\n" in text and new_line_no_prefix == True:
        text = text.replace("\n", f"\n        ")
    
    rtext = atext(text, log_type)
    print(rtext, end=end, file=sys.stdout)
    sys.stdout.flush()
