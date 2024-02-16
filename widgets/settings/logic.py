import logging as log
from os.path import exists as file_exists
from shutil import copy2
import json

from config.paths import PATHS

DEFAULT_DATA = {
    "invoice": {"db": None},
    "intrastat": {"db1": None, "db2": None},
    "sampa": {"db": None},
    "desha": {"db": None},
    "sem": {"db": None},
}


def create_settings():
    if not file_exists(PATHS.SETTINGS):
        try:
            with open(PATHS.SETTINGS, "w") as file:
                file.write(json.dumps(DEFAULT_DATA, indent=4, sort_keys=True))
        except Exception as e:
            log.error(f"{__name__} :: {str(e)}")


def read_settings():
    try:
        with open(PATHS.SETTINGS, "r") as file:
            json_settings = json.load(file)
        return json_settings
    except Exception as e:
        log.error(f"{__name__} :: {str(e)}")


def save_settings(settings):
    try:
        json_data = json.dumps(settings, indent=4, sort_keys=True)
        with open(PATHS.SETTINGS, "w") as file:
            file.write(json_data)
        return True

    except Exception as e:
        log.error(f"{__name__} :: {str(e)}")
        return False


def is_json(candidate):
    try:
        json.loads(candidate)
    except ValueError:
        return False
    return True


def move_file(path):
    try:
        return copy2(path, PATHS.MAIN)
    except Exception as e:
        log.error(f"{__name__} :: {str(e)}")
        return ""
