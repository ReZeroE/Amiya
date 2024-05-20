import os
import re
import sys
import shutil
import threading
import pyautogui
import psutil
import pygetwindow as gw
import win32gui, win32process, psutil
from enum import Enum
from screeninfo import get_monitors
from datetime import datetime
from termcolor import colored
from amiya.utils import constants
from amiya.utils.constants import BASENAME, DATETIME_FORMAT, TIME_FORMAT, DEVELOPMENT # "Amiya"

def verify_platform() -> bool:
    """
    Verifies whether the OS is supported by the package.
    Package amiya currently only support the Windows OS.
    
    :return: true if running on Windows, false otherwise
    :rtype: bool
    """
    return os.name == "nt"

# =================================================
# =============| DEFAULT LOG TYPE | ===============
# =================================================

class LogType(Enum):
    NORMAL  = "white"
    SUCCESS = "green"
    WARNING = "yellow"
    ERROR   = "red"

def atext(text: str, log_type: LogType = LogType.NORMAL) -> str:
    prefix = colored(BASENAME, "cyan")
    rtext = colored(text, log_type.value)
    return f"[{prefix}] {rtext}"

def aprint(
    text: str, 
    log_type: LogType   = LogType.NORMAL, 
    end: str            = "\n", 
    submodule_name: str = "", 
    new_line_no_prefix  = True, 
    file                = sys.stdout, 
    flush               = True
):
    # The new_line_no_prefix param coupled with \n in the text param will put the
    # text after the new line character on the next line, but without a prefix.
    if "\n" in text and new_line_no_prefix == True:
        text = text.replace("\n", f"\n        ")
    
    submodule_name = Printer.to_purple(submodule_name)
    submodule_name = f"[{submodule_name}] "
    text = submodule_name + text
    
    rtext = atext(text, log_type)
    print(rtext, end=end, file=sys.stdout)
    sys.stdout.flush()

def color_cmd(text: str, with_quotes: bool = False):
    text = text.lower()
    
    if constants.CLI_MODE == True:
        text = text.replace("amiya ", "")
    else:
        if not text.startswith("amiya"):
            text = f"amiya {text}"
            
    colored_cmd = colored(text, "light_cyan")
    
    if with_quotes:
        return f"'{colored_cmd}'"
    return colored_cmd

# =================================================
# ============| CENTER TEXT HELPER | ==============
# =================================================

# DON"T CHANGE THE FOLLOWING TWO CENTER TEXT FUNCTIONS. I GOT THESE TO WORK AFTER HOURS. BOTH ARE NEEDED!

def center_text(text):
    terminal_width, terminal_height = shutil.get_terminal_size((80, 20))  # Default size
    
    lines = text.split('\n')
    max_width = max(len(line) for line in lines)
    left_padding = (terminal_width - max_width) // 2
    
    new_text = []
    for line in lines:
        new_text.append(' ' * left_padding + line)
    return "\n".join(new_text) 
        
def print_centered(text):
    def strip_ansi_codes(s):
        return re.sub(r'\x1B[@-_][0-?]*[ -/]*[@-~]', '', s)
    
    terminal_width = os.get_terminal_size().columns
    lines = text.split('\n')
    for line in lines:
        line_without_ansi = strip_ansi_codes(line)
        leading_spaces = (terminal_width - len(line_without_ansi)) // 2
        print(' ' * leading_spaces + line.strip())


# =================================================
# ==============| CUSTOM PRINTER | ================
# =================================================

class Printer:
    @staticmethod
    def hex_text(text, hex_color):
        
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

        rgb = hex_to_rgb(hex_color)
        escape_seq = f"\x1b[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m" # ANSI escape code for 24-bit (true color): \x1b[38;2;<r>;<g>;<b>m
        return f"{escape_seq}{text}\x1b[0m"

    @staticmethod
    def to_purple(text):
        return Printer.hex_text(text, "#a471bf")
        
    @staticmethod
    def to_skyblue(text):
        return Printer.hex_text(text, "#6dcfd1")
        
    @staticmethod
    def to_lightgrey(text):
        return Printer.hex_text(text, "#8a8a8a")

    @staticmethod
    def to_blue(text):
        return Printer.hex_text(text, "#6aa5fc")

    @staticmethod
    def to_lightblue(text):
        return Printer.hex_text(text, "#8ab1f2")
    
    @staticmethod
    def to_lightgreen(text):
        return Printer.hex_text(text, "#74d47b")
    
    @staticmethod
    def to_lightred(text):
        return Printer.hex_text(text, "#f27e82")

    

def bool_to_str(boolean: bool, true_text="Valid", false_text="Invalid"):
    CHECKMARK = "\u2713"
    CROSSMARK = "\u2717"
    if boolean:
        return Printer.to_lightgreen(f"{CHECKMARK} {true_text}")
    return Printer.to_lightred(f"{CROSSMARK} {false_text}")

# ========================================================
# =============| PERMISSION VERIFICATION | ===============
# ========================================================

import os
import sys
import platform

def is_admin() -> bool:
    try:
        # For Windows
        if platform.system().lower() == "windows":
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0

        # For Linux and MacOS
        else:
            return os.getuid() == 0  # os.getuid() returns '0' if running as root

    except Exception as e:
        aprint(f"Error checking administrative privileges: {e}", log_type=LogType.ERROR)
        return False


# ===================================================
# ================| PROGRESS BAR | ==================
# ===================================================

