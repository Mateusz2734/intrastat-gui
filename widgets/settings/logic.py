import logging as log
import json
from os.path import exists as file_exists

DEFAULT_DATA = {
    "invoice": {"db": None},
    "intrastat": {"db1": None, "db2": None},
    "sampa": {"db": None},
    "desha": {"db": None},
}

SETTINGS_FILE = "C:/Skrypty/Pomocnik/settings.json"


def create_settings():
    if not file_exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "w") as file:
                file.write(json.dumps(DEFAULT_DATA, indent=4, sort_keys=True))
        except Exception as e:
            log.error(f"{__name__} :: {str(e)}")


def read_settings():
    try:
        with open(SETTINGS_FILE, "r") as file:
            json_settings = json.load(file)
        return json_settings
    except Exception as e:
        log.error(f"{__name__} :: {str(e)}")
