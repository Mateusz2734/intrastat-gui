import logging as log
import json
from os.path import exists as file_exists


def create_settings():
    default_data = {"invoice": {"db": None}, "intrastat": {"db1": None, "db2": None}, "sampa": {"db": None}}
    if not file_exists("C:/Skrypty/Pomocnik/settings.json"):
        try:
            with open('C:/Skrypty/Pomocnik/settings.json', 'w') as file:
                file.write(json.dumps(default_data, indent=4, sort_keys=True))
        except Exception as e:
            log.error(f"{__name__} :: {str(e)}")

def read_settings():
    try:
        with open('C:/Skrypty/Pomocnik/settings.json', 'r') as file:
            json_settings = json.load(file)
        return json_settings
    except Exception as e:
        log.error(f"{__name__} :: {str(e)}")