import time
import threading
import tkinter as tk
from pynput import mouse, keyboard

from amiya.automation_handler.units.action import Action, MouseAction, KeyboardAction
from amiya.automation_handler.units.sequence import AutomationSequence
from amiya.apps_manager.safety_monitor import SafetyMonitor
from amiya.pixel_calculator.resolution_detector import ResolutionDetector

from amiya.utils.helper import *
from amiya.exceptions.exceptions import *

class AutomationRecorder():
    def __init__(self, sequence: AutomationSequence, safety_monitor: SafetyMonitor):
        self.sequence = sequence
        self.safety_monitor = safety_monitor
        
        self.last_click_time = None
        self.is_recording = False
        
        self.stop_event = threading.Event()
        self.label = None
        
        
    def stop_recording(self, root: tk.Tk):
        self.stop_event.set()
        self.is_recording = False
        self.sequence.actions = self.sequence.actions[:-1]    # Remove the last key click (user clicks on the Stop Recording button)
        root.quit()
    
    def create_indicator_window(self):
        LENGTH = 300
        WIDTH = 400
        
        root = tk.Tk()
        root.title("Recording...")
        root.geometry(f"{WIDTH}x{LENGTH}+400+400")
        root.overrideredirect(True)  # Remove window decorations

        root.attributes('-topmost', True) # STAY ON TOOOOOPPPPPP

        # Set the overall background color to black and then make it transparent
        background_color = 'black'
        root.configure(bg=background_color)
        root.attributes('-transparentcolor', background_color)

        canvas = tk.Canvas(root, bg=background_color, highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)

        # Replace 'black' with the color of your choice for the rounded rectangle
        canvas_color = '#333333'
        radius = 10
        canvas.create_polygon(
            [
                radius,             0,                  WIDTH - radius,     0, 
                WIDTH,              radius,             WIDTH,              LENGTH - radius, 
                WIDTH - radius,     LENGTH,             radius,             LENGTH, 
                0,                  LENGTH - radius,    0,                  radius
            ],
            smooth=True, fill=canvas_color)

        self.label = tk.Label(canvas, text="Recording...", font=('Helvetica', 11), fg='#FFFFFF', bg=canvas_color)
        self.label.place(relx=0.5, rely=0.4, anchor='center')

        stop_button = tk.Button(canvas, text='Stop Recording', command=lambda: self.stop_recording(root), bg='#14628c', fg='#FFFFFF')
        stop_button.place(relx=0.5, rely=0.8, anchor='center', width=200)

        # stop_button_2 = tk.Button(canvas, text='Terminate Recording', command=self.stop_recording, bg='#14628c', fg='#FFFFFF')
        # stop_button_2.place(relx=0.5, rely=0.95, anchor='center', width=200)

        # Mouse movement handling
        def on_press(event):
            root._drag_start_x = event.x
            root._drag_start_y = event.y

        def on_drag(event):
            dx = event.x - root._drag_start_x
            dy = event.y - root._drag_start_y
            x = root.winfo_x() + dx
            y = root.winfo_y() + dy
            root.geometry(f"+{x}+{y}")

        root.bind('<Button-1>', on_press)
        root.bind('<B1-Motion>', on_drag)

        self.label.config(text=f"Recording...")

        root.mainloop()
        
        
    def record(self, start_on_callback=False) -> AutomationSequence:
        threading.Thread(target=self.create_indicator_window, daemon=True).start()
        
        if start_on_callback:
            self.is_recording = True
            self.last_click_time = time.time()
            aprint("Recording in-progress (press the 'Stop Recording' button or the UP-ARROW key to stop)...")
        else:
            raise AmiyaBaseException("Record must start on callback. Other case not implemented.")
        
        mouse_listener = mouse.Listener(on_click=self.__on_mouse_action)
        keyboard_listener = keyboard.Listener(on_press=self.__on_keyboard_action)
        
        with mouse.Listener(on_click=self.__on_mouse_action) as mouse_listener, \
            keyboard.Listener(on_press=self.__on_keyboard_action) as keyboard_listener:
            
            mouse_listener_thread     = threading.Thread(target=mouse_listener.join)
            keyboard_listener_thread  = threading.Thread(target=keyboard_listener.join)
            
            mouse_listener_thread.start()
            keyboard_listener_thread.start()

            # Wait until stop recording event is triggered
            self.stop_event.wait()

            # Stop listeners
            mouse_listener.stop()
            keyboard_listener.stop()

            # Wait for listeners to finish
            mouse_listener_thread.join()
            keyboard_listener_thread.join()

        time.sleep(0.3)
        return self.sequence
    
    def __on_mouse_action(self, x, y, button, pressed):
        if self.is_recording and pressed:
            now = time.time()
            delay = now - self.last_click_time if self.last_click_time else float(0)
            clicked = button == mouse.Button.left # If left is clicked, the click is registered as "clicked", else if right is clicked, only the mouse movement will be registered.
            self.sequence.add(MouseAction((x, y), delay, clicked, ResolutionDetector.get_window_size()))
            self.last_click_time = now
            self.on_mouse_action_update_window(x, y, delay)

    def __on_keyboard_action(self, key):
        if key == keyboard.Key.up and self.is_recording == True:        # Stop listener on Enter key press
            self.stop_recording()
            return False

        if self.is_recording:                                           # Record only if is_recording is set to True
            now = time.time()
            delay = now - self.last_click_time if self.last_click_time else float(0)
            self.sequence.add(KeyboardAction(key, delay))
            self.last_click_time = now
            self.on_keyboard_action_update_window(key, delay)
        
    
    def on_mouse_action_update_window(self, x, y, delay):
        if self.label:
            self.update_label(text=f"Mouse Click Detected - ({x}, {y})\nDelay: {round(delay, 2)}")

    def on_keyboard_action_update_window(self, key, delay):
        if self.label:
            try:
                self.update_label(text=f"Key Detected - '{key.char}'\nDelay: {round(delay, 2)}")
            except AttributeError:
                self.update_label(text=f"Key Detected - '{key}'\nDelay: {round(delay, 2)}")


    def update_label(self, text: str):
        self.label.config(text=f"Recording...\nTotal Actions Recorded: {len(self.sequence.actions)}\n\n{text}\n")

