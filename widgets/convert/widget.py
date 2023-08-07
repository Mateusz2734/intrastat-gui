import os.path as p

from PyQt5.QtWidgets import QLabel, QPushButton, QFileDialog
from PyQt5 import uic

from config.paths import PATHS
from config.messages import MSG
from widgets.BaseWidget import BaseWidget
from widgets.convert.logic import convert


class ConvertWindow(BaseWidget):
    def __init__(self):
        super().__init__()
        self.xls_file = None

        # load UI file
        uic.loadUi(p.join(PATHS.BASEDIR, p.normpath(PATHS.STYLE.CONVERT)), self)

        # define buttons
        self.btn_choose_file = self.findChild(QPushButton, "choose_file_btn")
        self.btn_ok = self.findChild(QPushButton, "btn_ok")

        # define labels
        self.label_choose_file = self.findChild(QLabel, "choose_file_label")

        self.populate_labels()

        # click handlers
        self.btn_choose_file.clicked.connect(self.choose_file_handler)
        self.btn_ok.clicked.connect(self.ok_handler)

    def populate_labels(self):
        self.label_choose_file.setText(self.xls_file)

    def choose_file_handler(self):
        fpath = QFileDialog.getOpenFileName(
            self, "Wybierz plik, którego rodzaj chcesz zmienić", PATHS.DESKTOP, MSG.FILES.XLS)
        if fpath[0] != "":
            self.label_choose_file.setText(fpath[0])
            self.xls_file = fpath[0]

    def ok_handler(self):
        if self.xls_file is not None:
            self.run_worker(convert, self.xls_file)
        else:
            self.show_warning(MSG.WARNINGS.MISSING_DATA)
