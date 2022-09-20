'''
EngDrom Initializer window, used to create and load projects
'''

from qframelesswindow import FramelessWindow
from PyQt5.QtWidgets import QApplication

from org.pyengdrom.gui.gui.titlebar import CustomTitleBar

class EngDromIW(FramelessWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitleBar(CustomTitleBar(self, "#041E26"))
        self.titleBar.raise_()

class EngDromInitializer:
    def __init__(self, args):
        app = QApplication([])

        widget = EngDromIW()
        widget.show()

        app.exec()
