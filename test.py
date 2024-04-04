# import pyautogui

# active_window_info = pyautogui.getActiveWindow()
# print(f"Current active/focused window: {active_window_info}")

from elevate import elevate; elevate()

import pyautogui
import time


print("starting in 5 secs...")
time.sleep(5)
pyautogui.click()
time.sleep(90)


ct = 0
try:
    while ct < 40:
        pyautogui.click()
        time.sleep(3)
        pyautogui.click()
        time.sleep(90)
        ct += 1
except KeyboardInterrupt:
    print("Program exited.")