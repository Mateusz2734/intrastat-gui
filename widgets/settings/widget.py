import json
import yaml
import os.path as p

from PyQt5.QtWidgets import QPushButton, QPlainTextEdit
from PyQt5 import uic

from config.paths import PATHS
from config.messages import MSG
from widgets.BaseWidget import BaseWidget


def is_yaml(candidate):
    try:
        yaml.safe_load(candidate)
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
                data = yaml.safe_load(file)
                self.editor.setPlainText(yaml.safe_dump(data))
        except Exception:
            self.show_error(MSG.ERRORS.CANT_OPEN)

    def save_data(self):
        data = self.editor.toPlainText()
        if is_yaml(data):
            yaml_data = json.dumps(yaml.safe_load(data))
            with open(self.path, "w") as file:
                file.write(yaml_data)
                self.show_message(MSG.SUCCESS.SETTINGS_SAVED)
        else:
            self.show_warning(MSG.WARNINGS.INVALID_YAML)
