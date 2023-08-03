import os
import os.path as p

from PyQt5.QtWidgets import QLabel, QPushButton, QFileDialog
from PyQt5.QtCore import QThread
from PyQt5 import uic

from config.paths import PATHS
from config.messages import MSG
from widgets.desha.worker import DeshaWorker
from widgets.settings.logic import read_settings
from widgets.BaseWidget import BaseWidget

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
        self.user = os.getlogin()

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

    def runDeshaWorker(self):
        self.thread = QThread()

        self.worker = DeshaWorker(self.desha_file, self.db_file)

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.started.connect(self.show_loader)

        # In case of error
        self.worker.error.connect(self.hide_loader)
        self.worker.error.connect(
            lambda: self.show_error(MSG.ERRORS.CANT_PROCESS)
        )
        self.worker.error.connect(self.thread.quit)
        self.worker.error.connect(self.worker.deleteLater)

        # If everything works fine
        self.worker.finished.connect(self.hide_loader)
        self.worker.finished.connect(
            lambda: self.show_message(MSG.SUCCESS.FILE_PROCESSED)
        )
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)

        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def ok_handler(self):
        if (self.db_file and self.desha_file) is not None:
            self.runDeshaWorker()
        else:
            self.show_warning(MSG.WARNINGS.MISSING_DATA)
