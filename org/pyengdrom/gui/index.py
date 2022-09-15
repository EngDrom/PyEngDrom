from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os
class EngdromGUI:
    def __init__(self,argv):
        self.array=[]
        self.model=QFileSystemModel()
        # set home folder as foldername
        self.foldername = os.getenv('HOME')
        self.app = QApplication([])
        # add bar menu with actions on click
        self.bar = QMenuBar()
        file = self.bar.addMenu("File")
        fnew=file.addAction("New")
        fopen=file.addAction("Open Folder")
        fsave=file.addAction("Save")
        fsave_as=file.addAction("Save As")
        fexit=file.addAction("Exit")
        #link actions
        fnew.triggered.connect(self.new)
        fopen.triggered.connect(self.open_folder)
        fsave.triggered.connect(self.save)
        fsave_as.triggered.connect(self.save_as)
        fexit.triggered.connect(self.exit)
        edit=self.bar.addMenu("Edit")
        fundo=edit.addAction("Undo")
        fredo=edit.addAction("Redo")
        fcut=edit.addAction("Cut")
        fcopy=edit.addAction("Copy")
        fpaste=edit.addAction("Paste")
        ffind=edit.addAction("Find")
        # add text editor
        fundo.triggered.connect(self.undo)
        fredo.triggered.connect(self.redo)
        fcut.triggered.connect(self.cut)
        fcopy.triggered.connect(self.copy)
        fpaste.triggered.connect(self.paste)
        ffind.triggered.connect(self.find)
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
        self.text.setStyleSheet("background-color: #2d2d2d; color: #ffffff")
        self.text.setText("Welcome to Engdrom !")
        #align to the center (horizontal and vertical) text
        self.text.setAlignment(Qt.AlignCenter)
        # add padding top of 20%
        self.text.setStyleSheet(f"padding-top: {int(0.3*self.text.height())}px")
        #align text horizontally
        self.text.setAlignment(Qt.AlignHCenter)
        # add logo of EngDrom to the text
        # add margin of 20%
        self.text.insertHtml("<center><img src='logo.png' width='50' height='50'><br><br><br></center>")
        self.array.append(self.text)
        self.onglets.addTab(self.text, "Welcome to Engdrom")
        # color onglets in dark
        self.onglets.setStyleSheet("background-color: #2d2d2d; color: #ffffff")
        #color bar in dark
        self.bar.setStyleSheet("background-color: #2d2d2d; color: #ffffff")
        # add status bar
        self.status = QStatusBar()
        #color status bar in dark
        self.status.setStyleSheet("background-color: #2d2d2d; color: #ffffff")
        # add all widgets to main window
        self.window = QMainWindow()
        #set dimensions
        self.window.resize(800,600)
        self.window.setMenuBar(self.bar)
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
            # add file content to text editor
            text.setText(f.read())
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
        self.save_as()
    def save_as(self):
        self.status.showMessage("Save file as")
        # open file dialog
        filename = QFileDialog.getSaveFileName(self.window, 'Save file', '/home')
        # save file
        with open(filename[0], 'w') as f:
            f.write(self.text.toPlainText())
        #update onglet name
        self.onglets.setTabText(self.onglets.currentIndex(), filename[0])
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
    def undo(self):
        self.text.undo()
        self.status.showMessage("Undo")
    def redo(self):
        self.text.redo()
        self.status.showMessage("Redo")
    def cut(self):
        self.text.cut()
        self.status.showMessage("Cut")
    def copy(self):
        self.text.copy()
        self.status.showMessage("Copy")
    def paste(self):
        self.text.paste()
        self.status.showMessage("Paste")
    def find(self):
        # create a box in the window to ask for susbtring to search
        text, ok = QInputDialog.getText(self.window, 'Find', 'Enter text:')
        # check if user clicked ok
        if ok:
            self.status.showMessage("Find: " + text)
            # search every occurence of the substring
            cursor = self.text.textCursor()
            cursor.setPosition(0)
            self.text.setTextCursor(cursor)
            # color every occurence of the substring
            while self.text.find(text):
                fmt = QTextCharFormat()
                fmt.setBackground(QBrush(QColor(255, 255, 0)))
                cursor = self.text.textCursor()
                cursor.mergeCharFormat(fmt)
                cursor.movePosition(QTextCursor.NextWord)
                self.text.setTextCursor(cursor)
        else:
            self.status.showMessage("Find")
    def close_onglet(self,index):
        # get onglet that is clicked
        # remove onglet
        self.onglets.removeTab(index)
        self.array.pop(index)
if __name__ == '__main__':
    import sys
    app=EngdromGUI(sys.argv)
