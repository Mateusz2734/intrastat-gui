from PyQt5.QtWidgets import QApplication, QMainWindow, QMdiArea, QPushButton
from PyQt5 import uic
from PyQt5 import QtGui
import sys
from widgets.intrastat import IntrastatWindow
from widgets.invoice import InvoiceWindow
 
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowIcon(QtGui.QIcon('./imgs/helper.png'))

        # load UI file
        uic.loadUi("./ui/main.ui", self)

        # define widgets and buttons
        self.mdi = self.findChild(QMdiArea, "mdiArea")
        self.intrastat_btn = self.findChild(QPushButton, "intrastat_btn")
        self.invoice_btn = self.findChild(QPushButton, "invoice_btn")
 
        # button click handlers
        self.intrastat_btn.clicked.connect(self.add_window_intrastat)
        self.invoice_btn.clicked.connect(self.add_window_invoice)
    
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

app = QApplication(sys.argv)
File = open("ui/style.qss",'r')

with File:
	qss = File.read()
	app.setStyleSheet(qss)


MainWindow = MainWindow()
app.exec_()