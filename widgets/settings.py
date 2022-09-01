from PyQt5.QtWidgets import QComboBox, QMainWindow, QLabel, QPushButton, QFileDialog, QMessageBox, QPlainTextEdit
from PyQt5.QtCore import QThread, Qt
from workers.ExportWorker import ExportWorker
from workers.ImportWorker import ImportWorker
from widgets.loader import Loader
from PyQt5 import uic
from os import getlogin
import os
import json
 
basedir = os.path.dirname(os.path.dirname(__file__))

class SettingsWindow(QMainWindow):
    def __init__(self):
        super(SettingsWindow, self).__init__()
        self.user = getlogin()
        self.path = f"C:/Skrypty/Pomocnik/settings.json"

        # load UI file
        uic.loadUi(os.path.join(basedir, "./ui/settings.ui"), self)

        # define widgets
        self.btn_ok = self.findChild(QPushButton, "btn_ok")
        self.editor = self.findChild(QPlainTextEdit, "editor")
        self.load_data()

    def load_data(self):
        with open(self.path, "r") as f:
            data = json.load(f)
            self.editor.setPlainText(json.dumps(data, indent=4, sort_keys=True))

