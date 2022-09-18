

from org.pyengdrom.engine.camera import ModelMatrix


class MeshInstance:
    def __init__(self, *x):
        self.mesh = int(x[0][0])
        self.mat  = tuple(map(int, x[-1]))

        self.x,  self.y,  self.z  = tuple(map(float, x[1]))
        self.rx, self.ry, self.rz = tuple(map(float, x[2]))
        self.sx, self.sy, self.sz = tuple(map(float, x[3]))
    def initGL(self, meshes, materials):
        self._gl_mesh = meshes[self.mesh]
        self._gl_mat  = tuple(map(lambda x: materials[x], self.mat))

        self.matrix = ModelMatrix()
        self.matrix.translate(self.x,  self.y,  self.z)
        self.matrix.rotate   (self.rx, self.ry, self.rz)
        self.matrix.scale    (self.sx, self.sy, self.sz)
    def paintGL(self):
        self._gl_mat[0].useGL()
        self._gl_mesh.paintGL(self._gl_mat[0], self.matrix.get_matrix())
        self._gl_mat[0].unUseGL()