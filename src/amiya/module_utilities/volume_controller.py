import sys
import customtkinter as ctk
from pycaw.pycaw import AudioUtilities
import multiprocessing
import subprocess

from amiya.utils.helper import aprint

class ConfirmDialog(ctk.CTkToplevel):
    def __init__(self, parent, title, message, callback):
        super().__init__(parent)
        self.title(title)
        self.geometry("350x150")
        self.callback = callback
        self.protocol("WM_DELETE_WINDOW", self.on_no)  # Handle the window close button click
        self.already_destroyed = False  # Flag to track destruction status

        self.position_next_to_parent()
        self.create_widgets(message)

    def position_next_to_parent(self):
        parent_x = self.master.winfo_x() + 10
        parent_y = self.master.winfo_y()
        parent_width = self.master.winfo_width()
        window_width = 350
        window_height = 150

        # Position right next to the parent window
        x_coordinate = parent_x + parent_width
        y_coordinate = parent_y

        self.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    def create_widgets(self, message):
        label = ctk.CTkLabel(self, text=message, wraplength=280)
        label.pack(pady=20, padx=20)

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=20)

        yes_button = ctk.CTkButton(button_frame, text="Yes", command=self.on_yes)
        yes_button.pack(side="left", padx=10)
        no_button = ctk.CTkButton(button_frame, text="No", command=self.on_no)
        no_button.pack(side="left", padx=10)

    def on_yes(self):
        if self.winfo_exists() and not self.already_destroyed:
            self.callback(True)
            self.deferred_destroy()

    def on_no(self):
        if self.winfo_exists() and not self.already_destroyed:
            self.callback(False)
            self.deferred_destroy()

    def deferred_destroy(self):
        """ Defer the destruction of the window to ensure all operations complete. """
        self.already_destroyed = True
        self.after(100, self.destroy)  # Delay destruction

class AmiyaVolumeControllerUI(ctk.CTk):
    def __init__(self):
        self.volumes = dict()
        
        super().__init__()
        self.title('Application Volume Control')

        ctk.set_appearance_mode("dark")  # or "light"
        ctk.set_default_color_theme("blue")  # general theme

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)

        self.apps = self.init_volume_controls()
        
        self.after_id = self.after(1000, self.scheduled_update)  # Schedule an update every 1000ms

        # Dynamically set the window size based on the number of applications
        window_height = min(600, max(200, 80 * len(self.apps)))
        self.geometry(f'400x{window_height}')

        # Bind the close event to a custom handler
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.attributes('-topmost', True)
        
        

    def init_volume_controls(self):
        sessions = AudioUtilities.GetAllSessions()
        apps = []
        for session in sessions:
            if session.Process:
                volume = session.SimpleAudioVolume
                apps.append(session.Process.name())  # Keep track of apps for dynamic sizing

                label = ctk.CTkLabel(self.frame, text=session.Process.name())
                label.pack(pady=(10, 0))  # Provide some padding above the label

                # Create a slider that defaults to the current volume
                volume_control = ctk.CTkSlider(self.frame, from_=0, to=100,
                                               command=lambda value, vol=volume: self.set_volume(value, vol))
                volume_control.set(volume.GetMasterVolume() * 100)
                volume_control.pack(pady=5)
                self.volumes[session.Process.name()] = (volume_control, volume)
        return apps

    def set_volume(self, value, volume):
        volume.SetMasterVolume(float(value) / 100, None)

    def on_close(self):
        aprint("Closing application volume control GUI...")
        
        if self.winfo_exists():
            reset_needed = any(vol.GetMasterVolume() < 1.0 for _, (slider, vol) in self.volumes.items())
            if reset_needed:
                def reset_all_volume(response):
                    if response:
                        for _, (slider, volume) in self.volumes.items():
                            volume.SetMasterVolume(1.0, None)  # Set volume to 100%
                    if self.winfo_exists():  # Check again before closing
                        self.destroy()
                    if self.after_id:
                        self.after_cancel(self.after_id)
        
                text = "Not all volumes are set at 100%. Reset all applications' volumes to 100% before exiting?"
                dialog = ConfirmDialog(self, "Volume Reset", text, callback=reset_all_volume)
                dialog.grab_set()
            
            else:
                if self.after_id:
                    self.after_cancel(self.after_id)
                self.destroy()

    def scheduled_update(self):
        try:
            if self.winfo_exists():
                pass
            else:
                self.after_cancel(self.after_id)
        except Exception as e:
            print(f"Error during scheduled update: {e}")
            self.after_cancel(self.after_id)

def start_volume_control_ui():
    aprint("Starting application volume control GUI...")
    app_ui = AmiyaVolumeControllerUI()
    app_ui.mainloop()


## DON"T USE THIS FOR NOW
def start_volume_control_ui_detached():
    # Command to run the Python script in a detached process
    python_executable = sys.executable
    creation_flags = subprocess.DETACHED_PROCESS
    subprocess.Popen([python_executable, __file__], creationflags=creation_flags)



# if __name__ == '__main__':
#     # gui_process = multiprocessing.Process(target=start_volume_control_ui)
#     # gui_process.start()
#     # gui_process.join()