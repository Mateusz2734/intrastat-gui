import logging as log

from PyQt5.QtCore import QObject, pyqtSignal

from widgets.desha.logic import desha


class DeshaWorker(QObject):
    def __init__(self, xlsx_file, db_file):
        super().__init__()
        self.xlsx_file = xlsx_file
        self.db_file = db_file

    finished = pyqtSignal()
    started = pyqtSignal()
    error = pyqtSignal()

    def run(self):
        self.started.emit()
        try:
            desha(self.xlsx_file, self.db_file)
        except Exception as e:
            log.error(f"{__name__} :: {str(e)}")
            self.error.emit()
        else:
            self.finished.emit()
