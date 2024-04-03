import time
import pyautogui

class MouseAction:
    def __init__(self, coor: tuple, delay: float, click: bool):
        self.coordinate = coor
        self.delay = delay
        self.click = click
        
    def execute(self):
        '''
        The delay represent the time lag between the current click and the previous click,
        therefore time.sleep() is executed at the start of a new action.
        '''
        time.sleep(self.delay) 
        
        x = self.coordinate[0]
        y = self.coordinate[1]
        pyautogui.moveTo(x, y, duration=0.1)
        
        if self.click:
            pyautogui.click()  
           
        
    
    def to_json(self):
        return {
            "coordinate": {
                "x": self.coordinate[0],
                "y": self.coordinate[1]
            },
            "delay": self.delay,
            "click": self.click
        }
        
    def __repr__(self):
        return f"MouseAction(coor={self.coordinate}, delay={self.delay}, click={self.click})"
