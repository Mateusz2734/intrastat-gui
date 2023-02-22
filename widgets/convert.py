import os

from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtCore import QThread, Qt
from PyQt5 import uic

from workers.ConvertWorker import ConvertWorker
from widgets.loader import Loader

basedir = os.path.dirname(os.path.dirname(__file__))


class ConvertWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.xls_file = None
        self.user = os.getlogin()

        self.loader = Loader()

        # load UI file
        uic.loadUi(os.path.join(basedir, "./ui/convert.ui"), self)

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
        self.worker.finished.connect(self.hide_loader)
        self.worker.finished.connect(self.show_message)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def show_message(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Gotowe!")
        msg.setStyleSheet(
            "QMessageBox {border: 2px solid #4891b4; border-radius:15px}")
        msg.setText("Plik został przetworzony.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowFlag(Qt.FramelessWindowHint)
        msg.exec()

    def show_warning(self):
        warn = QMessageBox(self)
        warn.setStyleSheet(
            "QMessageBox {border: 2px solid #4891b4; border-radius:15px}")
        warn.setWindowTitle("Ups!")
        warn.setText("Proszę podać wszystkie dane i spróbowac ponownie.")
        warn.setStandardButtons(QMessageBox.Ok)
        warn.setIcon(QMessageBox.Warning)
        warn.setWindowFlag(Qt.FramelessWindowHint)
        warn.exec()

    def show_loader(self):
        self.loader.show()

    def hide_loader(self):
        self.loader.hide()

    def ok_handler(self):
        if self.xls_file is not None:
            self.runConvertWorker()
        else:
            self.show_warning()
