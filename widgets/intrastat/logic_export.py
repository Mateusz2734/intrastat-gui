from os import getlogin

import pandas as pd

from config.paths import PATHS


def exportf(intrastat_file, db1_file, db2_file):
    # make dataframe from .xlsx file
    frame = pd.read_excel(intrastat_file)

    # import first database and define some constants
    db1 = pd.read_excel(db1_file)
    db_KodTowarowy = list(db1["KodTowarowy"])
    db_OpisTowaru = list(db1["OpisTowaru"])

    # import second database and define constants
    db2 = pd.read_excel(db2_file)
    db2_StaryKodTowarowy = list(db2["StaryKodTowarowy"])
    db2_NowyKodTowarowy = list(db2["NowyKodTowarowy"])
    db2_NowyOpisTowaru = list(db2["NowyOpisTowaru"])

    # iterate through every row and change values
    for index in frame.index:
        kod = frame.loc[index, "KodTowarowy"]
        try:
            kodTowarowy = int(str(kod)[:8:])
        except ValueError:
            kodTowarowy = 0
        if kodTowarowy in db_KodTowarowy:
            i = db_KodTowarowy.index(kodTowarowy)
            frame.loc[index, "KodTowarowy"] = db_KodTowarowy[i]
            frame.loc[index, "OpisTowaru"] = db_OpisTowaru[i]
        if kod in db2_StaryKodTowarowy:
            i = db2_StaryKodTowarowy.index(kod)
            frame.loc[index, "KodTowarowy"] = db2_NowyKodTowarowy[i]
            frame.loc[index, "OpisTowaru"] = db2_NowyOpisTowaru[i]

    # save dataframe as .xlsx file
    frame.to_excel(f"{PATHS.DESKTOP}/gotowe.xlsx", index=False)
