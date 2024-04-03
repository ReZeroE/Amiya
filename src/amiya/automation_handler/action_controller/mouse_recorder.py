import time
from pynput import mouse, keyboard
from automation_handler.action_controller.mouse_action import MouseAction

class ActionRecorder():
    def __init__(self):
        self.actions: list[MouseAction] = []
        self.last_click_time = None
        self.is_recording = False
        
    def record(self):
        print("Recording starting after enter key is pressed.")
        
        mouse_listener = mouse.Listener(on_click=self.__on_click)
        keyboard_listener = keyboard.Listener(on_press=self.__on_press)
        
        with mouse.Listener(on_click=self.__on_click) as mouse_listener, keyboard.Listener(on_press=self.__on_press) as keyboard_listener:
            
            keyboard_listener.join()
            for action in self.actions:
                print(action)
            
        time.sleep(1)
    
    def __on_click(self, x, y, button, pressed):
        if self.is_recording and pressed:
            now = time.time()
            delay = now - self.last_click_time if self.last_click_time else float(0)
            clicked = button == mouse.Button.left # If left is clicked, the click is registered as "clicked", else if right is clicked, only the mouse movement will be registered.
            self.actions.append(MouseAction((x, y), delay, clicked))
            self.last_click_time = now

    def __on_press(self, key):
        if key == keyboard.Key.enter:
                print("Recording in-progress...")
                self.is_recording = True    # Start recording on Enter key press
        elif key == keyboard.Key.space:
            self.is_recording = False       # Optional: Use to pause recording instead of stopping
            return False  # Stop listener
