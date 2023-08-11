import logging as log

from PyQt5.QtCore import QObject, pyqtSignal


class Worker(QObject):
    def __init__(self, logic, args, type=None):
        super().__init__()
        self.type = type
        self.logic = logic
        self.args = args

    finished = pyqtSignal(list)
    started = pyqtSignal()
    error = pyqtSignal()

    def run(self):
        self.started.emit()
        try:
            result = self.logic(self.args)
        except Exception as e:
            log.error(f"{__name__} :: {str(e)}")
            self.error.emit()
        else:
            if self.type is not None:
                self.finished.emit(result)
            else:
                self.finished.emit([])
