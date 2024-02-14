import json
import os.path as p

from PyQt5.QtWidgets import QPushButton, QPlainTextEdit
from PyQt5 import uic

from config.paths import PATHS
from config.messages import MSG
from widgets.BaseWidget import BaseWidget


def is_json(candidate):
    try:
        json.loads(candidate)
    except ValueError:
        return False
    return True


class SettingsWindow(BaseWidget):
    def __init__(self):
        super().__init__()
        self.path = PATHS.SETTINGS

        # load UI file
        uic.loadUi(p.join(PATHS.BASEDIR, p.normpath(PATHS.STYLE.SETTINGS)), self)

        # define widgets
        self.btn_ok = self.findChild(QPushButton, "btn_ok")
        self.editor = self.findChild(QPlainTextEdit, "editor")

        self.load_data()

        self.btn_ok.clicked.connect(self.save_data)

    # load data from .json file
    def load_data(self):
        try:
            with open(self.path, "r") as file:
                data = json.load(file)
                self.editor.setPlainText(json.dumps(
                    data, indent=4, sort_keys=True))
        except Exception:
            self.show_error(MSG.ERRORS.CANT_OPEN)

    def save_data(self):
        data = self.editor.toPlainText()
        if is_json(data):
            json_data = json.dumps(json.loads(data), indent=4, 
                                   sort_keys=True)
            with open(self.path, "w") as file:
                file.write(json_data)
                self.show_message(MSG.SUCCESS.SETTINGS_SAVED)
        else:
            self.show_warning(MSG.WARNINGS.INVALID_JSON)
