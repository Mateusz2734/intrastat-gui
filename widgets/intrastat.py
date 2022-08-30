from PyQt5.QtWidgets import QComboBox, QMainWindow, QLabel, QPushButton, QFileDialog
from PyQt5 import uic
 
class IntrastatWindow(QMainWindow):
    def __init__(self):
        super(IntrastatWindow, self).__init__()
        self.type = None
        self.db_file = None
        self.intrastat_file = None

        # load UI file
        uic.loadUi("./ui/intrastat.ui", self)

        # define widgets and buttons
        self.choose_type = self.findChild(QComboBox, "intrastat_choose_type")
        self.btn_choose_db = self.findChild(QPushButton, "choose_db_btn")
        self.label_choose_db = self.findChild(QLabel, "choose_db_label")
        self.label_choose_file = self.findChild(QLabel, "choose_file_label")
        self.btn_choose_file = self.findChild(QPushButton, "choose_file_btn")
        self.btn_ok = self.findChild(QPushButton, "btn_ok")
        self.btn_cancel = self.findChild(QPushButton, "btn_cancel")

        # add click handlers
        self.btn_choose_db.clicked.connect(self.choose_db)

    def choose_db(self):
        fpath = QFileDialog.getOpenFileName(self, "Wybierz bazę danych", "", "Pliki CSV (*.csv);;Wszystkie Pliki (*)")
        if fpath[0] != "":
            print(fpath[0])
            self.label_choose_db.setText(fpath[0].split("/")[-1])
            self.db_file = fpath[0]