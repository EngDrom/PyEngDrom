from org.pyengdrom.editor.base import EditorMode
from org.pyengdrom.editor.idle import IdleEditorMode
from org.pyengdrom.engine.camera import MatrixMaintainer
from org.pyengdrom.engine.files.grid import Grid
from org.pyengdrom.engine.files.material import Material
from org.pyengdrom.engine.files.mesh import Mesh

import numpy as np
from math import floor
from OpenGL.GL import *

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
    def __init__(self, grid):
        super().__init__()

        self.grid = grid
        self.atlas_value = 10

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
        for instance in engine._project.level.instances:
            if isinstance(engine._project.level.mesh_types[instance.mesh], Grid):
                self.grid = engine._project.level.mesh_types[instance.mesh]
                self.grid_pos = instance.x, instance.y, instance.z
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