from PyQt5.QtCore import QObject, pyqtSignal

from logic.importf import importf


class ImportWorker(QObject):
    def __init__(self, intrastat_file, db_file, db2_file):
        super().__init__()
        self.intrastat_file = intrastat_file
        self.db_file = db_file
        self.db2_file = db2_file

    finished = pyqtSignal()
    started = pyqtSignal()

    def run(self):
        self.started.emit()
        importf(self.intrastat_file, self.db_file, self.db2_file)
        self.finished.emit()
