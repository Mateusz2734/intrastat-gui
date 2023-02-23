import os

from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5 import uic

from widgets.loader import Loader

basedir = os.path.dirname(os.path.dirname(__file__))


class BaseWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        self.loader = Loader()

    def show_message(self, message: str):
        msg = QMessageBox(self)
        msg.setWindowTitle("Gotowe!")
        msg.setStyleSheet(
            "QMessageBox {border: 2px solid #4891b4; border-radius:15px}")
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowFlag(Qt.FramelessWindowHint)
        msg.exec()

    def show_warning(self, warning: str):
        warn = QMessageBox(self)
        warn.setStyleSheet(
            "QMessageBox {border: 2px solid #4891b4; border-radius:15px}")
        warn.setWindowTitle("Ups!")
        warn.setText(warning)
        warn.setStandardButtons(QMessageBox.Ok)
        warn.setIcon(QMessageBox.Warning)
        warn.setWindowFlag(Qt.FramelessWindowHint)
        warn.exec()

    def show_error(self, error: str):
        err = QMessageBox(self)
        err.setStyleSheet(
            "QMessageBox {border: 2px solid #4891b4; border-radius:15px}")
        err.setWindowTitle("Ups!")
        err.setText(error)
        err.setStandardButtons(QMessageBox.Ok)
        err.setIcon(QMessageBox.Critical)
        err.setWindowFlag(Qt.FramelessWindowHint)
        err.exec()

    def show_loader(self):
        self.loader.show()

    def hide_loader(self):
        self.loader.hide()
