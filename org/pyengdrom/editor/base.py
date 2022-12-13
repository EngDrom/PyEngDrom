from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class EditorMode(QWidget):
    def __init__(self):
        super().__init__()
        self.scroll=QScrollArea()
        self.selected=[]
        # show atlas as image
        atlas_path="assets/demo/platformer/art_sheet.png"
        self._atlas = QPixmap(atlas_path)
        # create a transparent mask
        self._mask = self._atlas.createMaskFromColor(QColor(Qt.transparent),Qt.MaskOutColor)
        self.p=QPainter(self._atlas)
        self.p.setPen(QColor(255,255,255))
        self.p.drawPixmap(self._atlas.rect(),self._mask, self._mask.rect())
        self.p.end()
        self.atlas = self._atlas.scaled(self._atlas.width()/self._atlas.height()*self.height(),self.height()+38)
        self.atlas_label = QLabel()
        self.atlas_label.setPixmap(self.atlas)
        # set full height
        self.atlas_label.resize(self._atlas.width()/self._atlas.height()*self.height(),self.height())
        # superpose a grid of 16*16 tiles on the image
        self.grid = QPixmap(self.atlas.width(),self.atlas.height())
        self.grid.fill(Qt.transparent)
        painter = QPainter(self.grid)
        painter.setPen(QPen(Qt.red, 1, Qt.SolidLine))
        for i in range(0,self.atlas.width(),int(self.atlas.width()/17)):
            painter.drawLine(i,0,i,self.atlas.height())
        for i in range(0,self.atlas.height(),int((self.atlas.height()+2)/8)):
            painter.drawLine(0,i,self.atlas.width(),i)
        painter.end()
        # superpose both grid and atlas
        self.grid_label = QLabel()
        self.grid_label.setPixmap(self.grid)
        self.grid_label.resize(self.atlas.width(),self.atlas.height())
        self.grid_label.move(0,0)
        self.atlas_label.move(0,0)
        self.grid_label.setMask(self.grid.mask())
        self.atlas_label.setMask(self.atlas.mask())

        # add scroll area
        self.scroll.setWidget(self.atlas_label)
        self.scroll.setWidgetResizable(True)
        self.scroll.move(0,0)

        # add grid
        self.grid_label.setParent(self.atlas_label)
        self.grid_label.move(0,0)

        # add to layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.scroll)
        self.setLayout(self.layout)
    
    def resizeEvent(self,e):
        #print()
        self.atlas=self._atlas.scaled(self._atlas.width()/self._atlas.height()*self.height(),self.height()-35)
        self.atlas_label.resize(self._atlas.width()/self._atlas.height()*self.height(),self.height()-35)
        self.atlas_label.setPixmap(self.atlas)
        self.scroll.setWidget(self.atlas_label)
        self.grid = QPixmap(self.atlas.width(),self.atlas.height())
        self.grid.fill(Qt.transparent)
        painter = QPainter(self.grid)
        painter.setPen(QPen(Qt.red, 1, Qt.SolidLine))
        for i in range(0,17):
            w=i*(self.atlas.width()/17+1)
            painter.drawLine(w-i,0,w-i,self.atlas.height())
        for i in range(0,8):
            h=i*(self.atlas.height()/8+1)
            painter.drawLine(0,h-i,self.atlas.width(),h-i)
        painter.end()
        self.grid_label.setPixmap(self.grid)
        self.grid_label.resize(self.atlas.width(),self.atlas.height())
        self.grid_label.move(0,0)
        self.atlas_label.move(0,0)
        self.grid_label.setMask(self.grid.mask())
        self.atlas_label.setMask(self.atlas.mask())
        self.grid_label.setParent(self.atlas_label)
        self.grid_label.move(0,0)
    # get double click event on image
    def mouseDoubleClickEvent(self,e):
        # get position on image
        x=e.pos().x()
        y=e.pos().y()
        # get decalage of image
        dx=self.atlas_label.pos().x()
        dy=self.atlas_label.pos().y()
        # get position on grid
        gx=(x-dx)//(self.atlas.width()/17)
        gy=(y-dy)//(self.atlas.height()/8)
        # color the selected tile in yellow with an opacity of 50%
        if (gx,gy) in self.selected:
            self.selected.remove((gx,gy))
        else:
            self.selected.clear()
            self.selected.append((gx,gy))
        # update grid
        self.grid = QPixmap(self.atlas.width(),self.atlas.height())
        self.grid.fill(Qt.transparent)
        painter = QPainter(self.grid)
        painter.setPen(QPen(Qt.red, 1, Qt.SolidLine))
        for i in range(0,17):
            w=i*(self.atlas.width()/17+1)
            painter.drawLine(w-i,0,w-i,self.atlas.height())
        for i in range(0,8):
            h=i*(self.atlas.height()/8+1)
            painter.drawLine(0,h-i,self.atlas.width(),h-i)
        painter.setPen(QPen(QColor(255,255,0,128), 1, Qt.SolidLine))
        painter.setBrush(QBrush(QColor(255,255,0,128), Qt.SolidPattern))
        for i in self.selected:
            painter.drawRect(i[0]*(self.atlas.width()/17),i[1]*(self.atlas.height()/8),self.atlas.width()/17,self.atlas.height()/8)
        painter.end()
        self.grid_label.setPixmap(self.grid)
        self.grid_label.resize(self.atlas.width(),self.atlas.height())
        #self.grid_label.move(0,0)
        #self.atlas_label.move(0,0)
        self.grid_label.setMask(self.grid.mask())
        self.atlas_label.setMask(self.atlas.mask())
        self.grid_label.setParent(self.atlas_label)