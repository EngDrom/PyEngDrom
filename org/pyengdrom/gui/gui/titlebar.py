
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from qframelesswindow import FramelessWindow, TitleBar

class IconBasedButton(QPushButton):
    def __init__(self, path, size):
        super().__init__()
        self.setIcon(QIcon(path))
        self.setIconSize(QSize(size, size))
        self.setStyleSheet('''
        QPushButton {
            background-color: transparent;
            border: none;
        }
        QPushButton:hover {
            background-color: #072D3C;
        }
        ''')
    def setMaxState(*args): pass

class CustomTitleBar(TitleBar):
    """ Title bar """
    SIZE = 48

    def setTitle(self, text):
        self.label.setText(text)
    def __init__(self, parent, color="#000000"):
        # Init
        super().__init__(parent)
        self.setFixedHeight(self.SIZE)

        # Replace layout
        QWidget().setLayout(self.hBoxLayout)
        self.hBoxLayout = QVBoxLayout(self)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.maxBtn = IconBasedButton("./assets/custombar/fullscreen.png", self.SIZE)
        self.minBtn = IconBasedButton("./assets/custombar/minimize.png",   self.SIZE)
        self.clsBtn = IconBasedButton("./assets/custombar/close.png",      self.SIZE)

        # Create real title bar widget
        self.realTBar = QWidget(self)
        self.realTBar.setStyleSheet(f"background-color: {color};")
        self.realTBar.setFixedHeight(self.SIZE)
        self.tbarLayout = QHBoxLayout(self.realTBar)
        self.tbarLayout.setSpacing(0)
        self.tbarLayout.setContentsMargins(10, 0, 0, 0)
        self.tbarLayout.setAlignment(Qt.AlignRight)
        self.label = QLabel("Project Manager")
        self.label.setStyleSheet("color: #FFFFFF; font-size: 20px; font-weight: 300;")
        self.label.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.tbarLayout.addWidget(self.label)
        self.tbarLayout.addStretch(1)

        self.realTBar.layout().addWidget(self.minBtn, 0, Qt.AlignRight)
        self.realTBar.layout().addWidget(self.maxBtn, 0, Qt.AlignRight)
        self.realTBar.layout().addWidget(self.clsBtn, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.realTBar)


        self.minBtn.clicked.connect(self.window().showMinimized)
        self.maxBtn.clicked.connect(self._TitleBar__toggleMaxState)
        self.clsBtn.clicked.connect(self.window().close)
