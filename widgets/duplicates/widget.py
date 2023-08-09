import os.path as p

from PyQt5.QtWidgets import QComboBox, QLabel, QPushButton, QFileDialog
from PyQt5 import uic

from config.paths import PATHS
from config.messages import MSG
from widgets.BaseWidget import BaseWidget
from widgets.duplicates.logic import duplicates


class DuplicatesWindow(BaseWidget):

    def __init__(self):
        super().__init__()

        self.file = None
        self.column = None

        # load UI file
        uic.loadUi(p.join(PATHS.BASEDIR, p.normpath(
            PATHS.STYLE.DUPLICATES)), self)

        # define buttons
        self.btn_choose_file = self.findChild(QPushButton, "file_btn")
        self.btn_ok = self.findChild(QPushButton, "btn_ok")

        # define labels
        self.label_choose_file = self.findChild(QLabel, "file_label")
        self.label_choose_column = self.findChild(QLabel, "column_label")

        self.populate_labels()

        # define other widgets
        self.choose_column = self.findChild(QComboBox, "column_combo")

        # click handlers
        self.btn_choose_file.clicked.connect(self.choose_file_handler)
        self.btn_ok.clicked.connect(self.ok_handler)

        # other handlers
        self.choose_column.activated.connect(self.choose_column_handler)

    def populate_labels(self):
        self.label_choose_file.setText(self.file)
        self.label_choose_column.setText(self.column)

    def choose_column_handler(self):
        pass

    def choose_file_handler(self):
        fpath = QFileDialog.getOpenFileName(
            self, "Wybierz plik, z którego chcesz usunąć duplikaty", PATHS.DESKTOP, MSG.FILES.EXCEL)
        if fpath[0] != "":
            self.label_choose_file.setText(fpath[0])
            self.file = fpath[0]

    def ok_handler(self):
        if self.choose_column.currentText() != "Wybierz kolumnę" and (self.file and self.column) is not None:
            self.run_worker(duplicates, self.file, self.column)
        else:
            self.show_warning(MSG.WARNINGS.MISSING_DATA)
