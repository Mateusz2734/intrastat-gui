from PyQt5.QtWidgets import QApplication, QMainWindow, QMdiArea, QAction, QMdiSubWindow, QTextEdit, QLabel, QPushButton, QDialog
from PyQt5 import uic
import sys
 
class IntrastatWindow(QMainWindow):
    def __init__(self):
        super(IntrastatWindow, self).__init__()

        # load UI file
        uic.loadUi("./ui/intrastat.ui", self)

        # define widgets and buttons
 
 
# class MainWindow(QMainWindow):
#     count = 0
#     def __init__(self):
#         super(MainWindow, self).__init__()

#         # load UI file
#         uic.loadUi("./ui/main.ui", self)

#         # define widgets and buttons
#         self.mdi = self.findChild(QMdiArea, "mdiArea")
#         self.intrastat_btn = self.findChild(QPushButton, "intrastat_btn")
 
#         # intrastat button click handler
#         self.intrastat_btn.clicked.connect(self.add_window)
    
#         # show main window
#         self.show()
       
#     def add_window(self):
#         page = IntrastatWindow()
#         subwindow = self.mdi.addSubWindow(page)
#         subwindow.setWindowTitle("Wprowadź informacje")
#         # page.btn_close.clicked.connect(self.subwindowclose)
#         # page.btn_new.clicked.connect(self.countrypage)
#         subwindow.show()
#         self.mdi.tileSubWindows()
 
# app = QApplication(sys.argv)
# MainWindow = MainWindow()
# app.exec_()