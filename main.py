from PyQt5.QtWidgets import QApplication, QMainWindow, QMdiArea, QAction, QMdiSubWindow, QTextEdit, QLabel, QPushButton
from PyQt5 import uic
from PyQt5 import QtGui
import sys
from widgets import intrastat
 
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowIcon(QtGui.QIcon('./imgs/helper.png'))

        # load UI file
        uic.loadUi("./ui/main.ui", self)

        # define widgets and buttons
        self.mdi = self.findChild(QMdiArea, "mdiArea")
        self.intrastat_btn = self.findChild(QPushButton, "intrastat_btn")
 
        # intrastat button click handler
        self.intrastat_btn.clicked.connect(self.add_window_intrastat)
    
        # show main window
        self.show()
       
    def add_window_intrastat(self):
        page = intrastat.IntrastatWindow()
        subwindow = self.mdi.addSubWindow(page)
        subwindow.setWindowTitle("Wprowadź informacje")

        subwindow.show()
        
        self.mdi.tileSubWindows()
 
app = QApplication(sys.argv)
MainWindow = MainWindow()
app.exec_()