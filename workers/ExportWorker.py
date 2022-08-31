from PyQt5.QtCore import QObject, pyqtSignal
from logic.exportf import exportf

class ExportWorker(QObject):
    def __init__(self, intrastat_file, db_file, db2_file, destination_folder, destination_name):
        super().__init__()
        self.intrastat_file = intrastat_file
        self.db_file = db_file
        self.db2_file = db2_file
        self.destination_folder = destination_folder
        self.destination_name = destination_name
    finished = pyqtSignal()
    started = pyqtSignal()

    def run(self):
        self.started.emit()
        exportf(self.intrastat_file, self.db_file, self.db2_file, self.destination_folder, self.destination_name)
        self.finished.emit()