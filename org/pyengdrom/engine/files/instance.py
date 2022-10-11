

from org.pyengdrom.engine.camera import ModelMatrix
from org.pyengdrom.engine.files.material import Material

import numpy as np

from org.pyengdrom.rice.hitbox.box import CubeHitBox, NoHitBox

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
    def move(self, x, y, z):
        self.matrix.translate(x, y, z)
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
    
    def compute_hitbox_minmax(self):
        if hasattr(self, "_minmax_hitbox"): return self._minmax_hitbox

        vbo = self._gl_mesh.vbos[0]
        if len(vbo) <= 2: return None, None

        p0 = np.array([vbo[0], vbo[1], vbo[2]])
        p1 = np.array([vbo[0], vbo[1], vbo[2]])

        for x in range(3, len(vbo), 3):
            p0[0] = min(vbo[x],     p0[0])
            p0[1] = min(vbo[x + 1], p0[1])
            p0[2] = min(vbo[x + 2], p0[2])

            p1[0] = max(vbo[x],     p1[0])
            p1[1] = max(vbo[x + 1], p1[1])
            p1[2] = max(vbo[x + 2], p1[2])

        self._minmax_hitbox = [p0, p1]
        return self._minmax_hitbox
    def compute_hitbox(self):
        a, b = self.compute_hitbox_minmax()
        if a is None:
            self._hitbox = NoHitBox()
            return self._hitbox
        
        rp0 = np.array([[a[0]], [a[1]], [a[2]], [1]])
        rp1 = np.array([[b[0]], [b[1]], [b[2]], [1]])

        matrix = self.matrix.get_matrix().transpose()
        a = np.dot(matrix, rp0)[:3, 0]
        b = np.dot(matrix, rp1)[:3, 0]
        
        self._hitbox = CubeHitBox(a, b)
        return self._hitbox
    def get_position(self):
        matrix = self.matrix.get_matrix()

        return matrix[3, :3]