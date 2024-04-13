import time
import os
from amiya.automation_handler.config_controller.config_handler import ActionsConfigHandler
from amiya.automation_handler.actions_controller.units.action import Action, MouseAction, KeyboardAction
from amiya.automation_handler.actions_controller.units.sequence import ActionsSequence
from amiya.automation_handler.actions_controller.actions_recorder import ActionsRecorder
from amiya.exceptions.exceptions import *
from amiya.utils.helper import *

class ActionsController:
    def __init__(self, config_dir):
        self.actions_config_dir = config_dir
        
        
    def load_sequence(self, sequence_name) -> ActionsSequence:
        """
        Function responsible for loading actions sequence from the JSON config files.
        
        1. Initializes a ConfigHandler to read the corresponding JSON config file.
        2. Initalizes an empty ActionsSequence object and calls the parse_config() function to fetch and parse the JSON config file.
        3. Returns the sequence object.
        """
        SEQUENCE_NAME = self.__reformat_sequence_name(sequence_name)
        SEQUENCE_FILENAME = self.__get_sequence_filename(sequence_name)
        
        config_handler = ActionsConfigHandler(config_abs_path=os.path.join(self.actions_config_dir, SEQUENCE_FILENAME))
        try:
            raw_sequence_json_config = config_handler.load_config()         # Loads the sequence config file
            
            sequence = ActionsSequence()                                    # Create new empty sequence object
            sequence.parse_config(raw_sequence_json_config)                 # Parses the json config into a sequence object
            
        except Amiya_ConfigDoesNotExistException:
            raise AmiyaBaseException(f"No automation sequence with name '{SEQUENCE_NAME}' can be found.")
        return sequence
        
    def load_all_sequences(self) -> list[ActionsSequence]:
        sequences: list[ActionsSequence] = []
        sequence_name_list = os.listdir(self.actions_config_dir)                            # List all file/dir names in the automation folder
        for seq_filename in sequence_name_list:
            if os.path.isfile(os.path.join(self.actions_config_dir, seq_filename)):         # If the file is indeed a file (aka not a folder)
                sequence = self.load_sequence(self.__get_sequence_name(seq_filename))       # Load the sequence file
                sequences.append(sequence)
        return sequences
    
    def start_recording(self, new_sequence_name, start_recording_on_callback=True) -> ActionsSequence:
        """
        Function responsible for recording new action sequences.
        
        1. Initializes a ActionsRecorder object that is responsible for recording and tracking all user actions.
        2. Convert the recording (ActionsRecorder's ActionsSequence object) into JSON format
        3. Saves the JSON in the corresponding automation folder for the App (using the ConfigHandler). 
        
        Returns the recorded action sequence
        
        :param overwrite: Overwrite a sequence even if the sequence already exist (identified by sequence name).
        :param start_record_on_callback: Start the recording as soon as the record() function below is called (as opposed to waiting for user input to start).
        """
        NEW_SEQUENCE_NAME = self.__reformat_sequence_name(new_sequence_name)
        NEW_SEQUENCE_FILENAME = self.__get_sequence_filename(new_sequence_name)
        
        seq_config_file = os.path.join(self.actions_config_dir, NEW_SEQUENCE_FILENAME)
        config_handler = ActionsConfigHandler(seq_config_file)

        action_recorder   = ActionsRecorder()
        recorded_sequence = action_recorder.record(start_recording_on_callback)              # Record mouse actions until "up-arrow" is pressed
        recorded_sequence.sequence_name = NEW_SEQUENCE_NAME                                  # Set the new sequence name
        
        aprint("Saving to configurations...")
        json_sequence     = recorded_sequence.to_json()                                      # Convert the ActionsSequence object into a list of JSON objects
        success           = config_handler.save_config(json_sequence)                        # Write JSON actions to config
        assert(success == True)
        
        return recorded_sequence                                                             # Returns the recorded action sequence if successful
    

    # ===========================================
    # ===========| HELPER FUNCTIONS | ===========
    # ===========================================
    def __get_sequence_name(self, filename: str):
        return filename.strip().lower().replace(".json", "")
            
    def __reformat_sequence_name(self, sequence_name: str):
        return sequence_name.strip().replace(" ", "-").lower()
    
    def __get_sequence_filename(self, sequence_name: str):
        return f"{self.__reformat_sequence_name(sequence_name)}.json"