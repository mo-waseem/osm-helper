import os
import warnings
import yaml

from dotenv import load_dotenv
from typing import Any

load_dotenv()


class Config:
    # You need to add this file to .gitignore of your project
    try:
        with open(
            os.getenv("CONFG_YAML_FILE_NAME", "osm_helper_config.yaml"), "r"
        ) as stream:
            try:
                OSM_CONFIG = yaml.safe_load(stream) or {}
            except yaml.YAMLError as exc: # noqa
                OSM_CONFIG = {}
    except FileNotFoundError:
        OSM_CONFIG = {}
    if not OSM_CONFIG:
        warnings.warn("osm-helper: 'osm_helper_config.yaml' file is not setted.")
        

    __conf = OSM_CONFIG 
    __default_osrm_url = "http://router.project-osrm.org/"
    __yaml_osrm_url = __conf.get("PRIMARY_OSRM_URL", None) if __conf else None
    __env_osrm_url = os.getenv("PRIMARY_OSRM_URL", None)
    if not __env_osrm_url and not __yaml_osrm_url:
        warnings.warn("osm-helper: 'PRIMARY_OSRM_URL' is not setted.")
    __osrm_url = __env_osrm_url or __yaml_osrm_url or __default_osrm_url
    
    __conf.update(
        {
            "OSRM_URL": __osrm_url
        }
    )
    __setters = ["OSRM_URL"]

    @staticmethod
    def config(name: str, default_value: Any=None) -> Any:
        return Config.__conf.get(name, default_value)

    @classmethod
    def set(cls, name: str, value: Any) -> None:
        if not isinstance(name, str):
            raise TypeError(f"{name} must be str not but {type(name)} is given.")

        if name in Config.__setters:
            cls.__conf[name] = value
        else:
            raise NameError(f'"{name}" not accepted in set() method')
