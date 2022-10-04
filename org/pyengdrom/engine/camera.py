
import numpy as np
import glm
import inspect
from OpenGL import GL

class MatrixMaintainer:
    def __init__(self):
        self.mat = glm.mat4()
        self.rot_mat = glm.mat4()
    def translate(self, x, y, z):
        self.mat = glm.translate(self.mat, (x, y, z))
    def translateLocal(self, x, y, z):
        pass # TODO transform translation vector to local rotated system and then apply
    def rotate(self, rx, ry, rz):
        self.rot_mat = glm.rotate(self.rot_mat, glm.radians(rx), (1, 0, 0))
        self.rot_mat = glm.rotate(self.rot_mat, glm.radians(ry), (0, 1, 0))
        self.rot_mat = glm.rotate(self.rot_mat, glm.radians(rz), (0, 0, 1))
        # TODO transform translation vector to new coordinate system
    def scale(self, sx, sy, sz):
        self.mat = glm.scale(self.mat, (sx, sy, sz))
    def get_matrix(self):
        return np.dot(np.array(self.rot_mat), np.array(self.mat)).transpose().reshape(4,4)

Camera      = MatrixMaintainer
ModelMatrix = MatrixMaintainer
