from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class EditorMode(QWidget):
    def __init__(self):
        super().__init__()
    def startPaintGL (self, engine):
        pass
    def endPaintGL(self, engine):
        pass
    def mouseClick(self, engine, button, x, y):
        pass
    def save (self, engine):
        pass
    def restartGL(self, engine):
        #self.deleteLater()
        pass