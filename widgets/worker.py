import logging as log

from PyQt5.QtCore import QObject, pyqtSignal


class Worker(QObject):
    def __init__(self, logic, *args):
        super().__init__()
        self.logic = logic
        self.args = args

    finished = pyqtSignal()
    started = pyqtSignal()
    error = pyqtSignal()

    def run(self):
        self.started.emit()
        try:
            self.logic(self.args)
        except Exception as e:
            log.error(f"{__name__} :: {str(e)}")
            self.error.emit()
        else:
            self.finished.emit()
