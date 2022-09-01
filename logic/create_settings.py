import json
from os.path import exists as file_exists

def create_settings():
    data = {
        "intrastat": {
            "invoice": {
                "file": None,
                "db": None
            },
            "intrastat": {
                "file": None,
                "db1": None,
                "db2": None
            }
        }
    }
    if not file_exists("C:/Skrypty/Pomocnik/settings.json"):
        with open('C:/Skrypty/Pomocnik/settings.json', 'w') as file:
            file.write(json.dumps(data, indent=4, sort_keys=True))
create_settings()