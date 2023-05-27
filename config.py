import os
from dotenv import load_dotenv

load_dotenv()
# print("hello")

class Config:
    __conf = {
        "OSRM_URL": os.getenv("OSM_HELPER_OSRM_URL", "http://router.project-osrm.org/table/v1/driving/"),
    }
    __setters = ["OSRM_URL"]

    @staticmethod
    def config(name):
        return Config.__conf[name]

    @staticmethod
    def set(name, value):
        if not isinstance(name, str):
            raise TypeError(f"{name} must be str not but {type(name)} is given.")
        
        if name in Config.__setters:
            Config.__conf[name] = value
        else:
            raise NameError(f'"{name}" not accepted in set() method')