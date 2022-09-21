'''
EngDrom Initializer window, used to create and load projects
'''

from typing import List, Tuple
from qframelesswindow import FramelessWindow
from PyQt5.QtWidgets import QApplication, QSplitter, QVBoxLayout, QWidget, QLabel, QPushButton
from PyQt5.QtCore import QRect, Qt
from org.pyengdrom.gui.core.tailwind import Tailwind

from org.pyengdrom.gui.gui.titlebar import CustomTitleBar

class SubWidgetButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.tw, self.tw_object = Tailwind.useGlobalTailwind()
        self.setupUI()
    def setupUI(self):
        self.tw(self, "bg-theme-800 text-white text-[18px] text-left text-gray-200 h-[72px] border-none hover:bg-theme-700 pl-[15px] pr-[15px]")
    def disable(self): self.setupUI()
    def activate(self):
        self.tw(self, "bg-theme-700 text-white text-[18px] text-left text-gray-200 h-[72px] border-none pl-[15px] pr-[15px]")
    def make_click(self, f, i):
        def wrapper():
            f(i)
        return wrapper

class SubWidgetButtonContainer(QWidget):
    def __init__(self, buttons, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__buttons = buttons
        self.__layout  = QVBoxLayout()
        self.__layout.setSpacing(5)
        self.__layout.setContentsMargins(0, 0, 0, 0)
        self.__layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.__layout)

        for __button in self.__buttons: self.__layout.addWidget(__button)

class SubWidgetPicker(QWidget):
    MIN_SIZE = 180

    def __init__(self, choices: List[Tuple[QWidget, str]], default: int, spl: QSplitter):
        super().__init__()
        assert 0 <= default < len(choices)
        self.__parent  = spl
        
        self.choices = choices
        self.false_w = QWidget()

        self.setupUI()
    def setupUI(self):
        self.setStyleSheet("QWidget { background: #041E26; }")
        self.__layout = QVBoxLayout()
        self.__layout.setSpacing(10)
        self.__layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.__layout)
        self.__buttons = [SubWidgetButton(x[1]) for x in self.choices]
        for __idx, __button in enumerate(self.__buttons):
            __button.clicked.connect(__button.make_click(self.set_current, __idx))

        self.innerWidget = SubWidgetButtonContainer(self.__buttons)
        self.__layout.addWidget(self.innerWidget)
    def set_current(self, val : int):
        assert 0 <= val < len(self.choices)
        __size = self.__parent.sizes()

        if hasattr(self, "current"): 
            self.__buttons[self.current].disable()
            self.__remove(self.current)

        self.__buttons[val].activate()
        self.__parent.addWidget(self.choices[val][0])
        self.current = val

        self.__parent.setSizes(__size)
    def __remove(self, current: int):
        self.choices[current][0].setParent(self.false_w)
    def resizeEvent(self, *args) -> None:
        return super().resizeEvent(*args)

class EngDromIWidget(QSplitter):
    def __init__(self):
        super().__init__(Qt.Horizontal)
        self.setStyleSheet('''
        QSplitter::handle {
            background: #03191E;   
        }''')
        self.X, self.Y = QWidget(), QWidget()
        self.X.setStyleSheet("background: #041E26;")
        self.Y.setStyleSheet("background: #041E26;")
        self.Z = SubWidgetPicker([(self.X, "Nouveau projet"), (self.Y, "Ouvrir un projet")], 0, self)
        #self.Z.setStyleSheet("background: #041E26;")
        #self.Z.setParent(self)
        #self.addWidget(self.Z)
        self.addWidget(self.Z)
        self.setCollapsible(0, False)
        self.Z.set_current(0)

        self.setSizes([300, 500])

class EngDromIW(FramelessWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setStyleSheet("background-color: #03191E;")
        self.setTitleBar(CustomTitleBar(self, "#041E26"))
        self.titleBar.raise_()
        self.titleBar.setTitle("EngDrom - Lanceur de projets")

        self.layout = QVBoxLayout()
        self.widget = EngDromIWidget()
        self.layout.addWidget(self.widget)
        self.layout.setContentsMargins(0, self.titleBar.SIZE + 5, 0, 0)
        self.setLayout(self.layout)
    def resizeEvent(self, e):
        l, t = 0, self.titleBar.SIZE + 5
        self.widget.setGeometry(
            QRect(l, t, self.width(), self.height() - t)
        )

        return super().resizeEvent(e)

class EngDromInitializer:
    def __init__(self, args):
        app = QApplication([])

        widget = EngDromIW()
        widget.show()

        app.exec()
