from PyQt5.QtCore import QObject, pyqtSignal

from logic.sampa import sampa


class SampaWorker(QObject):
    def __init__(self, xls_file, db_file):
        super().__init__()
        self.xls_file = xls_file
        self.db_file = db_file

    finished = pyqtSignal()
    started = pyqtSignal()
    error = pyqtSignal()

    def run(self):
        self.started.emit()
        try:
            sampa(self.xls_file, self.db_file)
        except Exception:
            self.error.emit()
        else:
            self.finished.emit()
