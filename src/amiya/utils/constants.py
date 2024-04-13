import os

# ==================================
# ==========| CONSTANTS | ==========
# ==================================
BASENAME        = "Amiya"
CONFIG_NAME     = "Amiya Config"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

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