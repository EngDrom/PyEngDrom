from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from org.pyengdrom.gui.gui.codeeditor import CodeEditor
from org.pyengdrom.gui.gui.viewport import ViewPortWidget
class WidgetManager(QWidget):
    def __init__(self,args):
        super().__init__()
        self.editor=CodeEditor(args).window
        self.viewport=ViewPortWidget()
        self.tab=QTabWidget()
        self.tab.addTab(self.editor,"Editor")
        self.tab.addTab(self.viewport,"Viewport")
        self.tab.setTabPosition(QTabWidget.West)
        self.tab.setTabShape(QTabWidget.Rounded)
        self.tab.setMovable(True)
        self.tab.setTabsClosable(False)


class WidgetManagerLauncher:
    def __init__(self,args):
        self.app = QApplication([])
        self.window = WidgetManager(args).tab
        self.window.show()
        self.app.exec_()