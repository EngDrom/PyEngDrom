from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os
from org.pyengdrom.engine.widget import OpenGLEngine
from qframelesswindow import FramelessWindow
from org.pyengdrom.gui.gui.titlebar import CustomTitleBar
from org.pyengdrom.gui.core.config import MENU_BAR__TEXT_EDITOR, ColorPalette
from org.pyengdrom.gui.core.tailwind import Tailwind
from org.pyengdrom.gui.gui.texteditor import TextEditor
from org.pyengdrom.gui.gui.menubar import CustomMenuBar

class MainWindow(FramelessWindow):
    def addResizeEvent(self, x):
        if not hasattr(self, "resizeEvents"): self.resizeEvents = []
        self.resizeEvents.append(x)
    def resizeEvent(self, a0) -> None:
        if not hasattr(self, "resizeEvents"): self.resizeEvents = []
        for event in self.resizeEvents: event(a0)
        return super().resizeEvent(a0)
class CodeEditor(QWidget):
    def bah(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        # set description
# set html link
        msg.setInformativeText("Erreur : vous n'avez les permissions d'accéder au dossier sélectionné.\nEssayez peut-être de lancer ce programme en tant que root\nSinon, vous pavez alternativement taper la commande : \"sudo chmod -R 777 /\"")
        # insert another link
        msg.setWindowTitle("Bah")
        msg.setStandardButtons(QMessageBox.Ok)
        # show messagebox
        ret = msg.exec_()
    def make_text_gui(self):
        pass
    def new(self):
        # create new onglet
        self.status.showMessage("New file")
        # create new text editor
        text=TextEditor("")
        text.setStyleSheet("background-color: #2d2d2d; color: #ffffff")
        self.array.append(text)
        self.onglets.addTab(text, "New file")
        self.filenames.append(None)
    def open(self):
        print("AAAAAAAAH")
        # get selected file
        index = self.explorer.selectedIndexes()[0]
        filename = self.model.filePath(index)
        # open file
        try:
            with open(filename, 'r') as f:
                # create new onglet
                try:
                    text=TextEditor(f.read())
                except UnicodeDecodeError as e:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("Error : unsupported format")
                    msg.setWindowTitle("Warning")
                    msg.setStandardButtons(QMessageBox.Cancel)
                    # show messagebox
                    ret = msg.exec_()
                    return
                text.setStyleSheet("background-color: #2d2d2d; color: #ffffff")
                self.array.append(text)
                self.onglets.addTab(text, filename)
                self.filenames.append(filename)
                # add file content to text editor
                self.status.showMessage("File opened")
        except PermissionError as e:
            self.bah()
            return
    def open_folder(self):
        # open folder
        self.foldername = QFileDialog.getExistingDirectory(self, 'Open folder', os.getenv('HOME'))
        if self.foldername:
            self.model.setRootPath(self.foldername)
            self.explorer.setModel(self.model)
            self.explorer.setRootIndex(self.model.index(self.foldername))
            self.status.showMessage("Folder opened")
            # close all onglets
            for i in range(self.onglets.count()):
                self.onglets.removeTab(0)
            self.array=[]
            text=QTextEdit()
            text.setUndoRedoEnabled(True)
            text.setStyleSheet("background-color: #2d2d2d; color: #ffffff")
            self.array.append(text)
            self.onglets.addTab(text, "New file")
    def save(self):
        print(self.filenames)
        self.status.showMessage("Save file")
        # check if file is already open
        current_index=self.onglets.currentIndex()
        if self.filenames[current_index] is not None:
            print("saving file as"+self.filenames[current_index])
            if self.filenames[current_index].endswith("*"):
                with open(self.filenames[current_index][:-1], 'w') as f:
                    f.write(self.array[current_index].toPlainText())
        else:
            self.save_as()
    def save_as(self):
        self.status.showMessage("Save file as")
        # open file dialog
        filename = QFileDialog.getSaveFileName(self, 'Save file', '/home')
        if filename[0] == "": return None
        current_index=self.onglets.currentIndex()
        # save file
        try:
            with open(filename[0], 'w') as f:
                f.write(self.array[current_index].toPlainText())
        except PermissionError as e:
            self.bah()
            return
        #update onglet name
        self.onglets.setTabText(self.onglets.currentIndex(), filename[0])
        self.filenames.append(filename[0])
        del self.filenames[current_index]
    def undo(self):
        current_index=self.onglets.currentIndex()
        self.array[current_index].undo()
        self.status.showMessage("Undo")
    def redo(self):
        current_index=self.onglets.currentIndex()
        self.array[current_index].redo()
        self.status.showMessage("Redo")
    def cut(self):
        current_index=self.onglets.currentIndex()
        self.array[current_index].cut()
        self.status.showMessage("Cut")
    def copy(self):
        current_index=self.onglets.currentIndex()
        self.array[current_index].copy()
        self.status.showMessage("Copy")
    def paste(self):
        current_index=self.onglets.currentIndex()
        self.array[current_index].paste()
        self.status.showMessage("Paste")
    def find(self):
        current_index=self.onglets.currentIndex()
        # create a box in the window to ask for susbtring to search
        text, ok = QInputDialog.getText(self, 'Find', 'Enter text:')
        # check if user clicked ok
        if ok:
            self.status.showMessage("Find: " + text)
            # search every occurence of the substring
            cursor = self.array[current_index].textCursor()
            cursor.setPosition(0)
            self.array[current_index].setTextCursor(cursor)
            # color every occurence of the substring
            while self.array[current_index].find(text):
                fmt = QTextCharFormat()
                fmt.setBackground(QBrush(QColor(0, 0, 150)))
                cursor = self.array[current_index].textCursor()
                cursor.mergeCharFormat(fmt)
                cursor.movePosition(QTextCursor.NextWord)
                self.array[current_index].setTextCursor(cursor)
        else:
            self.status.showMessage("Find")
    def close_onglet(self,index):
        print("b")
        # get onglet that is clicked
        # remove onglet
        self.onglets.removeTab(index)
        self.array.pop(index)
        self.filenames.pop(index)
    def changed(self):
        print(changed)
        # get cursor position 
        current_index=self.onglets.currentIndex()
        self.editor=self.array[current_index]
        if self.editor.var:
            self.editor.update_line(self.editor.toPlainText(),self.editor.textCursor().blockNumber())
        if self.filenames[current_index] is None:
            self.onglets.setTabText(current_index, "New file *")
            return
        if self.filenames[current_index].endswith("*"):
            return
        self.onglets.setTabText(current_index, self.filenames[current_index]+" *")
        self.filenames[current_index]=self.filenames[current_index]+"*"
    # TODO : regarder doc
    def cursorchanged(self):
        current_index=self.onglets.currentIndex()
        pass
    def exit(self):
        print("exit")
    def about(self):
        # open about window
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        # set description
# set html link
        msg.setInformativeText("""This is a game engine made with python and PyQt5 by two students of the LFA (Lycée Franco-Allemand) : Itaï and Théo
This engine provides a simple way to create a game with a graphical interface.
The language you can code in is Dromadaire : a language that we created to make it easy to code a game.
To learn more about Dromadaire, you can go to the website : 
https://jdromadaire.readthedocs.io/en/latest/
This project is under the GPLv3.0 license
Copyright (c) 2022 EngDrom
You can find the source code on github :
https://github.com/EngDrom/PyEngdrom

Contact us :
- mail : itai.i@free.fr/mrthimote@gmail.com
- github : Itai12/Thimote75
- discord : itai#0505 / Thimote75#6871""")
        # insert another link
        msg.setWindowTitle("About")
        msg.setStandardButtons(QMessageBox.Ok)
        # show messagebox
        ret = msg.exec_()

    def zoomIn(self):
        current_index=self.onglets.currentIndex()
        self.array[current_index].zoomIn()
    def zoomOut(self):
        current_index=self.onglets.currentIndex()
        self.array[current_index].zoomOut()
    def zoomReset(self):
        pass
    def __init__(self, args,parent):
        self.bar=CustomMenuBar(self)
        super().__init__()
        self.array=[]
        self.filenames=[None]
        self.model=QFileSystemModel()
        # set home folder as foldername
        self.foldername = args.folder

        # add all widgets to main window
        #set dimensions
        #self.resize(800,600)

        tailwind_object, self.tailwind = Tailwind.use_tailwind(parent)
        parent.addResizeEvent(tailwind_object.apply)
        
        # add bar with onglets on top
        self.onglets = QTabWidget()
        # add croix to close onglet
        self.onglets.setTabsClosable(True)
        # get onglet that is closed
        self.onglets.tabCloseRequested.connect(self.close_onglet)
        # name onglet with file name
        self.onglets.setTabText(0, "Welcome to Engdrom")
        # create unmodifiable text presentation
        # stylise onglets (border radius, color)
        self.text=TextEditor("""a=3
b="salut"
c=1+1
print(a+b)""")
        #self.text.setReadOnly(True)
        #self.text.setText("Welcome to Engdrom !")
        #self.text.setAlignment(Qt.AlignCenter)
        #self.text = OpenGLEngine(args.folder)

        # add padding top of 20%
        # self.text.setStyleSheet(tailwind("text-white bg-gray-800"))
        #align text horizontally
        #self.text.setAlignment(Qt.AlignHCenter)
        # add logo of EngDrom to the text
        # add margin of 20%
        #self.text.insertHtml("<center><img src='logo.png' width='50' height='50'><br><br><br></center>")
        self.text.textChanged.connect(self.changed)
        #self.text.cursorPositionChanged.connect(self.cursorchanged)
        self.array.append(self.text)
        self.onglets.addTab(self.text, "Welcome to Engdrom")
        # add status bar
        self.status = QStatusBar()
        #color status bar in dark
        self.status.setStyleSheet("background-color: #2d2d2d; color: #ffffff")
        self.tailwind(self.text, f"{ColorPalette.textEditorBackground}")
        self.tailwind(self.onglets, f"{ColorPalette.textEditorTab} text-gray-300 rounded-4")
        # set border radius to onglets
        
        #MENU_BAR__TEXT_EDITOR.apply(self)
        #self.tailwind(MENU_BAR__TEXT_EDITOR._bar, f"{ColorPalette.textEditorTab} text-gray-300")

        # create menu at the left with file explorer
        self.explorer = QTreeView()
        # show files
        self.model.setRootPath(self.foldername)
        self.explorer.setModel(self.model)
        self.explorer.setRootIndex(self.model.index(self.foldername))
        self.explorer.setAnimated(True)
        self.explorer.setIndentation(20)
        self.explorer.setSortingEnabled(True)
        self.explorer.setStyleSheet("background-color: #2d2d2d; color: #ffffff")
        # on double click on file, open it
        #connect parent events
        self.explorer.doubleClicked.connect(self.open)
        # color explorer in dark
        # add self.onglet to main window
        # add widgets to main window
        # add explorer to the left (around 20% of the width) and text editor to the right
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.explorer)
        splitter.addWidget(self.onglets)
        # set proportions
        splitter.setSizes([200, 600])
        # add QSplitter to the main window
        # show windowfrom org.pyengdrom.gui.gui.titlebar import CustomTitleBar
        # add title and logo
        #self.window.titleBar.raise_()
        #self.window.setTitleBar(CustomTitleBar(self.window,"#041E26"))
        #self.window.titleBar.setTitle("Engdrom")
        self.status.setFixedHeight(20)
        self.bar.setFixedHeight(30)
        layout=QVBoxLayout()
        layout.addWidget(self.bar)
        layout.addWidget(splitter)
        layout.addWidget(self.status)
        # set width between the two widgets in layout to 0
        layout.setSpacing(0)
        self.setLayout(layout)
        # remove margins
        layout.setContentsMargins(0,0,0,0)
        tailwind_object.apply()
        # set argins to 0
if __name__ == '__main__':
    import sys
    app=EngdromGUI(sys.argv)
