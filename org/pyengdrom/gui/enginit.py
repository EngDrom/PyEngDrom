'''
EngDrom Initializer window, used to create and load projects
'''

from typing import List, Tuple
from qframelesswindow import FramelessWindow
from PyQt5.QtWidgets import QApplication, QSplitter, QVBoxLayout, QWidget, QLabel, QPushButton, QLineEdit, QFileDialog
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QPixmap, QPainter, QBitmap, QIcon
from org.pyengdrom.config.const import QT_REBOOT
from org.pyengdrom.engine.utils.project import create_project
from org.pyengdrom.gui.core.tailwind import Tailwind
import os
from org.pyengdrom.gui.gui.titlebar import CustomTitleBar

class OpenProject(QWidget):
    def create_project(self,path):
        # get name
        with open(path+"/.project") as f:
            content=f.read()
        l=content.split("\n")
        for i in l:
            if i.startswith("name"):
                name=i.split("=")[1]
        create_project(None, name, path)
        EngDromInitializer.args.folder = path

        QApplication.exit(QT_REBOOT)
    def open_project(self):
        file_dialog=QFileDialog()
        file_dialog.setFileMode(QFileDialog.Directory)
        # get the path
        path=file_dialog.getExistingDirectory()
        if path:
            # create the project
            self.create_project(path)
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background:#000000")
        self.layout=QVBoxLayout()
        # create image widget
        self.image=QLabel()
        self.image.setPixmap(QPixmap("assets/editor/folder.png"))
        # center the image
        self.image.setAlignment(Qt.AlignCenter)
        # set size
        self.button=QPushButton("Open Project")
        self.button.setStyleSheet("background:#000000;color:#ffffff")
        self.button.clicked.connect(self.open_project)
        # create widget with a central button
        self.central=QWidget()
        self.central.setStyleSheet("background:#000000")
        self.central_layout=QVBoxLayout()
        self.central_layout.setContentsMargins(0,0,0,0)
        self.central.setLayout(self.central_layout)
        self.central_layout.addStretch()
        self.central_layout.addWidget(self.button)
        self.central_layout.addStretch()
        self.layout.addWidget(self.image)
        self.layout.addWidget(self.central)
        # set proportions
        self.layout.setStretch(0,1)
        self.layout.setStretch(1,1)
        self.setLayout(self.layout)

class ProjectImage(QWidget):
    WIDTH  = 550
    HEIGHT = 450

    def __init__(self, image, *args, **kwargs):
        super().__init__(*args, **kwargs)

        __layout = QVBoxLayout()
        #mask = QBitmap(self.WIDTH, self.HEIGHT)
        #mask.fill(Qt.color0)

        #painter = QPainter( mask )
        #painter.setBrush(Qt.color1)
        #painter.drawRoundedRect( 0, 0, self.WIDTH, self.HEIGHT, 30, 30 )

        label = QLabel()
        image = QPixmap(image)
        #image.setMask(mask)
        #print(image)
        label.setPixmap(image)
        __layout.addWidget(label)

        #del painter

        #self.setFixedWidth (self.WIDTH)
        #self.setFixedHeight(self.HEIGHT)
        self.setStyleSheet("border-radius: 30px;")

        self.setLayout(__layout)

class _NewProjectWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.tw, self.tw_object = Tailwind.useGlobalTailwind()
        self.setupUI()
    def buttonclicked(self):
        self.foldername = QFileDialog.getExistingDirectory(self, 'Open folder', os.getenv('HOME'))
        if self.foldername:
            self.path_line_edit.setText(self.foldername)
    def setupUI(self):
        self.__layout = QVBoxLayout()
        self.__layout.setAlignment(Qt.AlignCenter)
        self.__layout.setSpacing(15)
        self.__layout.setContentsMargins(100, 100, 100, 100)
        self.setLayout(self.__layout)
        self.__layout.addWidget(ProjectImage("./assets/templates/2d_template.png"))
        self.name_line_edit = QLineEdit()
        self.name_line_edit.setPlaceholderText("Nom du projet")
        self.name_line_edit.setFixedWidth(550)
        self.tw(self.name_line_edit, "text-gray-300 bg-theme-700 p-4 rounded-4 hover:bg-theme-600 focus:bg-theme-500")
        self.path_line_edit = QPushButton("Chemin du projet")
        #self.path_line_edit.setPlaceholderText("Chemin du projet")
        self.path_line_edit.setFixedWidth(550)
        self.path_line_edit.clicked.connect(self.buttonclicked)
        self.tw(self.path_line_edit, "text-gray-300 bg-theme-700 hover:bg-theme-500 rounded-4 p-4")
        #self.tw(self.path_line_edit, "text-gray-300 bg-theme-700 p-4 rounded-4 hover:bg-theme-600 focus:bg-theme-500")
        self.__layout.addWidget(self.name_line_edit)
        self.__layout.addWidget(self.path_line_edit)

        self.button = QPushButton("Créer le projet")
        self.tw(self.button, "text-gray-200 bg-theme-700 hover:bg-theme-500 rounded-4 p-4")
        self.button.setFixedWidth(550)
        self.button.clicked.connect(self.createProjectClick)
        self.__layout.addWidget(self.button)
    
    def get_template(self):
        return None
    def get_project_name(self):
        return self.name_line_edit.text()
    def get_project_path(self):
        return self.path_line_edit.text()

    def createProjectClick(self):
        a, b, c = self.get_template(), self.get_project_name(), self.get_project_path()
        if b.strip() == "": return None
        if c.strip() in ["","Chemin du projet"]: return None

        self.createProject(a, b, c)

    def createProject(self, template, pname, path):
        create_project(template, pname, path)
        EngDromInitializer.args.folder = path

        QApplication.exit(QT_REBOOT)
        
class NewProjectWidget(QSplitter):
    def __init__(self) -> None:
        super().__init__()

        self.addWidget(_NewProjectWidget())
        self.tw, self.tw_object = Tailwind.useGlobalTailwind()
        self.tw(self, "QSplitter@bg-theme-800")

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
        self.X, self.Y = NewProjectWidget(), OpenProject()
        self.Z = SubWidgetPicker([(self.X, "Nouveau projet"), (self.Y, "Ouvrir un projet")], 0, self)
        #self.Z.setStyleSheet("background: #041E26;")
        #self.Z.setParent(self)
        #self.addWidget(self.Z)
        self.addWidget(self.Z)
        self.setCollapsible(0, False)
        #self.setCollapsible(1, False)
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
    args = None
    def __init__(self, args):
        EngDromInitializer.args = args
        app = QApplication(["Engdrom Launcher"])
        widget = EngDromIW()
        widget.show()
        # set icon
        app.setWindowIcon(QIcon("assets/editor/icon.png"))
        self.err_code = app.exec()
