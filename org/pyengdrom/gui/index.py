from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from org.pyengdrom.gui.gui.codeeditor import CodeEditor
from org.pyengdrom.gui.gui.viewport import ViewPortWidget
from qframelesswindow import FramelessWindow
from org.pyengdrom.gui.gui.titlebar import CustomTitleBar
from org.pyengdrom.gui.gui.menubar import CustomMenuBar
class WidgetManager(QWidget):
    def __init__(self,args,parent):
        super().__init__()
        self.editor=CodeEditor(args,parent)
        self.viewport=ViewPortWidget(args.folder)
        self.tab=QTabWidget()
        # set editor margin to 0
        self.editor.setContentsMargins(0,0,0,0)
        self.tab.addTab(self.editor,"Editor")
        self.tab.addTab(self.viewport,"Viewport")
        # set margin to 0 into tab
        self.tab.setContentsMargins(0,0,0,0)
        # set margin to 0 into viewport
        self.tab.setTabPosition(QTabWidget.West)
        self.tab.setTabShape(QTabWidget.Rounded)
        self.tab.setMovable(True)
        self.tab.setTabsClosable(False)
        # make onglets unmovable
        self.tab.tabBar().setMovable(False)
        # set height of each onglet
        self.tab.tabBar().setStyleSheet("QTabBar::tab { height: 200px; width: 30px; }")
        self.tab.setStyleSheet("QTabWidget::pane { border: 0; }");
        # remove all margins
        self.tab.setContentsMargins(0,0,0,0)

class MainWindow(FramelessWindow):
    def __init__(self,args):
        super().__init__()
        self.widget=WidgetManager(args,self).tab
        self.setTitleBar(CustomTitleBar(self, "#041E26"))
        layout=QHBoxLayout()
        layout.addWidget(self.widget)
        layout.setContentsMargins(0, self.titleBar.SIZE , 0, 0)
        # remove spacing between widgets
        layout.setSpacing(0)
        self.setLayout(layout)
        self.show()
    def addResizeEvent(self, x):
        if not hasattr(self, "resizeEvents"): self.resizeEvents = []
        self.resizeEvents.append(x)
    def resizeEvent(self, a0) -> None:
        if not hasattr(self, "resizeEvents"): self.resizeEvents = []
        for event in self.resizeEvents: event(a0)
        return super().resizeEvent(a0)

class WidgetManagerLauncher:
    def __init__(self,args):
        self.app = QApplication(["PyEngDrom"])
        self.window = MainWindow(args)
        self.window.show()
        # add icon
        self.window.setWindowIcon(QIcon("./assets/editor/icon.png"))
        self.app.exec_()