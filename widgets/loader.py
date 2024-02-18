import os.path as p

from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QMovie

from config.paths import PATHS


class Loader(QLabel):
    def __init__(self):
        super().__init__()
        self.movie = QMovie(p.join(PATHS.BASEDIR, p.normpath(PATHS.STYLE.LOADER)))

        self.resize(232, 148)
        self.setMinimumSize(QSize(232, 148))
        self.setMaximumSize(QSize(232, 148))

        self.setMovie(self.movie)

        self.movie.start()
