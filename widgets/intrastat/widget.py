import os
import os.path as p

from PyQt5.QtWidgets import QComboBox, QLabel, QPushButton, QFileDialog
from PyQt5.QtCore import QThread
from PyQt5 import uic

from widgets.intrastat.worker_export import ExportWorker
from widgets.intrastat.worker_import import ImportWorker
from widgets.settings.logic import read_settings
from widgets.BaseWidget import BaseWidget

basedir = p.dirname(p.dirname(p.dirname(__file__)))



class IntrastatWindow(BaseWidget):

    def __init__(self):
        super().__init__()
        self.settings = read_settings()["intrastat"]
        self.user = os.getlogin()
        self.type = None
        self.db_file = self.settings["db1"]
        self.db2_file = self.settings["db2"]
        self.intrastat_file = None

        # load UI file
        uic.loadUi(p.join(basedir, p.normpath("./style/intrastat.ui")), self)

        # define buttons
        self.btn_choose_db = self.findChild(QPushButton, "choose_db_btn")
        self.btn_choose_file = self.findChild(QPushButton, "choose_file_btn")
        self.btn_choose_db2 = self.findChild(QPushButton, "choose_db2_btn")
        self.btn_ok = self.findChild(QPushButton, "btn_ok")

        # define labels
        self.label_choose_db = self.findChild(QLabel, "choose_db_label")
        self.label_choose_file = self.findChild(QLabel, "choose_file_label")
        self.label_choose_db2 = self.findChild(QLabel, "choose_db2_label")

        self.populate_labels()

        # define other widgets
        self.choose_type = self.findChild(QComboBox, "intrastat_choose_type")

        # disable file buttons
        self.btn_choose_db.setEnabled(False)
        self.btn_choose_file.setEnabled(False)
        self.btn_choose_db2.setEnabled(False)

        # click handlers
        self.btn_choose_db.clicked.connect(self.choose_db_handler)
        self.btn_choose_db2.clicked.connect(self.choose_db2_handler)
        self.btn_choose_file.clicked.connect(self.choose_file_handler)
        self.btn_ok.clicked.connect(self.ok_handler)

        # other handlers
        self.choose_type.activated.connect(self.choose_type_handler)

    def populate_labels(self):
        self.label_choose_file.setText(self.intrastat_file)
        self.label_choose_db.setText(self.db_file)
        self.label_choose_db2.setText(self.db2_file)

    def choose_type_handler(self):
        if self.choose_type.currentText() != "Wybierz rodzaj Intrastatu":
            self.type = self.choose_type.currentText()
            self.btn_choose_db.setEnabled(True)
            self.btn_choose_file.setEnabled(True)
            self.btn_choose_db2.setEnabled(True)
        else:
            self.btn_choose_db.setEnabled(False)
            self.btn_choose_file.setEnabled(False)
            self.btn_choose_db2.setEnabled(False)

    def choose_db_handler(self):
        fpath = QFileDialog.getOpenFileName(
            self, "Wybierz bazę danych", f"C:/Users/{self.user}/Desktop", "Pliki CSV (*.csv)")
        if fpath[0] != "":
            self.label_choose_db.setText(fpath[0])
            self.db_file = fpath[0]

    def choose_db2_handler(self):
        fpath = QFileDialog.getOpenFileName(
            self, "Wybierz bazę kodów", f"C:/Users/{self.user}/Desktop", "Skoroszyt programu Excel  (*.xlsx)")
        if fpath[0] != "":
            self.label_choose_db2.setText(fpath[0])
            self.db2_file = fpath[0]

    def choose_file_handler(self):
        if self.type == "Wywozowy":
            fpath = QFileDialog.getOpenFileName(
                self, "Wybierz plik Intrastatu", f"C:/Users/{self.user}/Desktop", "Skoroszyt programu Excel  (*.xlsx)")
            if fpath[0] != "":
                self.label_choose_file.setText(fpath[0])
                self.intrastat_file = fpath[0]
        elif self.type == "Przywozowy":
            fpath = QFileDialog.getExistingDirectory(
                self, "Wybierz folder z plikami .xml Intrastatu", f"C:/Users/{self.user}/Desktop")
            if fpath != "":
                self.label_choose_file.setText(fpath)
                self.intrastat_file = fpath

    def runExportWorker(self):
        self.thread = QThread()

        self.worker = ExportWorker(
            self.intrastat_file, self.db_file, self.db2_file)

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.started.connect(self.show_loader)

        # In case of error
        self.worker.error.connect(self.hide_loader)
        self.worker.error.connect(
            lambda: self.show_error("Wystąpił błąd w trakcie przetwarzania pliku"))
        self.worker.error.connect(self.thread.quit)
        self.worker.error.connect(self.worker.deleteLater)

        # If everything works fine
        self.worker.finished.connect(self.hide_loader)
        self.worker.finished.connect(
            lambda: self.show_message("Plik przetworzony pomyślnie."))
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)

        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def runImportWorker(self):
        self.thread = QThread()

        self.worker = ImportWorker(
            self.intrastat_file, self.db_file, self.db2_file)

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.started.connect(self.show_loader)

        # In case of error
        self.worker.error.connect(self.hide_loader)
        self.worker.error.connect(
            lambda: self.show_error("Wystąpił błąd w trakcie przetwarzania pliku"))
        self.worker.error.connect(self.thread.quit)
        self.worker.error.connect(self.worker.deleteLater)

        # If everything works fine
        self.worker.finished.connect(self.hide_loader)
        self.worker.finished.connect(
            lambda: self.show_message("Plik przetworzony pomyślnie."))
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)

        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def ok_handler(self):
        if self.choose_type.currentText() != "Wybierz rodzaj Intrastatu" and (self.db_file and self.db2_file and self.intrastat_file) is not None:
            if self.type == "Wywozowy":
                self.runExportWorker()
            elif self.type == "Przywozowy":
                self.runImportWorker()
        else:
            self.show_warning("Proszę uzupełnić wszystkie dane!")
