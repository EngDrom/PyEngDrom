from org.pyengdrom.editor.base import EditorMode
from org.pyengdrom.editor.idle import IdleEditorMode
from org.pyengdrom.engine.camera import MatrixMaintainer
from org.pyengdrom.engine.files.grid import Grid
from org.pyengdrom.engine.files.material import Material
from org.pyengdrom.engine.files.mesh import Mesh

import numpy as np
from math import floor
from OpenGL.GL import *

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

FRAG_TEXT = '''
#version 330 core
out vec4 _fragColor;
in vec2 pTC;
void main()
{
    float opacity = 0;
    
    int ux = int( abs(pTC.x * 1000) );
    int uy = int( abs(pTC.y * 1000) );
    int rx = ux % 1000;
    int ry = uy % 1000;

    if (rx <= 25 || ry <= 25) {
        opacity = 1;
    }

    _fragColor = vec4(0, 0, 0, 0);

    float c0 = 255;
    float c1 = 89;
    float c2 = 101;
    float c3 = 111;

    if ((ux > 20 && rx <= 15) || (ry <= 15 && uy > 20)) {
        _fragColor = vec4(c1 / c0, c2 / c0, c3 / c0, 1);
    }
    if (ux < 15 || uy < 15) {
        _fragColor = vec4(c1 / c0, c2 / c0, c3 / c0, 1);
    }
}
'''
VERT_TEXT = '''
#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec2 tC;

uniform mat4 mView;
uniform mat4 mProj;

out vec2 pTC;
void main()
{
    pTC = (mView * vec4(aPos, 1.0)).xy;
    gl_Position = mProj * vec4(aPos, 1.0);
}
'''

#
# TODO compute proporition coefficient (GX, GY) from width, height, projection matrix and grid position
#

GRID_COUNT_Y = 800 / 774 * 8
GRID_COUNT_X = GRID_COUNT_Y 

