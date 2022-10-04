from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from org.pyengdrom.engine.widget import OpenGLEngine

class ViewPortWidget(QWidget):
    def __init__(self, args):
        super().__init__()

        self.setLayout(QVBoxLayout())
        self.engine = OpenGLEngine(args.folder)
        self.layout().addWidget(self.engine)
    def keyPressEvent(self, a0) -> None:
        self.engine.keyPressEvent(a0)
    def keyReleaseEvent(self, a0) -> None:
        self.engine.keyReleaseEvent(a0)
    