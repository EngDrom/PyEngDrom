from org.pyengdrom.pydromadaire.lexer.lexer import Lexer
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
class TextEditor(QTextEdit):
    def insertFromMimeData(self, source):
        if source.hasText():
            self.insertPlainText(source.text())
            self.init_lexer()
        else:
            super().insertFromMimeData(source)
    def __init__(self,text):
        super().__init__()
        self.setAcceptRichText(False)
        self.setLineWrapMode(QTextEdit.NoWrap)
        self.setPlainText(text)
        self.text= text
        self.init_lexer()
        super().textChanged.connect(self.textChanged)
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Tab:
            self.insertPlainText("    ")
        else:
            super(TextEditor, self).keyPressEvent(event)
    def updateTitle(self,title):
        # parent is an QTabWidget
        self.parent().setTabText(self.parent().indexOf(self),title)
    def getTitle(self):
        return self.parent().tabText(self.parent().indexOf(self))
    def getText(self):
        return self.text
    #update self.text on textChanged
    def textChanged(self):
        #print("text changed",self.var)
        # check if some text was paste
        self.text = self.toPlainText()
        if self.var:
            self.update_line(self.toPlainText(),self.textCursor().blockNumber())
    def init_lexer(self):
        self.var=False
        try:
            tokens=Lexer(self.text,"<engdrom:editor>",_raise=False)._build()
        except BaseException as e:
            tokens=[]
            print(e)
        # color every token in blue
        for i in tokens[:-1]:
            # get cursor
            cursor = self.textCursor()
            start=i.pos
            if i.get_type()!="STRING":
                end=i.pos+len(i.get_value())
            else:
                end=i.pos+len(i.get_value())+2
            cursor.setPosition(start)
            cursor.setPosition(end,QTextCursor.KeepAnchor)
            # set color
            fmt=QTextCharFormat()
            # check type of token
            if i.get_type() == "NAME":
                fmt.setForeground(QColor(0,255,255))
            elif i.get_type() == "STRING":
                fmt.setForeground(QColor(255,0,0))
            elif i.get_type() == "NUMBER":
                fmt.setForeground(QColor(0,255,0))
            elif i.get_type() in ["TIMES","DIVIDE","PLUS","MINUS","SET"]:
                fmt.setForeground(QColor(255,0,255))
            elif i.get_type() in ["EQUALS","GREATER","LESS","NOT","OR","XOR","AND","VERT_LINE","B_AND","B_OR"]:
                fmt.setForeground(QColor(199,76,56))
            else:
                fmt.setForeground(QColor(255,255,255))
            cursor.mergeCharFormat(fmt)
            # set cursor
            self.setTextCursor(cursor)
        if len(tokens)>1:
            cursor = self.textCursor()
            cursor.setPosition(end)
            self.setTextCursor(cursor)
        self.var=True
        print(self.var)

    def update_line(self,text,line):
        #print("coucou")
        self.var=False
        cursorpos=self.textCursor().position()
        #print(line)
        try:
            tokens=Lexer(text.split("\n")[line],"<engdrom:editor>",_raise=False)._build()
            #print(tokens)
            cursor = self.textCursor()
            # get position of line begin
            cursor.movePosition(QTextCursor.StartOfLine)
            begin_of_line=cursor.position()
            for i in tokens[:-1]:
                cursor = self.textCursor()
                start=begin_of_line+i.pos
                if i.get_type()!="STRING":
                    end=begin_of_line+i.pos+len(i.get_value())
                else:
                    end=begin_of_line+i.pos+len(i.get_value())+2
                cursor.setPosition(start)
                cursor.setPosition(end,QTextCursor.KeepAnchor)
                # set color
                fmt=QTextCharFormat()
                # check type of token
                if i.get_type() == "NAME":
                    fmt.setForeground(QColor(0,255,255))
                elif i.get_type() == "STRING":
                    fmt.setForeground(QColor(255,0,0))
                elif i.get_type() == "NUMBER":
                    fmt.setForeground(QColor(0,255,0))
                elif i.get_type() in ["TIMES","DIVIDE","PLUS","MINUS","SET"]:
                    fmt.setForeground(QColor(255,0,255))
                elif i.get_type() in ["EQUALS","GREATER","LESS","NOT","OR","XOR","AND","VERT_LINE","B_AND","B_OR"]:
                    fmt.setForeground(QColor(199,76,56))
                else:
                    fmt.setForeground(QColor(255,255,255))
                cursor.mergeCharFormat(fmt)
                # set cursor
                self.setTextCursor(cursor)
            cursor = self.textCursor()
            cursor.setPosition(cursorpos)
            self.setTextCursor(cursor)
        except Exception as e:
            print(e)
        finally:
            self.var=True