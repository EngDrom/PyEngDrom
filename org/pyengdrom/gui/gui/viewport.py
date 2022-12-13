from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from org.pyengdrom.engine.widget import OpenGLEngine
from org.pyengdrom.editor.base import EditorMode
import os

class Explorer(QListView):
    def __init__(self,path=None):
        super().__init__()
        self.path = path
        if self.path is None:
            # set path to home directory
            self.path = os.path.expanduser("~")
        # set margin top to 20px
        self.setStyleSheet("background-color: #000000; color: #ffffff;")
        # set file explorer with icons
        self.setUniformItemSizes(True)
        self.setViewMode(QListView.IconMode)
        self.setIconSize(QSize(64,64))
        self.setGridSize(QSize(84,84))
        self.setMovement(QListView.Static)
        self.setResizeMode(QListView.Adjust)
        # set path for file explorer
        self.setPath(self.path)
        # onclick on folder open it
        self.clicked.connect(self.openFolder)
        # create a red square
    def setPath(self,path):
        self.path = path
        self.model = QStandardItemModel()
        # set icons for directories and files
        # sort files and directories
        dirs = []
        files = []
        # create back button
        back = QStandardItem("Back")
        back.setIcon(QIcon("./assets/editor/back2.png"))
        self.model.appendRow(back)
        for item in os.listdir(self.path):
            if os.path.isdir(os.path.join(self.path,item)):
                dirs.append(item)
            else:
                files.append(item)
        for item in dirs:
            self.model.appendRow(QStandardItem(QIcon("./assets/editor/folder.png"),item))
        for item in files:
            # check extension
            ext = os.path.splitext(item)[1]
            if ext == ".py":
                self.model.appendRow(QStandardItem(QIcon("./assets/editor/python.png"),item))
            elif ext in [".jpg",".png",".jpeg",".gif"]:
                self.model.appendRow(QStandardItem(QIcon("./assets/editor/image.png"),item))
            elif ext in [".mp3",".wav",".ogg",".mp2",".mp1"]:
                self.model.appendRow(QStandardItem(QIcon("./assets/editor/music.png"),item))
            elif ext in [".mp4",".avi",".mkv"]:
                self.model.appendRow(QStandardItem(QIcon("./assets/editor/video.png"),item))
            elif ext in [".zip",".rar",".7z",".tar.gz",".tar.xz"]:
                self.model.appendRow(QStandardItem(QIcon("./assets/editor/archive.png"),item))
            elif ext in [".pdf",".doc",".docx",".odt",".rtf"]:
                self.model.appendRow(QStandardItem(QIcon("./assets/editor/document.png"),item))
            else:
                self.model.appendRow(QStandardItem(QIcon("./assets/editor/file.png"),item))
        self.setModel(self.model)
    def openFolder(self,index):
        # get path of item
        item = self.model.itemFromIndex(index)
        path = os.path.join(self.path,item.text())
        if os.path.isdir(path):
            self.setPath(path)
        # elif it's back
        elif item.text() == "Back":
            self.goBack()
        else:
            print("open file",path)
    def goBack(self):
        # get parent directory
        path = os.path.dirname(self.path)
        self.setPath(path)

class ChildList(QListView):
    def __init__(self,content):
        super().__init__()
        self.model = QStandardItemModel()
        for item in content:
           self.model.appendRow(QStandardItem(item))
        self.setModel(self.model)
        # set background color
        self.setStyleSheet("background-color: #000000; color: #ffffff;")

class ViewPortWidget(QSplitter):
    def recompile(self):
        # delete self.engine
        self.engine.deleteLater()
        # create new engine
        self.engine = OpenGLEngine(self.path)
        # add engine to hspliter
        self.hsplitter.addWidget(self.engine)
    def __init__(self,path):
        self.path = path
        super().__init__(Qt.Horizontal)
        # create a Ui_Form object
        # create horizontal layout
        self.vsplitter=QSplitter(Qt.Vertical)
        # create file explorer
        # get full path of project
        self.path=os.path.abspath(self.path)
        self.explorer=Explorer(self.path)
        # create vertical layout
        self.hsplitter=QSplitter(Qt.Horizontal)
        # create viewport
        self.engine=OpenGLEngine(self.path)
        # create child list
        self.childlist=ChildList(["Test","Test"])
        self.listing=EditorMode()
        # add widgets to hspliter
        self.hsplitter.addWidget(self.childlist)
        self.hsplitter.addWidget(self.engine)
        self.hsplitter.setCollapsible(1,False)
        # set proportions to 30%/70%
        self.hsplitter.setSizes([300,700])
        # add hspliter to vspliter
        self.vsplitter.addWidget(self.hsplitter)
        self.vsplitter.addWidget(self.explorer)
        # prohib explorer to be removed
        self.vsplitter.setCollapsible(0,False)
        # set propotions to 70%/30%
        self.vsplitter.setSizes([700,300])
        # add vspliter to splitter
        self.addWidget(self.vsplitter)
        self.addWidget(self.listing)
        self.setCollapsible(0,False)
        # set proportions to 70% / 30%
        self.setSizes([700,300])
    def eventFilter(self, a0: 'QObject', a1: 'QEvent') -> bool:
        if a1.type() == a1.Type.KeyPress: return self.keyPressEvent(a1)
        if a1.type() == a1.Type.KeyRelease: return self.keyReleaseEvent(a1)
        return super().eventFilter(a0, a1)
    def keyPressEvent(self, a0) -> None:
        return self.engine.keyPressEvent(a0)
    def keyReleaseEvent(self, a0) -> None:
        return self.engine.keyReleaseEvent(a0)
