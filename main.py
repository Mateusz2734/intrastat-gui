from PyQt5.QtWidgets import QApplication, QMainWindow, QMdiArea, QPushButton
from PyQt5 import uic
from PyQt5 import QtGui
import sys
from logic.settings import create_settings
from widgets.intrastat import IntrastatWindow
from widgets.invoice import InvoiceWindow
from widgets.convert import ConvertWindow
from widgets.settings import SettingsWindow
import os
# import pyi_splash # type: ignore

basedir = os.path.dirname(__file__)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowIcon(QtGui.QIcon(os.path.join(basedir, './imgs/helper.png')))

        # load UI file
        uic.loadUi(os.path.join(basedir, "./ui/main.ui"), self)

        # define widgets and buttons
        self.mdi = self.findChild(QMdiArea, "mdiArea")
        self.intrastat_btn = self.findChild(QPushButton, "intrastat_btn")
        self.invoice_btn = self.findChild(QPushButton, "invoice_btn")
        self.convert_btn = self.findChild(QPushButton, "convert_btn")
        self.settings_btn = self.findChild(QPushButton, "settings_btn")

        # button click handlers
        self.intrastat_btn.clicked.connect(self.add_window_intrastat)
        self.invoice_btn.clicked.connect(self.add_window_invoice)
        self.convert_btn.clicked.connect(self.add_window_convert)
        self.settings_btn.clicked.connect(self.add_window_settings)

        # create settings file
        create_settings()

        # close splash screen
        # pyi_splash.close()

        # show main window
        self.show()
       
    def add_window_intrastat(self):
        page = IntrastatWindow()
        subwindow = self.mdi.addSubWindow(page)
        subwindow.setWindowTitle("INTRASTAT | Wprowadź informacje")
        subwindow.show()
        self.mdi.tileSubWindows()

    def add_window_invoice(self):
        page = InvoiceWindow()
        subwindow = self.mdi.addSubWindow(page)
        subwindow.setWindowTitle("FAKTURA | Wprowadź informacje")
        subwindow.show()
        self.mdi.tileSubWindows()

    def add_window_convert(self):
        page = ConvertWindow()
        subwindow = self.mdi.addSubWindow(page)
        subwindow.setWindowTitle("ZMIANA PLIKU | Wprowadź informacje")
        subwindow.show()
        self.mdi.tileSubWindows()

    def add_window_settings(self):
        page = SettingsWindow()
        subwindow = self.mdi.addSubWindow(page)
        subwindow.setWindowTitle("USTAWIENIA | Zmień domyślne wartości")
        subwindow.show()
        self.mdi.tileSubWindows()


app = QApplication(sys.argv)
File = open(os.path.join(basedir, "ui/style.qss"),'r')

with File:
	qss = File.read()
	app.setStyleSheet(qss)


MainWindow = MainWindow()
app.exec_()