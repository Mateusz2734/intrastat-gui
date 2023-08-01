from typing import Type
import sys
import os
import logging
import logging.config


from PyQt5.QtWidgets import QApplication, QMainWindow, QMdiArea, QPushButton
from PyQt5 import uic
from PyQt5 import QtGui

from widgets.settings.logic import create_settings
from widgets.intrastat.widget import IntrastatWindow
from widgets.invoice.widget import InvoiceWindow
from widgets.convert.widget import ConvertWindow
from widgets.sampa.widget import SampaWindow
from widgets.desha.widget import DeshaWindow
from widgets.settings.widget import SettingsWindow
from widgets.BaseWidget import BaseWidget

# import pyi_splash # type: ignore

basedir = os.path.dirname(__file__)
logging.config.fileConfig(os.path.join(basedir, "./log/logging.conf"))
log = logging.getLogger(__name__)


class MESSAGES:
    INTRASTAT = "INTRASTAT | Wprowadź informacje"
    INVOICE = "FAKTURA | Wprowadź informacje"
    CONVERT = "ZMIANA PLIKU | Wprowadź informacje"
    SAMPA = "SAMPA | Wprowadź informacje"
    DESHA = "DESHA | Wprowadź informacje"
    SETTINGS = "USTAWIENIA | Zmień domyślne wartości"


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowIcon(QtGui.QIcon(os.path.join(basedir, "./imgs/helper.png")))

        # load UI file
        uic.loadUi(os.path.join(basedir, "./style/main.ui"), self)

        # define widgets and buttons
        self.mdi = self.findChild(QMdiArea, "mdiArea")
        self.intrastat_btn = self.findChild(QPushButton, "intrastat_btn")
        self.invoice_btn = self.findChild(QPushButton, "invoice_btn")
        self.convert_btn = self.findChild(QPushButton, "convert_btn")
        self.sampa_btn = self.findChild(QPushButton, "sampa_btn")
        self.desha_btn = self.findChild(QPushButton, "desha_btn")
        self.settings_btn = self.findChild(QPushButton, "settings_btn")

        # button click handlers
        self.intrastat_btn.clicked.connect(
            lambda: self.add_window(IntrastatWindow, MESSAGES.INTRASTAT)
        )
        self.invoice_btn.clicked.connect(
            lambda: self.add_window(InvoiceWindow, MESSAGES.INVOICE)
        )
        self.convert_btn.clicked.connect(
            lambda: self.add_window(ConvertWindow, MESSAGES.CONVERT)
        )
        self.sampa_btn.clicked.connect(
            lambda: self.add_window(SampaWindow, MESSAGES.SAMPA)
        )
        self.desha_btn.clicked.connect(
            lambda: self.add_window(DeshaWindow, MESSAGES.DESHA)
        )
        self.settings_btn.clicked.connect(
            lambda: self.add_window(SettingsWindow, MESSAGES.SETTINGS)
        )

        # create settings file
        create_settings()

        # close splash screen
        # pyi_splash.close()

        # show main window
        self.show()

    def add_window(self, window: Type[BaseWidget], msg: str):
        page = window()
        subwindow = self.mdi.addSubWindow(page)
        subwindow.setWindowTitle(msg)
        subwindow.show()
        self.mdi.tileSubWindows()


app = QApplication(sys.argv)
File = open(os.path.join(basedir, "style/style.qss"), "r")

with File:
    qss = File.read()
    app.setStyleSheet(qss)


MainWindow = MainWindow()
app.exec_()
