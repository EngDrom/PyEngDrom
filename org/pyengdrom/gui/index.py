from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from org.pyengdrom.gui.gui.codeeditor import CodeEditor
from org.pyengdrom.gui.gui.viewport import ViewPortWidget
class WidgetManager(QTabWidget):
    def __init__(self,args):
        super().__init__()
        self.editor=CodeEditor(args).window
        self.viewport=ViewPortWidget(args)
        self.addTab(self.editor,"Editor")
        self.addTab(self.viewport,"Viewport")
        self.setTabPosition(QTabWidget.West)
        self.setTabShape(QTabWidget.Rounded)
        self.setMovable(True)
        self.setTabsClosable(False)
    
    def eventFilter(self, a0: 'QObject', a1: 'QEvent') -> bool:
        if a1.type() == a1.Type.KeyPress: return self.keyPressEvent(a1)
        if a1.type() == a1.Type.KeyRelease: return self.keyReleaseEvent(a1)
        return super().eventFilter(a0, a1)
    def keyPressEvent(self, a0) -> None:
        self.currentWidget().keyPressEvent(a0)
    def keyReleaseEvent(self, a0) -> None:
        self.currentWidget().keyReleaseEvent(a0)

class WidgetManagerLauncher:
    def __init__(self,args):
        self.app = QApplication([])
        #manager  = WidgetManager(args)
        self.window = ViewPortWidget(args)
        self.window.show()
        self.app.exec_()