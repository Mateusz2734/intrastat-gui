
from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt
  
  
class Loader(QMainWindow):
    def __init__(self):
        super(Loader, self).__init__()
        self.resize(232, 148)
        self.label = QLabel()
        self.setCentralWidget(self.label)
        self.label.setMinimumSize(QSize(232, 148))
        self.label.setMaximumSize(QSize(232, 148))
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setStyleSheet("QLabel {background-color: #242424}")

        self.movie = QMovie("./imgs/loader.gif")
        self.label.setMovie(self.movie)
  
        self.movie.start()