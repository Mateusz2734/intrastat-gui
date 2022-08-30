import pandas as pd
from os import getlogin

def export(intrastat_file, db_file):
    # get current user 
    user = getlogin()
    
    # make dataframe from .xlsx file
    frame = pd.read_excel(intrastat_file)

    # import first database and define some constants
    db1 = pd.read_csv(db_file, delimiter=';').drop('Unnamed: 2', axis=1)
    db_KodTowarowy = list(db1["KodTowarowy"])
    db_OpisTowaru = list(db1["OpisTowaru"])

    # iterate through every row and change values
    for index in frame.index:
        kod = frame.loc[index, 'KodTowarowy']
        try:
            kodTowarowy = int(str(kod)[:8:])
        except ValueError:
            kodTowarowy = 0
        if kodTowarowy in db_KodTowarowy:
            i = db_KodTowarowy.index(kodTowarowy)
            frame.loc[index, 'KodTowarowy'] = db_KodTowarowy[i]
            frame.loc[index, 'OpisTowaru'] = db_OpisTowaru[i]
    
    # save dataframe as .xlsx file
    frame.to_excel(f"C:/Users/{user}/Desktop/{intrastat_file}", index=False)