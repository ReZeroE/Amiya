import pyautogui

class ContinuousClickController:
    def __init__(self):
        pass
    
    def click_continuously(self, count: int, delay: float):
        pyautogui.press()
        pyautogui.release()