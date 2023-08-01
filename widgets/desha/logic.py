import os

import pandas as pd


def desha(desha_file, db_file):
    # get name of the file
    name = os.path.basename(desha_file).split(".")[0]

    # get current user
    user = os.getlogin()

    # make dataframe from .xlsx file and set default value on column 4
    frame = pd.read_excel(desha_file)
    frame["Unnamed: 4"] = False
    frame.rename(columns={"Unnamed: 4": "Kod dodatkowy"}, inplace=True)

    # import database and define some constants
    db = pd.read_excel(db_file, converters={"TARIC": str})
    db_Symbol = list(db["SYMBOL"])
    db_Nazwa = list(db["NAZWA"])
    db_Pcn = list(db["PCN"])
    db_Taric = list(db["TARIC"])

    # iterate through every row and change values
    for index in frame.index:
        kodTowaru = frame.loc[index, "Kod towaru"]
        if kodTowaru in db_Symbol:
            i = db_Symbol.index(kodTowaru)
            frame.loc[index, "Kod towaru"] = db_Symbol[i]
            frame.loc[index, "Nazwa"] = db_Nazwa[i]
            frame.loc[index, "Taryfa c."] = db_Pcn[i]
            frame.loc[index, "Kod dodatkowy"] = db_Taric[i]

    # save dataframe as .xlsx file
    frame.to_excel(f"C:/Users/{user}/Desktop/{name}-gotowy.xlsx", index=False)
