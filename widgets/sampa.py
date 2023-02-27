import os

from PyQt5.QtWidgets import QLabel, QPushButton, QFileDialog
from PyQt5.QtCore import QThread
from PyQt5 import uic

from workers.SampaWorker import SampaWorker
from logic.settings import read_settings
from widgets.BaseWidget import BaseWidget

basedir = os.path.dirname(os.path.dirname(__file__))


class SampaWindow(BaseWidget):
    def __init__(self):
        super().__init__()
        self.settings = read_settings()["sampa"]
        self.db_file = self.settings["db"]
        self.sampa_file = None
        self.user = os.getlogin()

        # load UI file
        uic.loadUi(os.path.join(basedir, "./ui/sampa.ui"), self)

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
        self.label_choose_file.setText(self.sampa_file)
        self.label_choose_db.setText(self.db_file)

    def choose_db_handler(self):
        fpath = QFileDialog.getOpenFileName(
            self, "Wybierz bazę danych", f"C:/Users/{self.user}/Desktop", "Pliki Excel (*.xlsx)")
        if fpath[0] != "":
            self.label_choose_db.setText(fpath[0])
            self.db_file = fpath[0]

    def choose_file_handler(self):
        fpath = QFileDialog.getOpenFileName(
            self, "Wybierz plik faktury", f"C:/Users/{self.user}/Desktop", "Pliki Excel (*.xlsx)")
        if fpath[0] != "":
            self.label_choose_file.setText(fpath[0])
            self.sampa_file = fpath[0]

    def runInvoiceWorker(self):
        self.thread = QThread()

        self.worker = SampaWorker(self.sampa_file, self.db_file)

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.started.connect(self.show_loader)

        # In case of error
        self.worker.error.connect(self.hide_loader)
        self.worker.error.connect(
            lambda: self.show_error("Wystąpił błąd w trakcie przetwarzania pliku"))
        self.worker.error.connect(self.thread.quit)
        self.worker.error.connect(self.worker.deleteLater)

        # If everything works fine
        self.worker.finished.connect(self.hide_loader)
        self.worker.finished.connect(
            lambda: self.show_message("Plik przetworzony pomyślnie."))
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)

        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def ok_handler(self):
        if (self.db_file and self.sampa_file) is not None:
            self.runInvoiceWorker()
        else:
            self.show_warning("Proszę uzupełnić wszystkie dane!")
