import sys
import customtkinter as ctk
from pycaw.pycaw import AudioUtilities
import multiprocessing
import subprocess

from amiya.utils.helper import aprint

class AmiyaVolumeControllerUI(ctk.CTk):
    def __init__(self):
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
        return apps

    def set_volume(self, value, volume):
        volume.SetMasterVolume(float(value) / 100, None)

    def on_close(self):
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
    aprint("Starting application volume control UI...")
    app_ui = AmiyaVolumeControllerUI()
    app_ui.mainloop()

def start_volume_control_ui_detached():
    # Command to run the Python script in a detached process
    python_executable = sys.executable
    creation_flags = subprocess.DETACHED_PROCESS
    subprocess.Popen([python_executable, __file__], creationflags=creation_flags)



# if __name__ == '__main__':
#     # gui_process = multiprocessing.Process(target=start_volume_control_ui)
#     # gui_process.start()
#     # gui_process.join()