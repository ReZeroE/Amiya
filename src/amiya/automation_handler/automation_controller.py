import time
import os
from amiya.automation_handler.automation_config_handler import SequenceConfigHandler
from amiya.automation_handler.units.action import Action, MouseAction, KeyboardAction
from amiya.automation_handler.units.sequence import AutomationSequence
from amiya.automation_handler.units.plate import AutomationPlate
from amiya.automation_handler.automation_recorder import AutomationRecorder
from amiya.exceptions.exceptions import *
from amiya.utils.helper import *
from amiya.apps_manager.safety_monitor import SafetyMonitor


APP_AUTOMATION_SEQUENCE_DIRNAME = "sequence"
APP_AUTOMATION_PLATE_DIRNAME    = "plate"

class AutomationController:
    def __init__(self, automation_dir):
        self.automation_dir     = automation_dir
        self.sequence_dirpath   = os.path.join(automation_dir, APP_AUTOMATION_SEQUENCE_DIRNAME)
        self.plate_dirpath      = os.path.join(automation_dir, APP_AUTOMATION_PLATE_DIRNAME)
        
        self.__create_automation_dir_structure()
        
        # TODO: This doesn't work in the CLI environment:
        # When two sequences with the same name gets recorded/created, he sequence with the same name will get overwritten 
        # in the config file, but the list structure will not remove the previous automation sequence
        # 
        # This needss to be changed into a dictionary with sequence name as the key
        self.__sequence_list: list[AutomationSequence] = self.__load_all_sequences()
        self.__plate_list: list[AutomationPlate] = None
    
    
    def __create_automation_dir_structure(self):
        if not os.path.exists(self.automation_dir):         # Create the app automation top directory (amiya/apps/<app_name>/automation)
            os.mkdir(self.automation_dir)
        if not os.path.exists(self.sequence_dirpath):       # Create the app automation sequence directory (amiya/apps/<app_name>/automation/sequence)
            os.mkdir(self.sequence_dirpath)
        if not os.path.exists(self.plate_dirpath):          # Create the app automation plate directory (amiya/apps/<app_name>/automation/plate)
            os.mkdir(self.plate_dirpath)
    
    # ========================================================
    # ===========| AUTOMATION SEQUENCE FUNCTIONS | ===========
    # ========================================================
    def get_all_sequences(self):
        return self.__sequence_list
    
    def get_sequence(self, sequence_name):
        target_sequence_name = self.__reformat_sequence_name(sequence_name)
        for sequence in self.__sequence_list:
            if sequence.sequence_name == target_sequence_name:
                return sequence
        return None
     
    def sequence_exists(self, sequence_name):
        return self.get_sequence(sequence_name) != None
        
    def record_sequence(self, new_sequence_name, safety_monitor: SafetyMonitor) -> AutomationSequence:
        NEW_SEQUENCE_NAME = self.__reformat_sequence_name(new_sequence_name)
        recording_sequence = AutomationSequence(NEW_SEQUENCE_NAME)                        # Create new empty actions sequence (later populated during recording)
        recording_sequence.set_date_created_to_current()                                  # Set current time to creation time

        action_recorder   = AutomationRecorder(recording_sequence, safety_monitor)        # Create the AutomationRecorder object by passing it the empty sequence object to populate and a safety monitor (to fetch app window size)
        action_recorder.record(start_on_callback=True)                                    # Record mouse actions until "end-recording" is pressed
        
        aprint("Saving to configurations...")
        config_handler    = SequenceConfigHandler(self.__get_sequence_filepath(new_sequence_name))
        json_sequence     = recording_sequence.to_json()                                  # Convert the AutomationSequence object into a list of JSON objects
        success           = config_handler.save_config(json_sequence)                     # Write JSON actions to config
        assert(success == True)
        
        self.__update_sequence_list(recording_sequence)
        return recording_sequence                                                         # Returns the recorded action sequence if successful
    
    def __update_sequence_list(self, sequence: AutomationSequence):
        self.__sequence_list.append(sequence)
        self.__sequence_list.sort(key=lambda seq: seq.date_created)
        
    def __load_all_sequences(self) -> list[AutomationSequence]:
        sequence_list: list[AutomationSequence] = []
        sequence_name_list = os.listdir(self.sequence_dirpath)        # List all file/dir names in the automation folder
        
        for seq_filename in sequence_name_list:
            AUTOMATION_FILE = os.path.join(self.sequence_dirpath, seq_filename)
            config_handler = SequenceConfigHandler(AUTOMATION_FILE)
            if config_handler.config_exists():
            
                raw_json_config = config_handler.load_config()              # Loads the sequence config file
                sequence = self.parse_sequence_config(raw_json_config)    # Parses the json config into a sequence object
                sequence_list.append(sequence)
                
        sequence_list.sort(key=lambda seq: seq.date_created)
        return sequence_list


    # ===========| HELPER FUNCTIONS | ===========
    
    def parse_sequence_config(self, raw_json_config: list):
        metadata        = raw_json_config["metadata"]
        sequence_name   = metadata["sequence_name"]
        
        sequence = AutomationSequence(sequence_name)
        
        sequence.date_created           = DatetimeHandler.str_to_datetime(metadata["date_created"])
        sequence.primary_monitor_info   = metadata["monitor_info"]
        sequence.other_data             = metadata["other_data"]
        
        actions_sequence = raw_json_config["actions_sequence"]
        for raw_action in actions_sequence:
            if "coordinate" in raw_action:
                mouse_action = MouseAction(
                    (
                        raw_action["coordinate"]["x"],
                        raw_action["coordinate"]["y"]
                    ),
                    raw_action["delay"],
                    raw_action["click"],
                    raw_action["window_info"]
                )
                sequence.actions.append(mouse_action)
            elif "key" in raw_action:
                keyboard_action = KeyboardAction(
                    raw_action["key"],
                    raw_action["delay"]
                )
                sequence.actions.append(keyboard_action)
            else:
                raise AmiyaBaseException(f"Action ({raw_action}) can't be interpreted!")
        return sequence
    
    def __get_sequence_name(self, filename: str):
        return filename.strip().lower().replace(".json", "")
 
    def __reformat_sequence_name(self, sequence_name: str):
        return sequence_name.strip().replace(" ", "-").lower()
    
    def __get_sequence_filepath(self, sequence_name: str):
        return os.path.join(self.sequence_dirpath, f"{self.__reformat_sequence_name(sequence_name)}.json")
    
    
    
    # ========================================================
    # =============| AUTOMATION PLATE FUNCTIONS | ============
    # ========================================================
    
    
    def create_plate(self, plate_name: str, sequence_names: list[str]):
        sequence_list: list[AutomationSequence] = [] # MUST BE IN ORDER!!!
        for seq_name in sequence_names:
            seq = self.get_sequence(seq_name)
            sequence_list.append(seq)
        
        plate = AutomationPlate(plate_name, sequence_list)
        plate.set_date_created_to_current()
        
        config_handler = SequenceConfigHandler(self.__get_plate_filepath(plate_name))
        plate_json = plate.to_json()
        config_handler.save_config(plate_json)
        
        self.__plate_list.append(plate)
 
    
    def parse_plate_config(self, raw_json):
        metadata = raw_json["metadata"]
        
        plate_name = metadata["plate_name"]
        date_created = metadata["date_created"]
        other_data = metadata["other_data"]
        
        sequence_names = raw_json["sequences"]
        sequence_list = []
        
        for sequence_name in sequence_names:
            seq = self.get_sequence(sequence_name)
            sequence_list.append(seq)
            
            
        automation_plate = AutomationPlate(
            plate_name,
            sequence_list
        )
        
        automation_plate.date_created = date_created
        automation_plate.other_data   = other_data
        
        
    def __reformat_plate_name(self, sequence_name: str):
        return sequence_name.strip().replace(" ", "-").lower()
    
    def __get_plate_filepath(self, sequence_name: str):
        return os.path.join(self.auto_plate_config_dir, f"{self.__reformat_sequence_name(sequence_name)}.json")