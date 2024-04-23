import os

from amiya.apps_manager.app import App
from amiya.utils.json_handler import JSONConfigHandler

class SchedulerConfigHandler(JSONConfigHandler):
    def __init__(self):
        super().__init__(
            config_abs_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json"),
            config_type=list
        )
        
        if not self.config_exists():
            self.save_config([])

    def save_task(self, task_name, app_tag, sequence_name, execution_time):
        tasks = self.load_config()
        data = {
            "task_name": task_name,
            "application_tag": app_tag,
            "sequence_name": sequence_name,
            "execution_time": execution_time
        }
        tasks.append(data)
        self.save_config(tasks)
        
    def load_tasks(self):
        return self.load_config()
    
    def validate_config(self):
        pass