import time
def progressbar(it, prefix="", size=60, out=sys.stdout):
    count = len(it)
    start = time.time() # time estimate start
    def show(j):
        x = int(size*j/count)
        remaining = ((time.time() - start) / j) * (count - j)        
        mins, sec = divmod(remaining, 60) # limited to minutes
        time_str = f"{int(mins):02}:{sec:03.1f}"
        aprint(f"{prefix}|{u'█'*x}{(' '*(size-x))}| {int(j)}/{count}  -  Est. Wait {time_str}", end='\r', file=out, flush=True)
    show(0.1) # avoid div/0 
    for i, item in enumerate(it):
        yield item
        show(i+1)
    print("", flush=True, file=out)
    


# ===================================================
# ===============| SCREEN HELPER | ==================
# ===================================================

def clear_screen():
    os.system('cls')
    
    
# ===================================================
# ===============| PATH MODIFIER | ==================
# ===================================================

from pathlib import Path
def shorten_display_path(path: str):
    original_path = Path(path)
    if not original_path.exists():
        return path

    drive = original_path.drive
    first_directory = next(iter(original_path.parts[1:]), '')
    exe_name = original_path.name


    simplified_path = Path(drive, first_directory, '...', exe_name)
    simplified_path_str = str(simplified_path)

    return simplified_path_str

# ===================================================
# =============| DATETIME HANDLER | =================
# ===================================================

class DatetimeHandler:
    @staticmethod
    def get_datetime():
        return datetime.now().replace(microsecond=0)

    def get_datetime_str():
        return datetime.now().strftime(DATETIME_FORMAT)

    def get_time_str():
        return datetime.now().strftime(TIME_FORMAT)

    @staticmethod
    def datetime_to_str(datetime: datetime):
        return datetime.strftime(DATETIME_FORMAT)
    
    @staticmethod
    def str_to_datetime(datetime_str: str):
        return datetime.strptime(datetime_str, DATETIME_FORMAT)
    
    
    
# ===================================================
# ===========| MESSAGE WITH SPINNER | ===============
# ===================================================

class SpinnerMessage(threading.Thread):
    def __init__(self, start_message, end_message="", spin_delay=0.1):
        super().__init__()
        self.running = False
        self.start_message = start_message
        self.end_message = end_message
        self.spin_delay = spin_delay

    def verbose_start(self):
        self.running = True
        self.start()

    def verbose_end(self):
        self.running = False
        self.join()
        time.sleep(0.1)
        aprint(f"\n{self.end_message}")

    def end_run(self):
        self.running = False
        self.join()

    # Thread function only. Doen't call directly!!!!!!
    def run(self):
        try:
            while self.running:
                for char in '|/-\\':
                    aprint(self.start_message + " " + char, end="\r", file=sys.stdout)
                    sys.stdout.flush()
                    time.sleep(self.spin_delay)
        except KeyboardInterrupt:
            pass
        
# ===================================================
# ==============| TERMINAL RESIZE | =================
# ===================================================
        
import shutil

def get_terminal_size():
    cols, rows = shutil.get_terminal_size()
    return cols, rows


def resize_terminal(min_cols, min_rows):
    # Get the current size
    current_cols, current_rows = shutil.get_terminal_size()

    if current_cols < min_cols:
        # Set the desired size
        os.system(f'mode con: cols={min_cols+5} lines={current_rows}')
        
    if current_rows < min_rows:
        # Set the desired size
        os.system(f'mode con: cols={current_cols} lines={min_rows+5}')

# ===================================================
# ==============| TERMINAL RESIZE | =================
# ===================================================

class WindowUtils:

    @staticmethod
    def bring_to_foreground(pid):
        # Try to find the window associated with the PID
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['pid'] == pid:
                # Get all windows and check if any belong to the target process
                for window in gw.getAllWindows():
                    if window._hWnd == win32gui.FindWindow(None, window.title):
                        _, window_pid = win32process.GetWindowThreadProcessId(window._hWnd)
                        if window_pid == pid:
                            if window.isMinimized:
                                window.restore()
                            window.activate()
                            pyautogui.click(window.left + window.width // 2, window.top + window.height // 2)
                            return True
        return False

    @staticmethod
    def active_window_process_name():
        try:
            _, process_ids = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
            thread_id, pid = process_ids
            return (psutil.Process(pid).name(), thread_id, pid)
        except:
            return None

class ProcessHandler:

    @staticmethod
    def get_related_processes(process_pid: int):
        process = psutil.Process(process_pid)
        if not process.is_running():
            return None, None
        
        parent_procs: list[psutil.Process] = []
        children_procs: list[psutil.Process] = []
               
        try:
            parent_procs = process.parents()
            children_procs = process.children(recursive=True)
        except:
            pass

        return parent_procs, children_procs
    
    @staticmethod
    def kill_pid(pid):
        try:
            proc = psutil.Process(pid)
            if proc.is_running():
                proc.kill()
                return True
        
        except psutil.NoSuchProcess:
            if DEVELOPMENT:
                aprint(f"[DEV] Unabled to kill proc {pid} because it's already closed.")
        except Exception as ex:
            if DEVELOPMENT:
                aprint(f"[DEV] Unabled to kill proc {pid} ({ex}).")
        return False

    
    @staticmethod
    def kill_pids(pids: list[int], excluding_pids: list[int] = []):
        for pid in pids:
            if pid not in excluding_pids:
                ProcessHandler.kill_pid(pid)