import os

# ==================================
# ==========| CONSTANTS | ==========
# ==================================
BASENAME        = "Amiya"
VERSION         = "0.0.2"
VERSION_DESC    = "Beta"

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
__AMIYA_DIRECTORY   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPS_DIRECTORY      = os.path.join(__AMIYA_DIRECTORY, "apps")
BIN_DIRECTORY       = os.path.join(__AMIYA_DIRECTORY, "bin")

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
CLI_MODE = False