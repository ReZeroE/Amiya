import subprocess

class SysUUIDController:
    @staticmethod
    def get_system_uuid():
        try:
            result = subprocess.check_output('wmic csproduct get uuid', shell=True).decode()
            uuid = result.strip().split('\n')[1].strip()
            return uuid
        except Exception as e:
            return str(e)
    
    system_uuid = get_system_uuid()
