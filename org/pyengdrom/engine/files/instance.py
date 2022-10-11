

from org.pyengdrom.engine.camera import ModelMatrix
from org.pyengdrom.engine.files.material import Material

import numpy as np

class MeshInstance:
    UNIQUE_COLOR = 1
    def uniqueColor(self):
        if hasattr(self, "_uniqueColor"): return self._uniqueColor

        assert MeshInstance.UNIQUE_COLOR < 256 ** 3
        color = MeshInstance.UNIQUE_COLOR

        r = color % 256
        color -= r
        color /= 256
        g = color % 256
        color -= g
        color /= 256
        b = color

        MeshInstance.UNIQUE_COLOR += 1

        self._uniqueColor = np.array([r, g, b]) / 256
        return self._uniqueColor
    def __init__(self, *x):
        self.mesh = int(x[0][0])
        self.mat  = tuple(map(int, x[-1]))

        self.x,  self.y,  self.z  = tuple(map(float, x[1]))
        self.rx, self.ry, self.rz = tuple(map(float, x[2]))
        self.sx, self.sy, self.sz = tuple(map(float, x[3]))

        self.enabled = True
    def setEnabled(self, enabled):
        self.enabled = enabled
    def initGL(self, meshes, materials):
        self._gl_mesh = meshes[self.mesh]
        self._gl_mat  = tuple(map(lambda x: materials[x], self.mat))

        self.matrix = ModelMatrix()
        self.matrix.translate(self.x,  self.y,  self.z)
        self.matrix.rotate   (self.rx, self.ry, self.rz)
        self.matrix.scale    (self.sx, self.sy, self.sz)
    def paintGL(self):
        if not self.enabled: return
        
        self._gl_mat[0].useGL()
        self._gl_mesh.paintGL(self._gl_mat[0], self.matrix.get_matrix())
        self._gl_mat[0].unUseGL()
    def paintBackBuffer(self):
        if not self.enabled: return

        Material.get_backbuffer_material().useGL()
        #print(self.uniqueColor())
        self._gl_mesh.main_shader = Material.get_backbuffer_material().main_shader
        self._gl_mesh.setVec3(self.uniqueColor(), "mColor")

        self._gl_mesh.paintGL(Material.get_backbuffer_material(), self.matrix.get_matrix())