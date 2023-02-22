from PyQt5.QtCore import QObject, pyqtSignal
from logic.convert_to_xlsx import convert


class ConvertWorker(QObject):
    def __init__(self, xls_file):
        super().__init__()
        self.xls_file = xls_file
    
    finished = pyqtSignal()
    started = pyqtSignal()

    def run(self):
        self.started.emit()
        convert(self.xls_file)
        self.finished.emit()
