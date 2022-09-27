import sys
import math

from PyQt5.QtWidgets import *
from OpenGL import GL, GLU
from PyQt5.QtCore import QTimer
from org.pyengdrom.engine.camera import Camera

from org.pyengdrom.engine.project import EngineProject

class OpenGLEngine(QOpenGLWidget):
    def __init__(self, folder):
        super().__init__()
        self._timer = QTimer()
        self._timer.timeout.connect(self.update)
        self._timer.start(int(1000 / 60))
        self._project = EngineProject(folder)
    def initializeGL(self) -> None:
        self._context = self.context()
        self._project.level.initGL(self)

        width  = self.width()
        height = self.height()
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GLU.gluPerspective(45.0, float(width) / float(height), 0.1, 100.0)
        
        self.camera = Camera()

        return super().initializeGL()

    def paintGL(self) -> None:
        GL.glClearColor(0, 0, 0, 1)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        self._project.level.paintGL()
    def resizeGL(self, w: int, h: int) -> None:
        self._context = self.context()
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GLU.gluPerspective(45.0, float(w) / float(h), 0.1, 100.0)
        
        self.update()
