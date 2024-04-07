import time
import pyautogui
from abc import ABC, abstractclassmethod

class Action(ABC):
    @abstractclassmethod
    def __repr__(self):
        pass
    
    @abstractclassmethod
    def execute(self):
        pass
    
    @abstractclassmethod
    def to_json(self):
        pass

class MouseAction(Action):
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


class KeyboardAction(Action):
    def __init__(self, key: str, delay: float):
        self.key = key
        self.delay = delay
    
    def execute(self):
        '''
        The delay represent the time lag between the current click and the previous click,
        therefore time.sleep() is executed at the start of a new action.
        '''
        time.sleep(self.delay) 
        pyautogui.press(self.key)
           
    def to_json(self):
        return {
            "key": self.key,
            "delay": self.delay
        }
        
    def __repr__(self):
        return f"KeyboardAction(key={self.key}, delay={self.delay})"
