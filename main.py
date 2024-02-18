from typing import Type
import sys
import os
import logging
import logging.config as cfg

from PyQt5 import QtGui, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QMdiArea,
    QPushButton,
    QWidget,
    QVBoxLayout,
)

from config.messages import MSG
from config.paths import PATHS
from widgets.settings.logic import create_settings
from widgets.intrastat.widget import IntrastatWindow
from widgets.invoice.widget import InvoiceWindow
from widgets.convert.widget import ConvertWindow
from widgets.sampa.widget import SampaWindow
from widgets.desha.widget import DeshaWindow
from widgets.sem.widget import SemWindow
from widgets.duplicates.widget import DuplicatesWindow
from widgets.settings.widget import SettingsWindow
from widgets.BaseWidget import BaseWidget
from widgets.loader import Loader

# import pyi_splash # type: ignore

cfg.fileConfig(os.path.join(PATHS.BASEDIR, PATHS.LOGGING))
log = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.overlay = None
        self.loader = Loader()

        self.setWindowIcon(QtGui.QIcon(os.path.join(PATHS.BASEDIR, PATHS.ICON)))

        # load UI file
        uic.loadUi(os.path.join(PATHS.BASEDIR, PATHS.STYLE.MAIN), self)

        # define widgets and buttons
        self.mdi = self.findChild(QMdiArea, "mdiArea")
        self.intrastat_btn = self.findChild(QPushButton, "intrastat_btn")
        self.invoice_btn = self.findChild(QPushButton, "invoice_btn")
        self.convert_btn = self.findChild(QPushButton, "convert_btn")
        self.sampa_btn = self.findChild(QPushButton, "sampa_btn")
        self.desha_btn = self.findChild(QPushButton, "desha_btn")
        self.sem_btn = self.findChild(QPushButton, "sem_btn")
        self.duplicates_btn = self.findChild(QPushButton, "duplicates_btn")
        self.settings_btn = self.findChild(QPushButton, "settings_btn")

        self.prepare_overlay()

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
        self.sem_btn.clicked.connect(lambda: self.add_window(SemWindow, MSG.TITLES.SEM))
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
        page.start_loading.connect(self.handle_start_loading)
        page.end_loading.connect(self.handle_end_loading)
        subwindow = self.mdi.addSubWindow(page)
        subwindow.setWindowTitle(msg)
        subwindow.show()
        self.mdi.tileSubWindows()

    def handle_start_loading(self):
        self.overlay.setGeometry(0, 0, self.mdi.width(), self.mdi.height())
        self.overlay.show()

    def handle_end_loading(self):
        self.overlay.hide()

    def prepare_overlay(self):
        self.overlay = QWidget(self.mdi)
        self.overlay.setAttribute(Qt.WA_TranslucentBackground)

        layout = QVBoxLayout()

        layout.addWidget(self.loader, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.overlay.setLayout(layout)

        self.overlay.hide()

    def resizeEvent(self, event):
        super().resizeEvent(event)

        if self.overlay is None:
            return

        self.overlay.setGeometry(0, 0, self.mdi.width(), self.mdi.height())


if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open(os.path.join(PATHS.BASEDIR, PATHS.STYLE.STYLESHEET), "r") as stylesheet:
        qss = stylesheet.read()
        app.setStyleSheet(qss)

    main_window = MainWindow()
    app.exec()
