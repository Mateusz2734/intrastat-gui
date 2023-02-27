from PyQt5.QtCore import QObject, pyqtSignal

from widgets.intrastat.logic_import import importf


class ImportWorker(QObject):
    def __init__(self, intrastat_file, db_file, db2_file):
        super().__init__()
        self.intrastat_file = intrastat_file
        self.db_file = db_file
        self.db2_file = db2_file

    finished = pyqtSignal()
    started = pyqtSignal()
    error = pyqtSignal()

    def run(self):
        self.started.emit()
        try:
            importf(self.intrastat_file, self.db_file, self.db2_file)
        except Exception:
            self.error.emit()
        else:
            self.finished.emit()
