import os
import sys
import json
import shutil
import time
import signal
from termcolor import colored
from amiya.apps_manager.app import App, APP_CONFIG_FILENAME
from amiya.apps_manager.apps_viewer import AppsViewer
from amiya.utils.constants import RAW_AUTO_DIRECTORY, AMIYA_PID, DEVELOPMENT
from amiya.exceptions.exceptions import *
from amiya.utils.helper import *
from amiya.automation_handler.automation_controller import AutomationController
from amiya.automation_handler.units.sequence import AutomationSequence
from amiya.automation_handler.automation_viewer import AutomationViewer
from amiya.apps_manager.safety_monitor import SafetyMonitor
from amiya.apps_manager.sync_controller.sync_controller import AppSyncController
from amiya.apps_manager.sync_controller.sys_uuid_controller import SYSTEM_UUID
from amiya.module_utilities.power_controller import PowerUtils


class RawAutoManager:
    def __init__(self):
        self.__init_dir_structure()
        self.raw_sequences_dict: dict[int, AutomationSequence] = self.__load_raw_sequences()
        
    
    def __load_raw_sequences(self):
        raw_auto_dir = RAW_AUTO_DIRECTORY
        
        raw_auto_dict: dict[int, App] = dict()
        raw_auto_name_list = os.listdir(raw_auto_dir)
        
        current_id = 1
        for raw_auto_name in raw_auto_name_list:
            seq_config = os.path.join(raw_auto_dir, raw_auto_name)
            if os.path.isfile(seq_config):
                auto_sequence = AutomationController.parse_sequence_config(seq_config)
                raw_auto_dict[current_id] = auto_sequence
                current_id += 1

        return raw_auto_dict
    
    
    
    def __init_dir_structure(self):
        if not os.path.exists(RAW_AUTO_DIRECTORY):
            os.mkdir(RAW_AUTO_DIRECTORY)
        
    
    
    def __get_sequence_by_id(self, input_id: str) -> AutomationSequence:
        try:
            seq_id = int(input_id)
            sequence = self.raw_sequences_dict[seq_id]
        except TypeError:
            aprint(f"Expecting an integer (such as 0 or 1) but got `{input_id}`", log_type=LogType.ERROR); raise AmiyaExit()
        except KeyError:
            aprint(f"ID {seq_id} does not correspond to any automation sequence.", log_type=LogType.ERROR); raise AmiyaExit()
            
        return sequence