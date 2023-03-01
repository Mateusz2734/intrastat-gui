import logging as log

from PyQt5.QtCore import QObject, pyqtSignal

from widgets.convert.logic import convert


class ConvertWorker(QObject):
    def __init__(self, xls_file):
        super().__init__()
        self.xls_file = xls_file
        # log = logging.getLogger(__name__)

    finished = pyqtSignal()
    started = pyqtSignal()
    error = pyqtSignal()

    def run(self):
        self.started.emit()
        try:
            convert(self.xls_file)
        except Exception as e:
            log.error(f"{__name__} :: {str(e)}")
            self.error.emit()
        else:
            self.finished.emit()
