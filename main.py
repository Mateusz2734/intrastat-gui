from typing import Type
import sys
import os
import logging
import logging.config as cfg


from PyQt5.QtWidgets import QApplication, QMainWindow, QMdiArea, QPushButton
from PyQt5 import uic
from PyQt5 import QtGui

from config.messages import MSG
from config.paths import PATHS
from widgets.settings.logic import create_settings
from widgets.intrastat.widget import IntrastatWindow
from widgets.invoice.widget import InvoiceWindow
from widgets.convert.widget import ConvertWindow
from widgets.sampa.widget import SampaWindow
from widgets.desha.widget import DeshaWindow
from widgets.duplicates.widget import DuplicatesWindow
from widgets.settings.widget import SettingsWindow
from widgets.BaseWidget import BaseWidget

# import pyi_splash # type: ignore

cfg.fileConfig(os.path.join(PATHS.BASEDIR, PATHS.LOGGING))
log = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(QtGui.QIcon(
            os.path.join(PATHS.BASEDIR, PATHS.ICON)))

        # load UI file
        uic.loadUi(os.path.join(PATHS.BASEDIR, PATHS.STYLE.MAIN), self)

        # define widgets and buttons
        self.mdi = self.findChild(QMdiArea, "mdiArea")
        self.intrastat_btn = self.findChild(QPushButton, "intrastat_btn")
        self.invoice_btn = self.findChild(QPushButton, "invoice_btn")
        self.convert_btn = self.findChild(QPushButton, "convert_btn")
        self.sampa_btn = self.findChild(QPushButton, "sampa_btn")
        self.desha_btn = self.findChild(QPushButton, "desha_btn")
        self.duplicates_btn = self.findChild(QPushButton, "duplicates_btn")
        self.settings_btn = self.findChild(QPushButton, "settings_btn")

        # button click handlers
        self.intrastat_btn.clicked.connect(
            lambda: self.add_window(IntrastatWindow, MSG.TITLES.INTRASTAT)
        )
        self.invoice_btn.clicked.connect(
            lambda: self.add_window(InvoiceWindow, MSG.TITLES.INVOICE)
        )
        self.convert_btn.clicked.connect(
            lambda: self.add_window(ConvertWindow, MSG.TITLES.CONVERT)
        )
        self.sampa_btn.clicked.connect(
            lambda: self.add_window(SampaWindow, MSG.TITLES.SAMPA)
        )
        self.desha_btn.clicked.connect(
            lambda: self.add_window(DeshaWindow, MSG.TITLES.DESHA)
        )
        self.duplicates_btn.clicked.connect(
            lambda: self.add_window(DuplicatesWindow, MSG.TITLES.DUPLICATES)
        )
        self.settings_btn.clicked.connect(
            lambda: self.add_window(SettingsWindow, MSG.TITLES.SETTINGS)
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


if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open(os.path.join(PATHS.BASEDIR, PATHS.STYLE.STYLESHEET), "r") as stylesheet:
        qss = stylesheet.read()
        app.setStyleSheet(qss)

    MainWindow()
    app.exec()
