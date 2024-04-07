import os

from amiya.apps_manager.app import App
from amiya.utils.json_handler import JSONConfigHandler

class SchedulerConfigHandler(JSONConfigHandler):
    def __init__(self, apps: list[App]):
        super().__init__(
            config_abs_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json"),
            config_type=dict,
            config_stub=[
                {
                    "ph_sequence_name": {
                        "scheduled_time": "",
                        "last_executed": ""
                    }
                }
            ]
        )