import logging as log
from os.path import exists as file_exists
import yaml

SETTINGS_FILE = "C:/Skrypty/Pomocnik/settings.yaml"

DEFAULT_DATA = {
    "invoice": {"db": None},
    "intrastat": {"db1": None, "db2": None},
    "sampa": {"db": None},
    "desha": {"db": None},
}

def create_settings():
    if not file_exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "w") as file:
                file.write(yaml.safe_dump(DEFAULT_DATA))
        except Exception as e:
            log.error(f"{__name__} :: {str(e)}")


def read_settings():
    try:
        with open(SETTINGS_FILE, "r") as file:
            yaml_settings = yaml.safe_load(file)
        return yaml_settings
    except Exception as e:
        log.error(f"{__name__} :: {str(e)}")