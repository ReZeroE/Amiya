from amiya.utils.json_handler import JSONConfigHandler
from amiya.exceptions.exceptions import *

class SequenceConfigHandler(JSONConfigHandler):
    def __init__(self, config_abs_path, config_type=list):
        super().__init__(
            config_abs_path,
            config_type
        )
    
    def validate_config(self):
        pass
    
class PlateConfigHandler(JSONConfigHandler):
    def __init__(self, config_abs_path, config_type=list):
        super().__init__(
            config_abs_path,
            config_type
        )
    
    def validate_config(self):
        pass