import os
import sys
import string
import subprocess
from concurrent import futures
from multiprocessing import Manager

from amiya.apps_manager.app import App
from amiya.exceptions.exceptions import AmiyaBaseException

class AppSyncController:
    def get_local_drives(self):
        available_drives = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]
        return available_drives

    def find_app_in_path(self, path, name, stop_flag):
        for root, _, files in os.walk(path):
            if stop_flag.value: # Check the shared flag value.
                return None
            if name in files:
                return os.path.join(root, name)
        return None

    def find_app(self, name, paths=[]):
        for p in paths:
            if not os.path.exists(p):
                raise AmiyaBaseException(f"Path does not exist. [{p}]")

        if len(paths) == 0:
            paths = self.get_local_drives()

        paths = [f"{path}\\" if path.endswith(":") and len(path) == 2 else path for path in paths]

        worker_threads = 1
        if os.cpu_count() > 1:
            worker_threads = os.cpu_count() - 1

        with futures.ProcessPoolExecutor(max_workers=worker_threads) as executor, Manager() as manager:
            stop_flag = manager.Value('b', False)   # Create a boolean shared flag.
            future_to_path = {executor.submit(self.find_app_in_path, path, name, stop_flag): path for path in paths}
            for future in futures.as_completed(future_to_path):
                result = future.result()
                if result is not None:
                    stop_flag.value = True # Set the flag to true when a result is found.
                    return result
        return None
    
    
    def sync(self, app: App):
        # If app's path verification failed
        if app.verified == False:
            app_basename = os.path.basename(app.exe_path)
            new_path = self.find_app(app_basename)
            
            # If app exist on the new machine
            if new_path != None:
                app.set_new_path(new_path)  # Set new path
                app.set_new_uuid()          # Set new system UUID
                app.save_app_config()       # Save new config
                return True                 # ---> New path set successfully
            else:
                app.set_new_uuid()          # Set new system UUID
                app.save_app_config()       # Save new config
                return False                # ---> App doesn't exist on new machine
        else:
            app.set_new_uuid()              # Set new system UUID
            app.save_app_config()           # Save new config
            return True                     # ---> App original path works on new machine

