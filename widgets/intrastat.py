from PyQt5.QtWidgets import QComboBox, QMainWindow, QLabel, QPushButton, QFileDialog
from PyQt5 import uic
from os import getlogin
 
class IntrastatWindow(QMainWindow):
    def __init__(self):
        super(IntrastatWindow, self).__init__()
        self.type = None
        self.db_file = None
        self.db2_file = None
        self.intrastat_file = None
        self.user = getlogin()

        # load UI file
        uic.loadUi("./ui/intrastat.ui", self)

        # define widgets and buttons
        self.choose_type = self.findChild(QComboBox, "intrastat_choose_type")
        self.btn_choose_db = self.findChild(QPushButton, "choose_db_btn")
        self.label_choose_db = self.findChild(QLabel, "choose_db_label")
        self.btn_choose_file = self.findChild(QPushButton, "choose_file_btn")
        self.label_choose_file = self.findChild(QLabel, "choose_file_label")
        self.btn_choose_db2 = self.findChild(QPushButton, "choose_db2_btn")
        self.label_choose_db2 = self.findChild(QLabel, "choose_db2_label")
        self.btn_ok = self.findChild(QPushButton, "btn_ok")

        # disable file buttons
        self.btn_choose_db.setEnabled(False)
        self.btn_choose_file.setEnabled(False)
        self.btn_choose_db2.setEnabled(False)
        
        # add click handlers
        self.choose_type.activated.connect(self.choose_type_handler)
        self.btn_choose_db.clicked.connect(self.choose_db_handler)
        self.btn_choose_db2.clicked.connect(self.choose_db2_handler)
        self.btn_choose_file.clicked.connect(self.choose_file_handler)
        self.btn_ok.clicked.connect(self.ok_handler)

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
        fpath = QFileDialog.getOpenFileName(self, "Wybierz bazę danych", f"C:/Users/{self.user}/Desktop", "Pliki CSV (*.csv);;Wszystkie Pliki (*)")
        if fpath[0] != "":
            self.label_choose_db.setText(fpath[0])
            self.db_file = fpath[0]

    def choose_db2_handler(self):
        fpath = QFileDialog.getOpenFileName(self, "Wybierz bazę kodów", f"C:/Users/{self.user}/Desktop", "Skoroszyt programu Excel  (*.xlsx);;Wszystkie Pliki (*)")
        if fpath[0] != "":
            self.label_choose_db2.setText(fpath[0])
            self.db2_file = fpath[0]
    
    def choose_file_handler(self): 
        if self.type == "Wywozowy":
            fpath = QFileDialog.getOpenFileName(self, "Wybierz plik Intrastatu", "", "Skoroszyt programu Excel  (*.xlsx);;Wszystkie Pliki (*)")
        elif self.type == "Przywozowy":
            fpath = QFileDialog.getOpenFileName(self, "Wybierz plik Intrastatu", "", "Plik XML  (*.xml);;Wszystkie Pliki (*)")
        if fpath[0] != "":
            self.label_choose_file.setText(fpath[0])
            self.intrastat_file = fpath[0]

    def ok_handler(self):
        print(self.type, self.db_file, self.db2_file, self.intrastat_file)
