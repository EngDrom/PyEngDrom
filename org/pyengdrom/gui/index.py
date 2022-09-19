from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os
from org.pyengdrom.engine.widget import OpenGLEngine

from org.pyengdrom.gui.core.config import MENU_BAR__TEXT_EDITOR, ColorPalette
from org.pyengdrom.gui.core.tailwind import Tailwind

class MainWindow(QMainWindow):
    def addResizeEvent(self, x):
        if not hasattr(self, "resizeEvents"): self.resizeEvents = []
        self.resizeEvents.append(x)
    def resizeEvent(self, a0) -> None:
        if not hasattr(self, "resizeEvents"): self.resizeEvents = []
        for event in self.resizeEvents: event(a0)
class EngdromGUI:
    def make_text_gui(self):
        pass

    def __init__(self, args):
        self.array=[]
        self.filenames=[None]
        self.model=QFileSystemModel()
        # set home folder as foldername
        self.foldername = args.folder
        self.app = QApplication([])

        # add all widgets to main window
        self.window = MainWindow()
        #set dimensions
        self.window.resize(800,600)

        tailwind_object, self.tailwind = Tailwind.use_tailwind(self.window)
        self.window.addResizeEvent(tailwind_object.apply)
        
        # add bar with onglets on top
        self.onglets = QTabWidget()
        # add croix to close onglet
        self.onglets.setTabsClosable(True)
        # get onglet that is closed
        self.onglets.tabCloseRequested.connect(self.close_onglet)
        # name onglet with file name
        self.onglets.setTabText(0, "Welcome to Engdrom")
        # create unmodifiable text presentation

        self.text=QTextEdit()
        self.text.setReadOnly(True)
        self.text.setText("Welcome to Engdrom !")
        self.text.setAlignment(Qt.AlignCenter)
        #self.text = OpenGLEngine(args.folder)

        # add padding top of 20%
        # self.text.setStyleSheet(tailwind("text-white bg-gray-800"))
        #align text horizontally
        #self.text.setAlignment(Qt.AlignHCenter)
        # add logo of EngDrom to the text
        # add margin of 20%
        self.text.insertHtml("<center><img src='logo.png' width='50' height='50'><br><br><br></center>")
        self.text.textChanged.connect(self.textchanged)
        self.text.cursorPositionChanged.connect(self.cursorchanged)
        self.array.append(self.text)
        self.onglets.addTab(self.text, "Welcome to Engdrom")
        # add status bar
        self.status = QStatusBar()
        #color status bar in dark
        self.status.setStyleSheet("background-color: #2d2d2d; color: #ffffff")
        self.tailwind(self.text, f"pt-[30vh] {ColorPalette.textEditorBackground}")
        self.tailwind(self.onglets, f"{ColorPalette.textEditorTab} text-gray-300")

        MENU_BAR__TEXT_EDITOR.apply(self)
        self.tailwind(MENU_BAR__TEXT_EDITOR._bar, f"{ColorPalette.textEditorTab} text-gray-300")

        # create menu at the left with file explorer
        self.explorer = QTreeView()
        # show files
        self.model.setRootPath(self.foldername)
        self.explorer.setModel(self.model)
        self.explorer.setRootIndex(self.model.index(self.foldername))
        self.explorer.setAnimated(False)
        self.explorer.setIndentation(20)
        self.explorer.setSortingEnabled(True)
        self.explorer.setStyleSheet("background-color: #2d2d2d; color: #ffffff")
        self.explorer.doubleClicked.connect(self.open)

        # color explorer in dark
        self.explorer.setStyleSheet("background-color: #2d2d2d; color: #ffffff")
        # add self.onglet to main window
        # add widgets to main window
        # add explorer to the left (around 20% of the width) and text editor to the right
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.explorer)
        splitter.addWidget(self.onglets)
        # set proportions
        splitter.setSizes([200, 600])
        # add QSplitter to the main window
        self.window.setCentralWidget(splitter)
        # add self.onglet on top of text editor
        self.window.setStatusBar(self.status)
        # show window
        self.window.show()
        # add title and logo
        self.window.setWindowTitle("Engdrom")
        self.app.exec_()
    def new(self):
        # create new onglet
        self.status.showMessage("New file")
        # create new text editor
        text=QTextEdit()
        text.setUndoRedoEnabled(True)
        text.setStyleSheet("background-color: #2d2d2d; color: #ffffff")
        self.array.append(text)
        self.onglets.addTab(text, "New file")
        self.filenames.append(None)
        self.array[-1].textChanged.connect(self.textchanged)
        self.array[-1].cursorPositionChanged.connect(self.cursorchanged)
    def open(self):
        # get selected file
        index = self.explorer.selectedIndexes()[0]
        filename = self.model.filePath(index)
        # open file
        with open(filename, 'r') as f:
            # create new onglet
            text=QTextEdit()
            text.setUndoRedoEnabled(True)
            text.setStyleSheet("background-color: #2d2d2d; color: #ffffff")
            self.array.append(text)
            self.onglets.addTab(text, filename)
            self.filenames.append(filename)
            # add file content to text editor
            text.setText(f.read())
            self.array[-1].textChanged.connect(self.textchanged)
            self.array[-1].cursorPositionChanged.connect(self.cursorchanged)
            self.status.showMessage("File opened")
    def open_folder(self):
        # open folder
        self.foldername = QFileDialog.getExistingDirectory(self.window, 'Open folder', os.getenv('HOME'))
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
        self.status.showMessage("Save file")
        # check if file is already open
        current_index=self.onglets.currentIndex()
        if self.filenames[current_index] is not None:
            if self.filenames[current_index].endswith("*"):
                with open(self.filenames[current_index][:-1], 'w') as f:
                    f.write(self.array[current_index].toPlainText())
        else:
            self.save_as()
    def save_as(self):
        self.status.showMessage("Save file as")
        # open file dialog
        filename = QFileDialog.getSaveFileName(self.window, 'Save file', '/home')
        if filename[0] == "": return None
        current_index=self.onglets.currentIndex()
        # save file
        with open(filename[0], 'w') as f:
            f.write(self.array[current_index].toPlainText())
        #update onglet name
        self.onglets.setTabText(self.onglets.currentIndex(), filename[0])
        self.filenames.append(filename[0])
    def exit(self):
        # create messagebox
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Do you want to save the file?")
        msg.setWindowTitle("Warning")
        msg.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        # show messagebox
        ret = msg.exec_()
        # check if user wants to save
        if ret == QMessageBox.Save:
            self.save()
            self.app.exit()
        elif ret == QMessageBox.Discard:
            self.app.exit()
        else:
            pass
    # TODO : update with self.array[index]
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
        text, ok = QInputDialog.getText(self.window, 'Find', 'Enter text:')
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
        # get onglet that is clicked
        # remove onglet
        self.onglets.removeTab(index)
        self.array.pop(index)
        self.filenames.pop(index)
    def textchanged(self):
        current_index=self.onglets.currentIndex()
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
if __name__ == '__main__':
    import sys
    app=EngdromGUI(sys.argv)