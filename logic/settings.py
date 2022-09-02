import json
from os.path import exists as file_exists

def create_settings():
    data = { "invoice": {"db": None},"intrastat": {"db1": None,"db2": None}}
    if not file_exists("C:/Skrypty/Pomocnik/settings.json"):
        with open('C:/Skrypty/Pomocnik/settings.json', 'w') as file:
            file.write(json.dumps(data, indent=4, sort_keys=True))

def read_settings():
    with open('C:/Skrypty/Pomocnik/settings.json', 'r') as file:
        json_settings = json.load(file)
    return json_settings

