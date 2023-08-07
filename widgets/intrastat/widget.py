import os.path as p

from PyQt5.QtWidgets import QComboBox, QLabel, QPushButton, QFileDialog
from PyQt5 import uic

from config.paths import PATHS
from config.messages import MSG
from widgets.settings.logic import read_settings
from widgets.BaseWidget import BaseWidget
from widgets.intrastat.logic_export import exportf
from widgets.intrastat.logic_import import importf


class TYPES:
    EXPORT = "Wywozowy"
    IMPORT = "Przywozowy"


class IntrastatWindow(BaseWidget):

    def __init__(self):
        super().__init__()
        self.type = None

        try:
            self.settings = read_settings()["intrastat"]
            self.db_file = self.settings["db1"]
            self.db2_file = self.settings["db2"]
        except Exception:
            self.db_file = None
            self.db2_file = None

        self.intrastat_file = None

        # load UI file
        uic.loadUi(p.join(PATHS.BASEDIR, p.normpath(PATHS.STYLE.INTRASTAT)), self)

        # define buttons
        self.btn_choose_db = self.findChild(QPushButton, "choose_db_btn")
        self.btn_choose_file = self.findChild(QPushButton, "choose_file_btn")
        self.btn_choose_db2 = self.findChild(QPushButton, "choose_db2_btn")
        self.btn_ok = self.findChild(QPushButton, "btn_ok")

        # define labels
        self.label_choose_db = self.findChild(QLabel, "choose_db_label")
        self.label_choose_file = self.findChild(QLabel, "choose_file_label")
        self.label_choose_db2 = self.findChild(QLabel, "choose_db2_label")

        self.populate_labels()

        # define other widgets
        self.choose_type = self.findChild(QComboBox, "intrastat_choose_type")

        # disable file buttons
        self.btn_choose_db.setEnabled(False)
        self.btn_choose_file.setEnabled(False)
        self.btn_choose_db2.setEnabled(False)

        # click handlers
        self.btn_choose_db.clicked.connect(self.choose_db_handler)
        self.btn_choose_db2.clicked.connect(self.choose_db2_handler)
        self.btn_choose_file.clicked.connect(self.choose_file_handler)
        self.btn_ok.clicked.connect(self.ok_handler)

        # other handlers
        self.choose_type.activated.connect(self.choose_type_handler)

    def populate_labels(self):
        self.label_choose_file.setText(self.intrastat_file)
        self.label_choose_db.setText(self.db_file)
        self.label_choose_db2.setText(self.db2_file)

    def choose_type_handler(self):
        if self.choose_type.currentText() != "Wybierz rodzaj Intrastatu":
            self.type = self.choose_type.currentText()
            self.btn_choose_db.setEnabled(True)
            self.btn_choose_file.setEnabled(True)
            self.btn_choose_db2.setEnabled(True)
        else:
            self.btn_choose_db.setEnabled(False)
            self.btn_choose_file.setEnabled(False)
            self.btn_choose_db2.setEnabled(False)

    def choose_db_handler(self):
        fpath = QFileDialog.getOpenFileName(
            self, "Wybierz bazę danych", PATHS.DESKTOP, MSG.FILES.EXCEL)
        if fpath[0] != "":
            self.label_choose_db.setText(fpath[0])
            self.db_file = fpath[0]

    def choose_db2_handler(self):
        fpath = QFileDialog.getOpenFileName(
            self, "Wybierz bazę kodów", PATHS.DESKTOP, MSG.FILES.EXCEL)
        if fpath[0] != "":
            self.label_choose_db2.setText(fpath[0])
            self.db2_file = fpath[0]

    def choose_file_handler(self):
        if self.type == TYPES.EXPORT:
            fpath = QFileDialog.getOpenFileName(
                self, "Wybierz plik Intrastatu", PATHS.DESKTOP, MSG.FILES.EXCEL)
            if fpath[0] != "":
                self.label_choose_file.setText(fpath[0])
                self.intrastat_file = fpath[0]
        elif self.type == TYPES.IMPORT:
            fpath = QFileDialog.getExistingDirectory(
                self, "Wybierz folder z plikami .xml Intrastatu", PATHS.DESKTOP)
            if fpath != "":
                self.label_choose_file.setText(fpath)
                self.intrastat_file = fpath

    def ok_handler(self):
        if self.choose_type.currentText() != "Wybierz rodzaj Intrastatu" and (self.db_file and self.db2_file and self.intrastat_file) is not None:
            if self.type == TYPES.EXPORT:
                self.run_worker(exportf, self.intrastat_file,
                                self.db_file, self.db2_file)
            elif self.type == TYPES.IMPORT:
                self.run_worker(importf, self.intrastat_file,
                                self.db_file, self.db2_file)
        else:
            self.show_warning(MSG.WARNINGS.MISSING_DATA)
