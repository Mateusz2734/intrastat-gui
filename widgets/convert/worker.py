from PyQt5.QtCore import QObject, pyqtSignal

from widgets.convert.logic import convert


class ConvertWorker(QObject):
    def __init__(self, xls_file):
        super().__init__()
        self.xls_file = xls_file

    finished = pyqtSignal()
    started = pyqtSignal()
    error = pyqtSignal()

    def run(self):
        self.started.emit()
        try:
            convert(self.xls_file)
        except Exception:
            self.error.emit()
        else:
            self.finished.emit()
