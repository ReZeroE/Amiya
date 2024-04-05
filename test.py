# import pyautogui

# active_window_info = pyautogui.getActiveWindow()
# print(f"Current active/focused window: {active_window_info}")

# from elevate import elevate; elevate()

# import pyautogui
# import time


# print("starting in 5 secs...")
# time.sleep(5)
# pyautogui.click()
# time.sleep(90)


# ct = 0
# try:
#     while ct < 40:
#         pyautogui.click()
#         time.sleep(3)
#         pyautogui.click()
#         time.sleep(90)
#         ct += 1
# except KeyboardInterrupt:
#     print("Program exited.")


# import schedule
# import time

# def my_task():
#     print("Running my scheduled task!")

# # Schedule the task to run daily at 10:30 AM
# schedule.every().day.at("13:51").do(my_task)

# while True:
#     schedule.run_pending()
#     time.sleep(1)

import os
import shutil

def print_centered(text):
    # Get the size of the terminal
    terminal_width, terminal_height = shutil.get_terminal_size((80, 20))  # Default size
    
    # Split the text into lines
    lines = text.split('\n')
    
    # Find the maximum width of the text block
    max_width = max(len(line) for line in lines)
    
    # Calculate the left padding to center the text
    left_padding = (terminal_width - max_width) // 2
    
    # Print each line with the necessary left padding
    for line in lines:
        print(' ' * left_padding + line)

text = r'''
      _    __  __ _____   __ _       ____ _     ___  
     / \  |  \/  |_ _\ \ / // \     / ___| |   |_ _| 
    / _ \ | |\/| || | \ V // _ \   | |   | |    | |  
   / ___ \| |  | || |  | |/ ___ \  | |___| |___ | |  
  /_/   \_\_|  |_|___| |_/_/   \_\  \____|_____|___| 
  
A lightweight cross-platform automation tool for daily tasks!
              https://github.com/ReZeroE/Amiya
                        By Kevin L.
'''

print_centered(text)