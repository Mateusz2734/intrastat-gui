import os
import os.path as p

from PyQt5.QtWidgets import QLabel, QPushButton, QFileDialog
from PyQt5.QtCore import QThread
from PyQt5 import uic

from widgets.convert.worker import ConvertWorker
from widgets.BaseWidget import BaseWidget

basedir = p.dirname(p.dirname(p.dirname(__file__)))


class ConvertWindow(BaseWidget):
    def __init__(self):
        super().__init__()
        self.xls_file = None
        self.user = os.getlogin()

        # load UI file
        uic.loadUi(p.join(basedir, p.normpath("./style/convert.ui")), self)

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
            self, "Wybierz plik, którego rodzaj chcesz zmienić", f"C:/Users/{self.user}/Desktop", "Pliki XLS (*.xls)")
        if fpath[0] != "":
            self.label_choose_file.setText(fpath[0])
            self.xls_file = fpath[0]

    def runConvertWorker(self):
        self.thread = QThread()

        self.worker = ConvertWorker(self.xls_file)

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
        if self.xls_file is not None:
            self.runConvertWorker()
        else:
            self.show_warning("Proszę uzupełnić wszystkie dane!")
