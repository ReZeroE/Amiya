import os

BASENAME = "Amiya Arknights Assistant"
CONFIG_NAME = "Amiya Config"

__AMIYA_DIRECTORY   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPS_DIRECTORY      = os.path.join(__AMIYA_DIRECTORY, "apps")
BIN_DIRECTORY       = os.path.join(__AMIYA_DIRECTORY, "bins")

FOCUS_PID_EXE       = os.path.join(BIN_DIRECTORY, "focus_pid.exe")