from PyQt5.QtCore import QObject, pyqtSignal
from logic.invoice import invoice

class InvoiceWorker(QObject):
    def __init__(self, intrastat_file, db_file):
        super().__init__()
        self.intrastat_file = intrastat_file
        self.db_file = db_file
    finished = pyqtSignal()
    started = pyqtSignal()

    def run(self):
        self.started.emit()
        invoice(self.intrastat_file, self.db_file)
        self.finished.emit()