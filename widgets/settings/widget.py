import json
import os
import os.path as p

from PyQt5.QtWidgets import QPushButton, QPlainTextEdit
from PyQt5 import uic

from widgets.BaseWidget import BaseWidget


def is_json(candidate):
    try:
        json.loads(candidate)
    except ValueError:
        return False
    return True


basedir = p.dirname(p.dirname(p.dirname(__file__)))


class SettingsWindow(BaseWidget):
    def __init__(self):
        super().__init__()
        self.user = os.getlogin()
        self.path = "C:/Skrypty/Pomocnik/settings.json"

        # load UI file
        uic.loadUi(p.join(basedir, p.normpath("./style/settings.ui")), self)

        # define widgets
        self.btn_ok = self.findChild(QPushButton, "btn_ok")
        self.editor = self.findChild(QPlainTextEdit, "editor")

        self.load_data()

        self.btn_ok.clicked.connect(self.save_data)

    # load data from .json file
    def load_data(self):
        with open(self.path, "r") as file:
            data = json.load(file)
            self.editor.setPlainText(json.dumps(
                data, indent=4, sort_keys=True))

    def save_data(self):
        data = self.editor.toPlainText()
        if is_json(data):
            json_data = json.dumps(json.loads(data), indent=4, sort_keys=True)
            with open(self.path, "w") as file:
                file.write(json_data)
                self.show_message("Pomyślnie zapisano ustawienia.")
        else:
            self.show_warning("Nieprawidłowa postać pliku .json")
