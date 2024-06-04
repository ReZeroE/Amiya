import os
import sys
import customtkinter as ctk
from pycaw.pycaw import AudioUtilities
import subprocess

from amiya.exceptions.exceptions import AmiyaExit
from amiya.utils.helper import aprint, SpinnerMessage

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
    def __init__(self, spin_msg: SpinnerMessage):
        self.volumes = dict()
        self.spin_msg = spin_msg
        self.auto_reload_enabled = True  # Flag to control auto reload

        super().__init__()
        self.title('Application Volume Control')

        ctk.set_appearance_mode("dark")  # or "light"
        ctk.set_default_color_theme("blue")  # general theme

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)

        self.apps = self.init_volume_controls()
        
        # self.after_id = self.after(1000, self.scheduled_update)  # Schedule an update every 1000ms

        # Dynamically set the window size based on the number of applications
        window_height = min(500, max(250, 95 * len(self.apps) + 50))
        self.geometry(f'400x{window_height}')

        # Add refresh button at the bottom
        self.refresh_button = ctk.CTkButton(self, text="Refresh", command=self.refresh_apps)
        self.refresh_button.pack(pady=(10, 20))

        # Bind the close event to a custom handler
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.attributes('-topmost', True)
        
        self.set_icon()
        self.spin_msg.verbose_start()

    def set_icon(self):
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources', "amiya.ico")
        print(icon_path)
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)

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
        self.spin_msg.verbose_end()
        
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

    # def scheduled_update(self):
    #     try:
    #         if self.winfo_exists() and self.auto_reload_enabled:
    #             self.update_apps()  # Update the list of apps
    #             self.after_id = self.after(1000, self.scheduled_update)  # Schedule the next update
    #     except Exception as e:
    #         print(f"Error during scheduled update: {e}")
    #         self.after_cancel(self.after_id)
            
    def refresh_apps(self):
        self.auto_reload_enabled = False  # Disable auto-reload
        self.update_apps()  # Manually refresh the list of apps
        self.auto_reload_enabled = True  # Enable auto-reload after refresh

    def update_apps(self):
        current_apps = set(self.apps)
        new_apps = set()
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            if session.Process:
                if session.Process.name() not in current_apps:
                    new_apps.add(session.Process.name())
                    volume = session.SimpleAudioVolume
                    label = ctk.CTkLabel(self.frame, text=session.Process.name())
                    label.pack(pady=(10, 0))  # Provide some padding above the label
                    
                    volume_control = ctk.CTkSlider(self.frame, from_=0, to=100,
                                               command=lambda value, vol=volume: self.set_volume(value, vol))
                    volume_control.set(volume.GetMasterVolume() * 100)
                    volume_control.pack(pady=5)
                    self.volumes[session.Process.name()] = (volume_control, volume)

        stopped_apps = set()
        for app_name in current_apps:
            if app_name not in [session.Process.name() for session in sessions if session.Process]:
                stopped_apps.add(app_name)
                
                # Find and remove the label and slider for the inactive app
                for widget in self.frame.winfo_children():
                    if isinstance(widget, ctk.CTkLabel) and widget.cget("text") == app_name:
                        widget.pack_forget()  # Remove label
                    elif isinstance(widget, ctk.CTkSlider) and widget in self.volumes[app_name]:
                        widget.pack_forget()  # Remove slider

        if new_apps or stopped_apps:
            # Update self.apps with new apps and adjust window size if needed
            self.apps.extend(new_apps)
            for app_name in stopped_apps:
                self.apps.remove(app_name)
            
            window_height = min(500, max(250, 95 * len(self.apps) + 50))
            self.geometry(f'400x{window_height}')

            # Refresh the UI
            self.update_idletasks()

def start_volume_control_ui():
    spin_msg = SpinnerMessage(
        start_message  = "Application volume control (AVC) GUI running...", 
        end_message    = "AVC GUI terminated successfully.",
        spin_delay     = 0.1
    )
    
    app_ui = AmiyaVolumeControllerUI(spin_msg)
    try:
        app_ui.mainloop()
    except KeyboardInterrupt:
        spin_msg.verbose_end()
        app_ui.destroy()

if __name__ == "__main__":
    start_volume_control_ui()


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
