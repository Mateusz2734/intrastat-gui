import os
import os.path as p


class PATHS:
    MAIN = "C:/Skrypty/Pomocnik"
    SETTINGS = "C:/Skrypty/Pomocnik/settings.yaml"
    DESKTOP = f"C:/Users/{os.getlogin()}/Desktop"
    BASEDIR = f"{p.dirname(p.dirname(__file__))}"
    TEMP = "C:/Skrypty/Pomocnik/temp.xlsx"
    LOGGING = "./log/logging.conf"
    ICON = "./imgs/helper.png"

    class STYLE:
        SETTINGS = "./style/settings.ui"
        SAMPA = "./style/sampa.ui"
        INVOICE = "./style/invoice.ui"
        INTRASTAT = "./style/intrastat.ui"
        DESHA = "./style/desha.ui"
        CONVERT = "./style/convert.ui"
        MAIN = "./style/main.ui"
        DUPLICATES = "./style/duplicates.ui"
        LOADER = "./imgs/loader.gif"
        STYLESHEET = "style/style.qss"

