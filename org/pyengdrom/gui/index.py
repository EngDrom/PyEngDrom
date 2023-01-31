from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from org.pyengdrom.engine.widget import OpenGLEngine
from org.pyengdrom.gui.gui.codeeditor import CodeEditor
from org.pyengdrom.gui.gui.viewport import ViewPortWidget
from qframelesswindow import FramelessWindow
from org.pyengdrom.gui.gui.titlebar import CustomTitleBar
from org.pyengdrom.gui.gui.menubar import CustomMenuBar


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
        #self.tab.changeEvent.connect(self.change)
        # set height of each onglet
        self.tab.tabBar().setStyleSheet("QTabBar::tab { height: 200px; width: 30px; }")
        self.tab.setStyleSheet("QTabWidget::pane { border: 0; }");
        # remove all margins
        self.tab.setContentsMargins(0,0,0,0)
        
        # create a shortcut for left arrow
        self.left = QShortcut(QKeySequence("Left"),self)
        self.left.activated.connect(self.leftArrow)
        # create a shortcut for right arrow
        self.right = QShortcut(QKeySequence("Right"),self)
        self.right.activated.connect(self.rightArrow)


    def leftArrow(self):
        pass

    def rightArrow(self):
        pass

    def changeEvent(self,a0: 'QEvent'):
        print("salut")
        self.viewport.engine.keys=[False]*4
        return super().changeEvent(a0)

    def eventFilter(self, a0: 'QObject', a1: 'QEvent') -> bool:
        if a1.type() == a1.Type.KeyPress: return self.keyPressEvent(a1)
        if a1.type() == a1.Type.KeyRelease: return self.keyReleaseEvent(a1)
        # if tab changed
        return super().eventFilter(a0, a1)
    def keyPressEvent(self, a0) -> None:
        return self.tab.currentWidget().keyPressEvent(a0)
    def keyReleaseEvent(self, a0) -> None:
        return self.tab.currentWidget().keyReleaseEvent(a0)
class MainWindow(FramelessWindow):
    def __init__(self,args):
        super().__init__()
        self.args=args
        self.widget=WidgetManager(args,self)
        self.setTitleBar(CustomTitleBar(self, "#041E26"))
        layout=QHBoxLayout()
        layout.addWidget(self.widget.tab)
        layout.setContentsMargins(0, self.titleBar.SIZE , 0, 0)
        # remove spacing between widgets
        layout.setSpacing(0)
        # add button on the top absolute position
        self.setLayout(layout)
        # set size
        self.resize(800,600)
        self.show()
    '''def recompile(self):
        self.widget.viewport.recompile()'''
    def addResizeEvent(self, x):
        if not hasattr(self, "resizeEvents"): self.resizeEvents = []
        self.resizeEvents.append(x)
    def resizeEvent(self, a0) -> None:
        if not hasattr(self, "resizeEvents"): self.resizeEvents = []
        for event in self.resizeEvents: event(a0)
        return super().resizeEvent(a0)
    def eventFilter(self, a0: 'QObject', a1: 'QEvent') -> bool:
        if a1.type() == a1.Type.KeyPress:
            self.keyPressEvent(a1)
            if a1.key() in [Qt.Key_Left,Qt.Key_Right,Qt.Key_Down,Qt.Key_Up] and self.widget.tab.currentIndex()==1: return True
            return False
        if a1.type() == a1.Type.KeyRelease: self.keyReleaseEvent(a1); return False
        return super().eventFilter(a0, a1)
    def keyPressEvent(self, a0) -> None:
        return self.widget.keyPressEvent(a0)
    def keyReleaseEvent(self, a0) -> None:
        return self.widget.keyReleaseEvent(a0)

class WidgetManagerLauncher:
    def __init__(self,args):
        print(args)
        self.app = QApplication(["EngDrom"])
        #manager  = WidgetManager(args)
        self.window = MainWindow(args)
        # set dimensions
        self.window.resize(800,600)
        # set name & icon
        self.window.setWindowTitle("PyEngDrom")
        # set app name
        self.app.setApplicationName("PyEngDrom")
        self.window.setWindowIcon(QIcon("assets/editor/icon.png"))

        self.window.show()
        # set app name
        self.app.setApplicationName("PyEngDrom")
        # set window name
        self.app.setWindowIcon(QIcon("assets/editor/icon.png"))
        self.app.exec_()