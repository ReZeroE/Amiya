import subprocess
from amiya.utils.helper import aprint

class SysUUIDController:
    @staticmethod
    def get_system_uuid():
        try:
            result = subprocess.check_output('wmic csproduct get uuid', shell=True).decode()
            uuid = result.strip().split('\n')[1].strip()
            return uuid
        except Exception as e:
            return str(e)

    @staticmethod
    def print_uuid():
        aprint(f"System UUID: {SysUUIDController.get_system_uuid()}")


SYSTEM_UUID = SysUUIDController.get_system_uuid()