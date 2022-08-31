import xml.etree.ElementTree as Et
from logic import exportf
import pandas as pd
import glob
import os

def importf(intrastat_dir, db1_file, db2_file, destination_folder, destination_name): #
    
    # rename all xml files
    files = glob.glob(f'{intrastat_dir}/*.xml')
    for file in files:
        os.rename(file, f'{int(file.split(".")[0]):03d}.xml')

    # define main parser
    def parser_intrastat(name: str):
        tree = Et.parse(name)
        root = tree.getroot()
        number = int(name.split(".")[0])
        elems = []
        for towar in root.iter('{http://www.mf.gov.pl/xsd/Intrastat/IST.xsd}Towar'):
            elems.append(towar.attrib)
        frame_towar = pd.DataFrame(elems)
        frame_towar.insert(0, "NrDokumentu", number, True)
        return frame_towar

    # define info parser
    def parser_info(name):
        tree = Et.parse(name)
        root = tree.getroot()
        number = int(name.split(".")[0])
        elems = []
        for deklaracja in root.iter('{http://www.mf.gov.pl/xsd/Intrastat/IST.xsd}Deklaracja'):
            elems.append(deklaracja.attrib)
        frame_info = pd.DataFrame(elems)
        frame_info.insert(0, "NrDokumentu", number, True)
        return frame_info
    
    # parse every xml file
    dataframe_intrastat = pd.DataFrame()
    dataframe_info = pd.DataFrame()
    files = glob.glob('*.xml')
    for file in files:
        dataframe_intrastat = pd.concat([dataframe_intrastat, parser_intrastat(file)])
        dataframe_info = pd.concat([dataframe_info, parser_info(file)])

    # cast types in main file
    dataframe_intrastat["PozId"] = dataframe_intrastat["PozId"].astype("int64")
    dataframe_intrastat["RodzajTransakcji"] = dataframe_intrastat["RodzajTransakcji"].astype("int64")
    dataframe_intrastat["KodTowarowy"] = dataframe_intrastat["KodTowarowy"].astype("int64")
    dataframe_intrastat["MasaNetto"] = dataframe_intrastat["MasaNetto"].astype("int64")
    dataframe_intrastat["IloscUzupelniajacaJm"] = dataframe_intrastat["IloscUzupelniajacaJm"].astype("int64")
    dataframe_intrastat["WartoscFaktury"] = dataframe_intrastat["WartoscFaktury"].astype("int64")
    dataframe_intrastat["WartoscStatystyczna"] = dataframe_intrastat["WartoscStatystyczna"].astype("int64")

    # cast types in info file
    dataframe_info["UC"] = dataframe_info["UC"].astype("int64")
    dataframe_info["Rok"] = dataframe_info["Rok"].astype("int64")
    dataframe_info["Miesiac"] = dataframe_info["Miesiac"].astype("int64")
    dataframe_info["Numer"] = dataframe_info["Numer"].astype("int64")
    dataframe_info["Wersja"] = dataframe_info["Wersja"].astype("int64")
    dataframe_info["LacznaWartoscFaktur"] = dataframe_info["LacznaWartoscFaktur"].astype("int64")
    dataframe_info["LacznaWartoscStatystyczna"] = dataframe_info["LacznaWartoscStatystyczna"].astype("int64")
    dataframe_info["LacznaLiczbaPozycji"] = dataframe_info["LacznaLiczbaPozycji"].astype("int64")

    # save files
    dataframe_intrastat.to_excel("C:/data/Pomocnik/temp.xlsx", index=False)
    dataframe_info.to_excel(f"{destination_folder}/info.xlsx", index=False)

    exportf.exportf("C:/data/Pomocnik/temp.xlsx", db1_file, db2_file, destination_folder, destination_name)

    os.remove("C:/data/Pomocnik/temp.xlsx")