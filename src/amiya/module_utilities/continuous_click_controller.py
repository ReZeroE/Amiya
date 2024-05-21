import time
import pyautogui
from pynput import keyboard
from threading import Event

from amiya.exceptions.exceptions import AmiyaExit
from amiya.utils.helper import aprint

class ContinuousClickController:
    def __init__(self):
        self.thread_event = Event()
        self.pause = False
    
    def click_continuously(
        self, 
        count: int = -1, 
        interval: float = 1.0, 
        hold_time: float = 0.1, 
        start_after: float = 5.0,
        quite: bool = False
    ):
        
        aprint(f"Uniform clicking starting in {start_after} seconds, press ESC key anytime to stop...\nClick count: {"INF" if count == -1 else count}\Interval between clicks: {interval} seconds\nTime between press and release: {hold_time} seconds\nQuite: {quite}")
        
        listener = keyboard.Listener(on_press=self.__on_press)
        listener.start()
        
        time.sleep(start_after)
        
        try:
            click_count = 0
            while True:
                if click_count == count:
                    break
                
                if self.thread_event.is_set():
                    break
                
                if self.pause:
                    time.sleep(0.1)
                    continue
                
                if not quite:
                    buffer = " " * 10
                    x, y = pyautogui.position()
                    aprint(f"[{click_count+1}/{"INF" if count == -1 else count}] Clicking ({x}, {y})...{buffer}", end="\r")
                
                pyautogui.mouseDown()
                self.__click(hold_time, interval)
                click_count += 1
                
                
                
        except KeyboardInterrupt:
            print("")
            listener.stop()
            raise AmiyaExit()
    
    def __click(self, hold_time, interval):
        pyautogui.mouseDown()
        time.sleep(hold_time)
        pyautogui.mouseUp()
        time.sleep(interval)
                
    def __on_press(self, button):
        if button == keyboard.Key.esc:
            aprint("\nEsc key pressed, stopping...")
            self.thread_event.set()
            
        if button == keyboard.Key.space:
            self.pause = not self.pause
            
            buffer = " " * 7
            if self.pause == True:
                aprint(f"Clicks paused. Press space again to start.{buffer}", end="\r")
            else:
                aprint(f"Clicks unpaused. Press space again to pause.{buffer}", end="\r")