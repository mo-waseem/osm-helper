import os
import yaml
from dotenv import load_dotenv

load_dotenv()


class Config:
    # You need to add this file to .gitignore of your project
    with open(
        os.getenv("CONFG_YAML_FILE_NAME", "osm_helper_config.yaml"), "r"
    ) as stream:
        try:
            OSM_CONFIG = yaml.safe_load(stream)
        except yaml.YAMLError as exc: # noqa
            OSM_CONFIG = {}
            pass

    __conf = OSM_CONFIG
    __conf.update(
        {
            "OSRM_URL": __conf.get(
                "PRIMARY_OSRM_URL",
                os.getenv(
                    "PRIMARY_OSRM_URL",
                    "http://router.project-osrm.org/",
                ),
            )
        }
    )
    __setters = ["OSRM_URL"]

    @staticmethod
    def config(name, default_value=None):
        return Config.__conf.get(name, default_value)

    @classmethod
    def set(cls, name, value):
        if not isinstance(name, str):
            raise TypeError(f"{name} must be str not but {type(name)} is given.")

        if name in Config.__setters:
            cls.__conf[name] = value
        else:
            raise NameError(f'"{name}" not accepted in set() method')
