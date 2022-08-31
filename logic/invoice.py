import pandas as pd
from os import getlogin

def invoice(intrastat_file, db_file):
    # get current user
    user = getlogin()

    # open database and define constants
    db = pd.read_csv(db_file, delimiter=';')
    db_KodTowarowy = list(db["KodTowarowy"])
    db_OpisTowaru = list(db["OpisTowaru"])
    
    # make dataframe from Excel file
    frame = pd.read_excel(intrastat_file)

    # iterate through every row and change values
    for index in frame.index:
        taryfa = frame.loc[index, 'Taryfa']
        try:
            Taryfa = int(taryfa)
        except ValueError:
            Taryfa = 0
        if Taryfa in db_KodTowarowy:
            i = db_KodTowarowy.index(Taryfa)
            frame.loc[index, 'Taryfa'] = db_KodTowarowy[i]
            frame.loc[index, 'Nazwa'] = db_OpisTowaru[i]
    frame.to_excel(f"C:/Users/{user}/Desktop/gotowe.xlsx", index=False)