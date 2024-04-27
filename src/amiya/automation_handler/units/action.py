
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
    def __init__(self, *args):
        self.delay = ...
    
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
    def __init__(self, coor: tuple, delay: float, click: bool, window_info: dict):
        self.coordinate     = coor
        self.delay          = delay
        self.click          = click
        
        self.window_info    = window_info
        assert("width" in self.window_info)
        assert("height" in self.window_info)
        assert("is_fullscreen" in self.window_info)
 
    def execute(self):
        '''
        The delay represent the time lag between the current click and the previous click,
        therefore time.sleep() is executed at the start of a new action.
        '''
        
        x = self.coordinate[0]
        y = self.coordinate[1]
        pyautogui.moveTo(x, y, duration=0.1)
        
        if self.click:
            # pyautogui.click(interval=0.1)
            
            pyautogui.mouseDown()
            time.sleep(0.1)  
            pyautogui.mouseUp()
    
    def to_json(self):
        return {
            "coordinate": {
                "x": self.coordinate[0],
                "y": self.coordinate[1]
            },
            "delay": self.delay,
            "click": self.click,
            "window_info": self.window_info
        }
        
    def __repr__(self):
        return f"MouseAction(coor={self.coordinate}, delay={round(self.delay, 2)}, click={self.click})"


class KeyboardAction(Action):
    def __init__(self, key: str, delay: float):
        self.key = self.reformat_key(key)
        self.delay = delay
    
    def execute(self, keyboard):
        '''
        The delay represent the time lag between the current click and the previous click,
        therefore time.sleep() is executed at the start of a new action.
        '''
        
        self.press_key(self.key, keyboard)
    
    def to_json(self):
        return {
            "key": self.key,
            "delay": self.delay
        }
        
    def __repr__(self):
        return f"KeyboardAction(key={self.key}, delay={round(self.delay, 2)})"

    def press_key(self, key: str, pynput_keyboard: pynput.keyboard.Controller):
        '''
        This is going to be a difficult to explain, but essentially the string format keys
        recorded by pynput can't be re-recognized by pynput for execution. Therefore, a mapping
        between the string formated keys (collected by pynput itself) and the actual Key object
        is used to convert the key when trying to execute the keyboard action.
        
        There are going to be a wide range of keys that aren't supported including "hotkeys" or
        a combination of two different keys. This will need to be specified in the documentation.
        '''
        # TODO: find a better way to implement this, if possible
        pynput_key = PYNPUT_KEY_MAPPING.get(key, key)
        try:
            pynput_keyboard.press(pynput_key)
            time.sleep(0.05)
            pynput_keyboard.release(pynput_key)
        except (keyboard.Controller.InvalidKeyException, ValueError) as ex:
            # TODO: log this unsupported key as opposed to print it
            # print(f"Unsupported key: <{key}>")
            pass
        
    def reformat_key(self, key: keyboard.Key) -> str:
        key: str = str(key).strip().replace("'", "")
        
        removing = ["_r", "_gr", "_l"]
        for suffix in removing:
            if key.endswith(suffix):
                key = key.replace(suffix, "")

        return key
    