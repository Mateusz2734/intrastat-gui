import logging as log

from PyQt5.QtCore import QObject, pyqtSignal

from widgets.invoice.logic import invoice


class InvoiceWorker(QObject):
    def __init__(self, intrastat_file, db_file):
        super().__init__()
        self.intrastat_file = intrastat_file
        self.db_file = db_file
        
    finished = pyqtSignal()
    started = pyqtSignal()
    error = pyqtSignal()

    def run(self):
        self.started.emit()
        try:
            invoice(self.intrastat_file, self.db_file)
        except Exception as e:
            log.error(f"{__name__} :: {str(e)}")
            self.error.emit()
        else:
            self.finished.emit()
