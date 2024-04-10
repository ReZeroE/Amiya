
import re
import time
import pyautogui
import pynput
from pynput import keyboard
from abc import ABC, abstractclassmethod
from amiya.utils.pynput_mapping import PYNPUT_KEY_MAPPING

'''
Action: A single mouse of keyboard action.

Sequence: A list/sequence of Action objects.

ActionRecorder: Class for recording action sequences.

'''


class Action(ABC):
    @abstractclassmethod
    def __repr__(self):
        pass
    
    @abstractclassmethod
    def execute(self, *args):
        pass
    
    @abstractclassmethod
    def to_json(self):
        pass


class MouseAction(Action):
    def __init__(self, coor: tuple, delay: float, click: bool):
        self.coordinate = coor
        self.delay = delay
        self.click = click
        
    def execute(self, _):
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
        self.key = self.reformat_key(key)
        self.delay = delay
    
    def execute(self, keyboard):
        '''
        The delay represent the time lag between the current click and the previous click,
        therefore time.sleep() is executed at the start of a new action.
        '''
        
        time.sleep(self.delay)
        self.press_key(self.key, keyboard)
    
    def to_json(self):
        return {
            "key": self.key,
            "delay": self.delay
        }
        
    def __repr__(self):
        return f"KeyboardAction(key={self.key}, delay={self.delay})"

    def press_key(self, key: str, pynput_keyboard: pynput.keyboard.Controller):
        '''
        This is going to be difficult to explain, but essentially the keys are recorded using
        pynput and will be executed using pyautogui. The two packages uses different keyboard's key 
        formats. Unfortuanately I can't think of a better way implement this at the moment so here it is. 
        
        This will "forcefully" reformat the key value from pynput's version into something 
        accepted by pyautogui.  
        '''
        # TODO: not sure if I can, but find a better way to convert the keys into strings
        pynput_key = PYNPUT_KEY_MAPPING.get(key, key)
        
        try:
            pynput_keyboard.press(pynput_key)
            pynput_keyboard.release(pynput_key)
        except keyboard.Controller.InvalidKeyException:
            print(f"Unsupported key: <{key}>")
        
    def reformat_key(self, key: keyboard.Key) -> str:
        key: str = str(key).strip().replace("'", "")
        
        removing = ["_r", "_gr", "_l"]
        for suffix in removing:
            if key.endswith(suffix):
                key = key.replace(suffix, "")

        return key