class EditorGridMode(IdleEditorMode):
    def __init__(self, grid,engine):
        self.grid=grid
        print("init")
        super().__init__()

        self.project=engine._project
        for instance in engine._project.level.instances:
            if isinstance(engine._project.level.mesh_types[instance.mesh], Grid):
                self.grid = engine._project.level.mesh_types[instance.mesh]
                self.grid_pos = instance.x, instance.y, instance.z
        self.atlas_=self.grid.atlas
        self.sizex,self.sizey=self.atlas_.size()
        self.w,self.h=self.atlas_.atlas[-1][2:]
        self.hi=self.sizex//self.h
        self.wi=self.sizey//self.w
        #self.atlas_value=-1
        self.mesh = Mesh("!")
        self.mesh.vao = [ 3, 2 ]
        self.mesh.vbos = [
            [
                -100, -100, -10, # TODO make mesh permanent
                -100,  100, -10, # TODO make mesh permanent
                 100, -100, -10, # TODO make mesh permanent
                 100,  100, -10  # TODO make mesh permanent
            ],
            [
                -1, -1,
                -1, 1,
                1, -1,
                1, 1,
            ]
        ]

        self.mesh.indices = [ 0, 1, 2, 1, 2, 3 ]

        self.material = Material("!")

        self.material.frag = FRAG_TEXT
        self.material.vert = VERT_TEXT
        super().__init__()
        self.scroll=QScrollArea()
        self.selected=[]
        # show atlas as image
        atlas_path=self.atlas_.path
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
        self.atlasgrid = QPixmap(self.atlas.width(),self.atlas.height())
        self.atlasgrid.fill(Qt.transparent)
        painter = QPainter(self.atlasgrid)
        painter.setPen(QPen(Qt.red, 1, Qt.SolidLine))
        for i in range(0,self.atlas.width(),int(self.atlas.width()/self.wi)):
            painter.drawLine(i,0,i,self.atlas.height())
        for i in range(0,self.atlas.height(),int((self.atlas.height()+2)/self.hi)):
            painter.drawLine(0,i,self.atlas.width(),i)
        painter.end()
        # superpose both grid and atlas
        self.grid_label = QLabel()
        self.grid_label.setPixmap(self.atlasgrid)
        self.grid_label.resize(self.atlas.width(),self.atlas.height())
        self.grid_label.move(0,0)
        self.atlas_label.move(0,0)
        self.grid_label.setMask(self.atlasgrid.mask())
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
    
    
    ##################
    # OpenGL related #
    ##################

    def restartGL(self, engine):
        self.mesh.initGL(None, None)
        self.material.initGL()
        super().restartGL(engine)
    def endPaintGL(self, engine):
        self.material.useGL()
        pos = np.dot(engine.camera.get_matrix().transpose(), np.array([[0], [0], [0], [1]]))
        matrix = MatrixMaintainer()
        matrix.translate(*-np.reshape(pos, (4))[:3])

        self.matrix = matrix

        self.mesh.main_shader = self.material.main_shader
        #self.proj_matrix = glGetDoublev(GL_PROJECTION_MATRIX)
        self.mesh.setMatrix( matrix.get_matrix(), "mView" )
        self.mesh.paintGL(self.material, None)
    
    def mouseClick(self, engine, button, x, y):
        print(self.atlas_value)
        for instance in engine._project.level.instances:
            if isinstance(engine._project.level.mesh_types[instance.mesh], Grid):
                self._grid = engine._project.level.mesh_types[instance.mesh]
                self._grid_pos = instance.x, instance.y, instance.z
        new_value = -1 if button == 2 else self.atlas_value
        pos = np.dot(engine.camera.get_matrix().transpose(), np.array([[0], [0], [0], [1]]))
        y = engine.height() - y
        gy = GRID_COUNT_Y
        gx = GRID_COUNT_X * engine.width() / engine.height()

        rx = (x - engine.width()  / 2) / engine.width()  * gx - pos[0][0]
        ry = (y - engine.height() / 2) / engine.height() * gy - pos[1][0]
        self.grid.modify(1, floor(rx), floor(ry), new_value)
    def save(self, engine):
        for instance in engine._project.level.instances:
            if isinstance(engine._project.level.mesh_types[instance.mesh], Grid):
                self.grid = engine._project.level.mesh_types[instance.mesh]
                self.grid_pos = instance.x, instance.y, instance.z
        
        self.grid.save()
    def resizeEvent(self,e):
        #print()
        self.atlas=self._atlas.scaled(self._atlas.width()/self._atlas.height()*self.height(),self.height()-35)
        self.atlas_label.resize(self._atlas.width()/self._atlas.height()*self.height(),self.height()-35)
        self.atlas_label.setPixmap(self.atlas)
        self.scroll.setWidget(self.atlas_label)
        self.atlasgrid = QPixmap(self.atlas.width(),self.atlas.height())
        self.atlasgrid.fill(Qt.transparent)
        painter = QPainter(self.atlasgrid)
        painter.setPen(QPen(Qt.red, 1, Qt.SolidLine))
        for i in range(0,self.hi):
            w=i*(self.atlas.width()/self.hi+1)
            painter.drawLine(w-i,0,w-i,self.atlas.height())
        for i in range(0,self.wi):
            h=i*(self.atlas.height()/self.wi+1)
            painter.drawLine(0,h-i,self.atlas.width(),h-i)
        painter.end()
        self.grid_label.setPixmap(self.atlasgrid)
        self.grid_label.resize(self.atlas.width(),self.atlas.height())
        self.grid_label.move(0,0)
        self.atlas_label.move(0,0)
        self.grid_label.setMask(self.atlasgrid.mask())
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
        print(x,y,dx,dy)
        # get position on grid
        self.atlas_value=-1
        print(self.atlas_.atlas)
        for i in range(len(self.atlas_.atlas)):
            x1,y1,w1,h1=self.atlas_.atlas[i]
            if x1<=(x-dx)/(self.atlas.width()/self.hi)*self.w<=x1+w1 and y1<=(y-dy)/(self.atlas.height()/self.wi)*self.h<=y1+h1:
                self.atlas_value=i
                break
        print((x-dx)/(self.atlas.width()/self.hi)*self.w,(y-dy)/(self.atlas.height()/self.wi)*self.h)
        gx=(x-dx)//(self.atlas.width()/self.hi)
        gy=(y-dy)//(self.atlas.height()/self.wi)
        # color the selected tile in yellow with an opacity of 50%
        if (gx,gy) in self.selected:
            self.selected.remove((gx,gy))
        else:
            self.selected.clear()
            self.selected.append((gx,gy))
        # update grid
        self.atlasgrid = QPixmap(self.atlas.width(),self.atlas.height())
        self.atlasgrid.fill(Qt.transparent)
        painter = QPainter(self.atlasgrid)
        painter.setPen(QPen(Qt.red, 1, Qt.SolidLine))
        for i in range(0,self.hi):
            w=i*(self.atlas.width()/self.hi+1)
            painter.drawLine(w-i,0,w-i,self.atlas.height())
        for i in range(0,self.wi):
            h=i*(self.atlas.height()/self.wi+1)
            painter.drawLine(0,h-i,self.atlas.width(),h-i)
        painter.setPen(QPen(QColor(255,255,0,128), 1, Qt.SolidLine))
        painter.setBrush(QBrush(QColor(255,255,0,128), Qt.SolidPattern))
        for i in self.selected:
            painter.drawRect(i[0]*(self.atlas.width()/self.hi),i[1]*(self.atlas.height()/self.wi),self.atlas.width()/self.hi,self.atlas.height()/self.wi)
        painter.end()
        self.grid_label.setPixmap(self.atlasgrid)
        self.grid_label.resize(self.atlas.width(),self.atlas.height())
        #self.grid_label.move(0,0)
        #self.atlas_label.move(0,0)
        self.grid_label.setMask(self.atlasgrid.mask())
        self.atlas_label.setMask(self.atlas.mask())
        self.grid_label.setParent(self.atlas_label)