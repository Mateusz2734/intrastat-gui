import os


class PATHS:
    SETTINGS = "C:/Skrypty/Pomocnik/settings.yaml"
    DESKTOP = f"C:/Users/{os.getlogin()}/Desktop"
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
        LOADER = "./imgs/loader.gif"
        STYLESHEET = "style/style.qss"
