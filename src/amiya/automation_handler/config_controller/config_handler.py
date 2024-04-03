import os
import json

try:
    CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
    assert(os.path.isfile(CONFIG_FILE))

except AssertionError:
    print(f"Config file not found, creating config file from stub.")
    
    def create_config_with_stub():
        os.system(f'type nul > {CONFIG_FILE}' if os.name == 'nt' else f'touch {CONFIG_FILE}')
        with open(CONFIG_FILE, "w") as wf:
            STUB = [
                {
                    "coordinate": {
                        "x": 0,
                        "y": 0    
                    },
                    "delay": 0.0,
                    "click": False
                }
            ]
            wf.write(json.dumps(STUB, indent=4))

    create_config_with_stub()


class ConfigHandler:
    def __init__(self):
        self.config: list = self.read_config()
        self.__validate_config(self.config)


    def read_config(self):
        try:
            with open(CONFIG_FILE, "r") as rf:
                config = json.load(rf)
                return config
        except FileNotFoundError:
            print(f"Config file not found (stab did not auto generate)."); exit(1)
        except Exception as ex:
            raise ex


    def write_to_config(self, json_actions: list[dict]):
        if len(json_actions) == 0:
            print("Actions list is empty - no actions to write to config.")
            return True
        
        if os.path.isfile(CONFIG_FILE):
            uinput = input("Config already exist. Are you sure that you would like to overwrite it? [y/n] ")
            if uinput.lower().strip() != "y":
                return False
        
        # verify that the input json action config is correct
        self.__validate_config(json_actions)
        
        try:
            with open(CONFIG_FILE, "w") as wf:
                json.dump(json_actions, wf, indent=4)
        except FileNotFoundError:
            print(f"config not found (stab did not auto generate)."); exit(1)
        except Exception as ex:
            raise ex
        
        print(f"Actions ({len(json_actions)}) successfully written to config!")
        return True


    def __validate_config(self, config):
        for record in config:
            if not isinstance(record["coordinate"]["x"], int) or not isinstance(record["coordinate"]["y"], int):
                print(f'[coordinate] Expected (int, int), but got ({type(record["coordinate"]["x"])}, {type(record["coordinate"]["x"])})')
                
            if not isinstance(record["delay"], float):
                print(f'[delay] Expected float, but got {type(record["delay"])}')
                
            if not isinstance(record["click"], bool):
                print(f'[click] Expected bool, but got {type(record["click"])}')
                
                