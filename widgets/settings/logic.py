import logging as log
from os.path import exists as file_exists
import yaml

from config.paths import PATHS

DEFAULT_DATA = {
    "invoice": {"db": None},
    "intrastat": {"db1": None, "db2": None},
    "sampa": {"db": None},
    "desha": {"db": None},
    "sem": {"db": None}
}

def create_settings():
    if not file_exists(PATHS.SETTINGS):
        try:
            with open(PATHS.SETTINGS, "w") as file:
                file.write(yaml.safe_dump(DEFAULT_DATA))
        except Exception as e:
            log.error(f"{__name__} :: {str(e)}")


def read_settings():
    try:
        with open(PATHS.SETTINGS, "r") as file:
            yaml_settings = yaml.safe_load(file)
        return yaml_settings
    except Exception as e:
        log.error(f"{__name__} :: {str(e)}")