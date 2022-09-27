import sys
import math

from PyQt5.QtWidgets import *
from OpenGL import GL, GLU
from PyQt5.QtCore import QTimer
import PyQt5.QtGui as QtGui
from org.pyengdrom.engine.camera import Camera

from org.pyengdrom.engine.project import EngineProject

import numpy as np
import matplotlib.pyplot as plt

class OpenGLEngine(QOpenGLWidget):
    def __init__(self, folder):
        super().__init__()
        self._timer = QTimer()
        self._timer.timeout.connect(self.update)
        self._timer.start(int(1000 / 60))
        self._project = EngineProject(folder)
        self.run_trace_calculation = True
        self.callbacks = []
        
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

    def addTraceCalculationCallback(self, callback):
        self.callbacks.append(callback)
        self.run_trace_calculation = True
    def getTraceCalculation(self, x, y):
        if not hasattr(self, 'trace_calculation'): return 0

        x = math.floor(x)
        y = math.floor(y)

        return self._project.level.getInstanceByTrace(self.trace_calculation[y, x])
    def paintGL(self) -> None:
        if self.run_trace_calculation:
            GL.glClearColor(0, 0, 0, 1)
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            self._project.level.paintBackBuffer()
            self.run_trace_calculation = False
            GL.glFinish()

            x0, y0, x1, y1 = GL.glGetIntegerv(GL.GL_VIEWPORT)
            self.trace_calculation = np.array( GL.glReadPixels(0, 0, x1 - x0, y1 - y0, GL.GL_RGB, GL.GL_FLOAT) )
            self.trace_calculation = np.flip(np.reshape(self.trace_calculation, (y1 - y0, x1 - x0, 3)), axis=0)
            
            for callback in self.callbacks: callback(self)
            self.callbacks = []
        GL.glClearColor(0, 0, 0, 1)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        self._project.level.paintGL()
    def resizeGL(self, w: int, h: int) -> None:
        self._context = self.context()
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GLU.gluPerspective(45.0, float(w) / float(h), 0.1, 100.0)
        
        self.update()
    
    def hideClicked(self, widget: "OpenGLEngine", x, y):
        index = self.getTraceCalculation(x, y)

        for instance in self._project.level.instances:
            instance.setEnabled(True)
        self._project.level.instances[index].setEnabled(False)
    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        x, y = a0.pos().x(), a0.pos().y()
        if (a0.button() == 1):
            self.addTraceCalculationCallback(lambda u: self.hideClicked(u, x, y))
        return super().mousePressEvent(a0)
