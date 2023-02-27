import os
import os.path as p

from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QMovie

basedir = os.path.dirname(os.path.dirname(__file__))


class Loader(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(232, 148)
        self.label = QLabel(self)
        self.label.setMinimumSize(QSize(232, 148))
        self.label.setMaximumSize(QSize(232, 148))
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setStyleSheet("QLabel {background-color: #242424}")

        self.movie = QMovie(p.join(basedir, p.normpath("imgs\loader.gif")))
        self.label.setMovie(self.movie)

        self.movie.start()
