import os.path as p
from shutil import copy2

from PyQt5.QtWidgets import QPushButton, QLabel, QFileDialog
from PyQt5 import uic

from config.paths import PATHS
from config.messages import MSG
from widgets.BaseWidget import BaseWidget
from widgets.settings.logic import read_settings, save_settings, move_file


class SettingsWindow(BaseWidget):
    def __init__(self):
        super().__init__()
        self.path = PATHS.SETTINGS
        self.settings = read_settings()

        # load UI file
        uic.loadUi(p.join(PATHS.BASEDIR, p.normpath(PATHS.STYLE.SETTINGS)), self)

        # define buttons
        self.ok_btn = self.findChild(QPushButton, "ok_btn")
        self.intrastat_db1_btn = self.findChild(QPushButton, "intrastat_db1_btn")
        self.intrastat_db2_btn = self.findChild(QPushButton, "intrastat_db2_btn")
        self.invoice_db_btn = self.findChild(QPushButton, "invoice_db_btn")
        self.sampa_db_btn = self.findChild(QPushButton, "sampa_db_btn")
        self.desha_db_btn = self.findChild(QPushButton, "desha_db_btn")
        self.sem_db_btn = self.findChild(QPushButton, "sem_db_btn")

        # define labels
        self.intrastat_db1_file = self.findChild(QLabel, "intrastat_db1_file")
        self.intrastat_db2_file = self.findChild(QLabel, "intrastat_db2_file")
        self.invoice_db_file = self.findChild(QLabel, "invoice_db_file")
        self.sampa_db_file = self.findChild(QLabel, "sampa_db_file")
        self.desha_db_file = self.findChild(QLabel, "desha_db_file")
        self.sem_db_file = self.findChild(QLabel, "sem_db_file")

        self.populate_labels()

        self.ok_btn.clicked.connect(self.handle_save_settings)
        self.intrastat_db1_btn.clicked.connect(
            lambda: self.handle_choose_db("intrastat", "db1")
        )
        self.intrastat_db2_btn.clicked.connect(
            lambda: self.handle_choose_db("intrastat", "db2")
        )
        self.invoice_db_btn.clicked.connect(
            lambda: self.handle_choose_db("invoice", "db")
        )
        self.sampa_db_btn.clicked.connect(lambda: self.handle_choose_db("sampa", "db"))
        self.desha_db_btn.clicked.connect(lambda: self.handle_choose_db("desha", "db"))
        self.sem_db_btn.clicked.connect(lambda: self.handle_choose_db("sem", "db"))

    def populate_labels(self):
        self.intrastat_db1_file.setText(self.settings["intrastat"]["db1"])
        self.intrastat_db2_file.setText(self.settings["intrastat"]["db2"])
        self.invoice_db_file.setText(self.settings["invoice"]["db"])
        self.sampa_db_file.setText(self.settings["sampa"]["db"])
        self.desha_db_file.setText(self.settings["desha"]["db"])
        self.sem_db_file.setText(self.settings["sem"]["db"])

    def handle_save_settings(self):
        if save_settings(self.settings):
            self.show_message(MSG.SUCCESS.SETTINGS_SAVED)
        else:
            self.show_warning(MSG.WARNINGS.INVALID_JSON)

    def handle_choose_db(self, key1, key2):
        fpath = QFileDialog.getOpenFileName(
            self,
            f"Wybierz bazę danych {key1}/{key2}",
            PATHS.MAIN,
            MSG.FILES.EXCEL,
        )

        if fpath[0] == "":
            return

        moved_path = move_file(fpath[0])

        if moved_path == "":
            self.show_warning(MSG.ERRORS.CANT_PROCESS)
            return

        self.settings[key1][key2] = moved_path
        self.populate_labels()

        self.show_message(MSG.SUCCESS.DB_CHANGED)

        save_settings(self.settings)
