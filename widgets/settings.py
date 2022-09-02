from PyQt5.QtWidgets import QMainWindow, QPushButton, QMessageBox, QPlainTextEdit
from PyQt5.QtCore import Qt
from PyQt5 import uic
from os import getlogin
import os
import json
 
def is_json(candidate):
    try:
        json.loads(candidate)
    except ValueError as e:
        return False
    return True

basedir = os.path.dirname(os.path.dirname(__file__))

class SettingsWindow(QMainWindow):
    def __init__(self):
        super(SettingsWindow, self).__init__()
        self.user = getlogin()
        self.path = "C:/Skrypty/Pomocnik/settings.json"

        # load UI file
        uic.loadUi(os.path.join(basedir, "./ui/settings.ui"), self)

        # define widgets
        self.btn_ok = self.findChild(QPushButton, "btn_ok")
        self.editor = self.findChild(QPlainTextEdit, "editor")
        
        self.load_data()

        self.btn_ok.clicked.connect(self.save_data)

    # load data from .json file
    def load_data(self):
        with open(self.path, "r") as file:
            data = json.load(file)
            self.editor.setPlainText(json.dumps(data, indent=4, sort_keys=True))

    def save_data(self):
        data = self.editor.toPlainText()
        if is_json(data):
            json_data = json.dumps(json.loads(data), indent=4, sort_keys=True)
            with open(self.path, "w") as file:
                file.write(json_data)
                self.show_message()
        else:
            self.show_warning()
            
    def show_warning(self):
        warn = QMessageBox(self)
        warn.setStyleSheet("QMessageBox {border: 2px solid #4891b4; border-radius:15px}")
        warn.setWindowTitle("Ups!")
        warn.setText("Nieprawidłowy format pliku .json")
        warn.setStandardButtons(QMessageBox.Ok)
        warn.setIcon(QMessageBox.Warning)
        warn.setWindowFlag(Qt.FramelessWindowHint)
        warn.exec()

    def show_message(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Gotowe!")
        msg.setStyleSheet("QMessageBox {border: 2px solid #4891b4; border-radius:15px}")
        msg.setText("Pomyślnie zapisano ustawienia.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowFlag(Qt.FramelessWindowHint)
        msg.exec()