import os

from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import Qt, QThread

from widgets.loader import Loader
from widgets.worker import Worker
from config.messages import MSG

STYLE = "QMessageBox {border: 2px solid #4891b4; border-radius:15px}"

class BaseWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        self.loader = Loader()

    def show_message(self, message: str):
        msg = QMessageBox(self)
        msg.setWindowTitle("Gotowe!")
        msg.setStyleSheet(STYLE)
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowFlag(Qt.FramelessWindowHint)
        msg.exec()

    def show_warning(self, warning: str):
        warn = QMessageBox(self)
        warn.setStyleSheet(STYLE)
        warn.setWindowTitle("Ups!")
        warn.setText(warning)
        warn.setStandardButtons(QMessageBox.Ok)
        warn.setIcon(QMessageBox.Warning)
        warn.setWindowFlag(Qt.FramelessWindowHint)
        warn.exec()

    def show_error(self, error: str):
        err = QMessageBox(self)
        err.setStyleSheet(STYLE)
        err.setWindowTitle("Ups!")
        err.setText(error)
        err.setStandardButtons(QMessageBox.Ok)
        err.setIcon(QMessageBox.Critical)
        err.setWindowFlag(Qt.FramelessWindowHint)
        err.exec()

    def run_worker(self, logic, args, err_msg=None, succ_msg=None):
        self.thread = QThread()

        self.worker = Worker(logic, args)

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.started.connect(self.show_loader)

        # In case of error
        self.worker.error.connect(self.hide_loader)
        self.worker.error.connect(
            lambda: self.show_error(err_msg if err_msg is not None else MSG.ERRORS.CANT_PROCESS))
        self.worker.error.connect(self.thread.quit)
        self.worker.error.connect(self.worker.deleteLater)

        # If everything works fine
        self.worker.finished.connect(self.hide_loader)
        self.worker.finished.connect(
            lambda: self.show_message(succ_msg if succ_msg is not None else MSG.SUCCESS.FILE_PROCESSED))
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)

        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def show_loader(self):
        self.loader.show()

    def hide_loader(self):
        self.loader.hide()
