
import numpy as np
import glm
import inspect
from OpenGL import GL

class MatrixMaintainer:
    def __init__(self):
        self.mat = glm.mat4()
    def translate(self, x, y, z):
        self.mat = glm.translate(self.mat, (x, y, z))
    def rotate(self, rx, ry, rz):
        self.mat = glm.rotate(self.mat, glm.radians(rx), (1, 0, 0))
        self.mat = glm.rotate(self.mat, glm.radians(ry), (0, 1, 0))
        self.mat = glm.rotate(self.mat, glm.radians(rz), (0, 0, 1))
    def scale(self, sx, sy, sz):
        self.mat = glm.scale(self.mat, (sx, sy, sz))
    def get_matrix(self):
        return np.array(self.mat).transpose().reshape(4,4)

Camera      = MatrixMaintainer
ModelMatrix = MatrixMaintainer
