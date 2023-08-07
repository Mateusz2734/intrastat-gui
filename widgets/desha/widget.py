import os.path as p

from PyQt5.QtWidgets import QLabel, QPushButton, QFileDialog
from PyQt5 import uic

from config.paths import PATHS
from config.messages import MSG
from widgets.settings.logic import read_settings
from widgets.BaseWidget import BaseWidget
from widgets.desha.logic import desha

basedir = p.dirname(p.dirname(p.dirname(__file__)))


class DeshaWindow(BaseWidget):
    def __init__(self):
        super().__init__()
        try:
            self.settings = read_settings()["desha"]
            self.db_file = self.settings["db"]
        except Exception:
            self.db_file = None
        self.desha_file = None

        # load UI file
        uic.loadUi(p.join(basedir, p.normpath(PATHS.STYLE.DESHA)), self)

        # define buttons
        self.btn_choose_db = self.findChild(QPushButton, "choose_db_btn")
        self.btn_choose_file = self.findChild(QPushButton, "choose_file_btn")
        self.btn_ok = self.findChild(QPushButton, "btn_ok")

        # define labels
        self.label_choose_db = self.findChild(QLabel, "choose_db_label")
        self.label_choose_file = self.findChild(QLabel, "choose_file_label")

        self.populate_labels()

        # click handlers
        self.btn_choose_db.clicked.connect(self.choose_db_handler)
        self.btn_choose_file.clicked.connect(self.choose_file_handler)
        self.btn_ok.clicked.connect(self.ok_handler)

    def populate_labels(self):
        self.label_choose_file.setText(self.desha_file)
        self.label_choose_db.setText(self.db_file)

    def choose_db_handler(self):
        fpath = QFileDialog.getOpenFileName(
            self,
            "Wybierz bazę danych",
            PATHS.DESKTOP,
            MSG.FILES.EXCEL,
        )
        if fpath[0] != "":
            self.label_choose_db.setText(fpath[0])
            self.db_file = fpath[0]

    def choose_file_handler(self):
        fpath = QFileDialog.getOpenFileName(
            self,
            "Wybierz plik faktury",
            PATHS.DESKTOP,
            MSG.FILES.EXCEL,
        )
        if fpath[0] != "":
            self.label_choose_file.setText(fpath[0])
            self.desha_file = fpath[0]

    def ok_handler(self):
        if (self.db_file and self.desha_file) is not None:
            self.run_worker(desha, self.desha_file, self.db_file)
        else:
            self.show_warning(MSG.WARNINGS.MISSING_DATA)
