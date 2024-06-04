import os

# ==================================
# ==========| CONSTANTS | ==========
# ==================================
BASENAME        = "Amiya"
COMMAND         = "amiya"
VERSION         = "0.0.4"
VERSION_DESC    = "Beta"
DEVELOPMENT     = VERSION_DESC.lower() != "stable"

CONFIG_NAME     = "Amiya Config"
TIME_FORMAT     = "%H:%M:%S"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# DO NOT REMOVE/MODIFY THESE VALUES (critical to the program's execution)
FORCE_ACTIONS_DELAY = 0.0

AUTHOR          = "Kevin L."
AUTHOR_DETAIL   = f"{AUTHOR} - kevinliu@vt.edu - Github: ReZeroE"
REPOSITORY      = "https://github.com/ReZeroE/Amiya"

# ==================================
# ============| PATHS | ============
# ==================================
HOME_DIRECTORY      = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

PYTHON_MODULE_PATH = os.path.join(HOME_DIRECTORY, "site-packages", "amiya")
if os.path.exists(PYTHON_MODULE_PATH):
    # If the module is built using `pip install .`, then the path would be something like C:/PythonXXX/Lib/site-packages/<package_name>
    HOME_DIRECTORY = PYTHON_MODULE_PATH
    __AMIYA_DIRECTORY = PYTHON_MODULE_PATH
else:
    # Else if the module is built locally using `pip install -e .`, then the path will be the local directory structure
    __AMIYA_DIRECTORY   = os.path.join(HOME_DIRECTORY, "src", "amiya")

APPS_DIRECTORY      = os.path.join(__AMIYA_DIRECTORY, "apps")
RAW_AUTO_DIRECTORY  = os.path.join(__AMIYA_DIRECTORY, "raw_automations")
BIN_DIRECTORY       = os.path.join(__AMIYA_DIRECTORY, "bin")

# Development Only
BACKUP_APPS_DIRECTORY = os.path.join(__AMIYA_DIRECTORY, "apps_backup")

# ==================================
# =========| EXECUTABLES | =========
# ==================================
FOCUS_PID_EXE           = os.path.join(BIN_DIRECTORY, "focus_pid.exe")
GET_FOCUSED_PID_EXE     = os.path.join(BIN_DIRECTORY, "get_active_pid.exe")
GET_WINDOW_SIZE_EXE     = os.path.join(BIN_DIRECTORY, "get_window_size.exe")

# ==================================
# ============| GLOBAL | ===========
# ==================================

# Global variable to identify whether the program is in CLI mode
# MUST BE USED AS constants.CLI_MODE (only this accesses the re-bind value)
CLI_MODE    = False
AMIYA_PID   = os.getpid()

# ===============================================
# ============| PYNPUT KEY MAPPINGS | ===========
# ===============================================
from pynput.keyboard import Key
PYNPUT_KEY_MAPPING = {
    'Key.esc'       : Key.esc,
    'Key.space'     : Key.space,
    'Key.backspace' : Key.backspace,
    'Key.enter'     : Key.enter,
    
    'Key.tab': Key.tab,
    'Key.caps_lock': Key.caps_lock,
    'Key.shift': Key.shift,
    'Key.ctrl': Key.ctrl,
    'Key.alt': Key.alt,
    
    'Key.delete': Key.delete,
    'Key.end': Key.end,
    'Key.home': Key.home,
    
    'Key.f1': Key.f1,
    'Key.f2': Key.f2,
    'Key.f3': Key.f3,
    'Key.f4': Key.f4,
    'Key.f5': Key.f5,
    'Key.f6': Key.f6,
    'Key.f7': Key.f7,
    'Key.f8': Key.f8,
    'Key.f9': Key.f9,
    'Key.f10': Key.f10,
    'Key.f11': Key.f11,
    'Key.f12': Key.f12,
    
    'Key.page_down': Key.page_down,
    'Key.page_up': Key.page_up,
    
    'Key.up': Key.up,
    'Key.down': Key.down,
    'Key.left': Key.left,
    'Key.right': Key.right,
    
    'Key.media_play_pause': Key.media_play_pause,
    'Key.media_volume_mute': Key.media_volume_mute,
    'Key.media_volume_up': Key.media_volume_up,
    'Key.media_volume_down': Key.media_volume_down,
    'Key.media_previous': Key.media_previous,
    'Key.media_next': Key.media_next,
    'Key.insert': Key.insert,
    'Key.menu': Key.menu,
    'Key.num_lock': Key.num_lock,
    'Key.pause': Key.pause,
    'Key.print_screen': Key.print_screen,
    'Key.scroll_lock': Key.scroll_lock
}