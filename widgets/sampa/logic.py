import os

import pandas as pd

from config.paths import PATHS


def sampa(args):
    if len(args) != 2:
        raise Exception("Wrong number of arguments")
    
    sampa_file = args[0]
    db_file = args[1]

    # get name of the file
    name = os.path.basename(sampa_file).split(".")[0]

    # make dataframe from .xlsx file and set default value on column 4
    frame = pd.read_excel(sampa_file)
    frame["Unnamed: 4"] = False
    frame.rename(columns={"Unnamed: 4": "Kod dodatkowy"}, inplace=True)

    # import database and define some constants
    db = pd.read_excel(db_file, converters={"Kod dodatkowy": str})
    db_KodTowaru = list(db["Kod towaru"])
    db_NazwaTowaru = list(db["Nazwa towaru"])
    db_KodTaryfy = list(db["Kod taryfy celnej"])
    db_Koncowka = list(db["Kod dodatkowy"])

    # iterate through every row and change values
    for index in frame.index:
        kodTowaru = frame.loc[index, "Kod towaru"]
        if kodTowaru in db_KodTowaru:
            i = db_KodTowaru.index(kodTowaru)
            frame.loc[index, "Kod towaru"] = db_KodTowaru[i]
            frame.loc[index, "Nazwa"] = db_NazwaTowaru[i]
            frame.loc[index, "Taryfa c."] = db_KodTaryfy[i]
            frame.loc[index, "Kod dodatkowy"] = db_Koncowka[i]

    # save dataframe as .xlsx file
    frame.to_excel(f"{PATHS.DESKTOP}/{name}-gotowy.xlsx", index=False)
