from datetime import datetime
from amiya.apps_manager.safety_monitor import SafetyMonitor

from amiya.utils.helper import *
from amiya.automation_handler.units.sequence import AutomationSequence

class AutomationPlate:
    def __init__(self, plate_name: str, sequence_list: list[AutomationSequence]):
        
        self.plate_name: str                 = plate_name
        self.date_created: datetime          = None                          # Default to None (and set at to_json() and parse_json())
        self.other_data                      = None
        
        self.sequence_dict: dict[int, AutomationSequence]   = self.__set_ids(sequence_list)
    
    
    def execute(self, safety_monitor: SafetyMonitor):
        for sequence in [self.sequence_dict[idx] for idx in sorted(self.sequence_dict)]:
            sequence.execute(safety_monitor)
    
    
    def to_json(self):
        return {
            "metadata": {
                "plate_name": self.plate_name,
                "date_created": DatetimeHandler.datetime_to_str(self.date_created),
                "other_data": self.other_data
            },
            "sequences": [
                seq.sequence_name for seq in self.sequence_dict.values()
            ]
        }
        
        
    
        
    def set_date_created_to_current(self):
        self.date_created = DatetimeHandler.get_datetime()
        
        
    def __set_ids(self, sequence_list: list[AutomationSequence]):
        return {idx+1: sequence for idx, sequence in enumerate(sequence_list)}
    
    