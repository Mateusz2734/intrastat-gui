import os

import pandas as pd

from config.paths import PATHS


def invoice(args):
    if len(args) != 2:
        raise Exception("Wrong number of arguments")

    invoice_file = args[0]
    db_file = args[1]

    name = os.path.basename(invoice_file).split(".")[0]

    # open database and define constants
    db = pd.read_excel(db_file)
    db_KodTowarowy = list(db["KodTowarowy"])
    db_OpisTowaru = list(db["OpisTowaru"])

    # make dataframe from Excel file
    frame = pd.read_excel(invoice_file)

    # iterate through every row and change values
    for index in frame.index:
        taryfa = frame.loc[index, "Taryfa"]
        try:
            Taryfa = int(taryfa)
        except ValueError:
            Taryfa = 0
        if Taryfa in db_KodTowarowy:
            i = db_KodTowarowy.index(Taryfa)
            frame.loc[index, "Taryfa"] = db_KodTowarowy[i]
            frame.loc[index, "Nazwa"] = db_OpisTowaru[i]
    frame.to_excel(f"{PATHS.DESKTOP}/{name}-gotowy.xlsx", index=False)
