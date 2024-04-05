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

import webbrowser
search_terms = [" hello world"]

# ... construct your list of search terms ...

for term in search_terms:
    url = "https://www.google.com.tr/search?q={}".format(term)
    webbrowser.open_new_tab(url)