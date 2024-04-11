import time
from pynput import mouse, keyboard

from amiya.automation_handler.actions_controller.units.action import Action, MouseAction, KeyboardAction
from amiya.automation_handler.actions_controller.units.sequence import ActionsSequence

from amiya.utils.helper import *

class ActionsRecorder():
    def __init__(self, new_sequence_name):
        self.sequence = ActionsSequence(new_sequence_name)
        self.sequence.set_date_created_to_current()
        
        self.last_click_time = None
        self.is_recording = False
        
        
    def record(self):
        # from elevate import elevate; elevate()
        aprint("Recording starting after the UP-ARROW key is pressed.", log_type=LogType.WARNING)
        
        mouse_listener = mouse.Listener(on_click=self.__on_mouse_action)
        keyboard_listener = keyboard.Listener(on_press=self.__on_keyboard_action)
        
        with mouse.Listener(on_click=self.__on_mouse_action) as mouse_listener, \
            keyboard.Listener(on_press=self.__on_keyboard_action) as keyboard_listener:
            keyboard_listener.join()
            
        self.sequence.print_sequence()
        time.sleep(1)
    
    def __on_mouse_action(self, x, y, button, pressed):
        if self.is_recording and pressed:
            now = time.time()
            delay = now - self.last_click_time if self.last_click_time else float(0)
            clicked = button == mouse.Button.left # If left is clicked, the click is registered as "clicked", else if right is clicked, only the mouse movement will be registered.
            self.sequence.add(MouseAction((x, y), delay, clicked))
            self.last_click_time = now

    def __on_keyboard_action(self, key):
        if key == keyboard.Key.up and self.is_recording == False:
            aprint("Recording in-progress (press the UP-ARROW key again to stop)...")
            self.is_recording = True                                    # Start recording on up key press
        elif key == keyboard.Key.up and self.is_recording == True:
            self.is_recording = False
            return False                                                # Stop listener on Enter key press (2nd time)

        if self.is_recording:                                           # Record only if is_recording is set to True
            now = time.time()
            delay = now - self.last_click_time if self.last_click_time else float(0)
            self.sequence.add(KeyboardAction(key, delay))
            self.last_click_time = now
        
if __name__ == "__main__":
    ar = ActionsRecorder() 
    ar.record()