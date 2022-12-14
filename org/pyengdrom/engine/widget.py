import sys
import math

from PyQt5.QtWidgets import *
from OpenGL import GL, GLU
from PyQt5.QtCore import QTimer, Qt
import PyQt5.QtGui as QtGui
from org.pyengdrom.api.controller import AttachedCameraController2D
from org.pyengdrom.api.engine import AWAIT_LEVEL_LOADED
from org.pyengdrom.engine.camera import Camera
from org.pyengdrom.engine.files.texture import Texture

from org.pyengdrom.engine.project import EngineProject

import numpy as np
import matplotlib.pyplot as plt
from org.pyengdrom.pydromadaire.evaluate.nodes.attr import CallFunctionNode
from org.pyengdrom.rice.hitbox.box import CubeHitBox, HitBox

from org.pyengdrom.rice.manager import MOVEMODE_Bijection, MOVEMODE_Component, Manager, Proxy, WorldCollisionManager, run_calculation

class OpenGLEngine(QOpenGLWidget):
    TRANSLATE_SPEED = 10
    ROTATE_SPEED    = 10

    def __init__(self, folder):
        super().__init__()
        self._timer = QTimer()
        self._timer.timeout.connect(self.update)
        self._timer.start(int(1000 / 60))
        self._project = EngineProject(folder)
        self.run_trace_calculation = True
        self.callbacks = []
        self.pressed = False
        self.move_camera_by_frame = np.array([0.0, 0.0, 0.0])
        self.frame_id = 0

        # Temporary
        self._texture = Texture("./assets/demo/platformer/art_sheet.png")
        
    def initializeGL(self) -> None:
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glEnable(GL.GL_BLEND)

        self.world_collision = WorldCollisionManager()
        self.world_collision.boxes.append(CubeHitBox([-10, -15, -20], [10, -5, 0]))
        self.physics_managers = []
        for instance in self._project.level.instances[2:3]:
            proxy = Proxy(instance, 1000, MOVEMODE_Component | MOVEMODE_Bijection, self.world_collision)
            self.physics_managers.append(Manager(proxy))

        self._context = self.context()
        self._project.level.initGL(self, self.world_collision)
        self._texture.initGL()
        for instance in self._project.level.instances:
            instance._gl_mesh._texture = self._texture
        
        self._project.level.camera_controller = AttachedCameraController2D(self._project.level.instances[2], self.physics_managers[0].proxy)

        width  = self.width()
        height = self.height()
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GLU.gluPerspective(45.0, float(width) / float(height), 0.1, 100.0)
        
        self.camera = Camera()

        for stack_data in self._project.level.scripts_stack:
            if stack_data is not None and stack_data.__global__ is not None and AWAIT_LEVEL_LOADED in stack_data.__global__.dict:
                for stack, func in stack_data.__global__.dict[AWAIT_LEVEL_LOADED]:
                    runner = CallFunctionNode(func, (self, ))
                    
                    runner.evaluate(stack)

        return super().initializeGL()

    def getControllers(self):
        return [ self._project.level.camera_controller ]
    def addTraceCalculationCallback(self, callback):
        self.callbacks.append(callback)
        self.run_trace_calculation = True
    def getTraceCalculation(self, x, y):
        if not hasattr(self, 'trace_calculation'): return 0

        x = math.floor(x)
        y = math.floor(y)

        return self._project.level.getInstanceByTrace(self.trace_calculation[y, x])
    def paintGL(self) -> None:
        self.frame_id += 1
        run_calculation(self.physics_managers, 1 / 60)
        
        controller = self._project.level.camera_controller
        controller.move(self.camera, self.move_camera_by_frame, self.TRANSLATE_SPEED)
        controller.frame(self.camera)
        
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
        # x, y = a0.x(), a0.y() # WARNING NEEDED (otherwise conflict with c++ destructors)
        # self.addTraceCalculationCallback(lambda u: self.hideClicked(u, x, y))
        # return
        self.pressed     = True
        self.last_point  = a0.pos().x(), a0.pos().y()
        self.start_point = a0.pos().x(), a0.pos().y()
        self.button      = a0.button()
        return super().mousePressEvent(a0)
    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        dx, dy = a0.pos().x() - self.last_point[0], a0.pos().y() - self.last_point[1]
        self.last_point = a0.pos().x(), a0.pos().y()
        
        if self.button == 1: 
            self._project.level.camera_controller.rotate(self.camera, [dx / min(self.width(), self.height()), - dy / min(self.width(), self.height())], self.ROTATE_SPEED)
        
        return super().mouseMoveEvent(a0)
    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.pressed = False
        self.button  = -1
        return super().mouseReleaseEvent(a0)
    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() == Qt.Key.Key_Up:    self.move_camera_by_frame[1] -= 0.01
        if a0.key() == Qt.Key.Key_Down:  self.move_camera_by_frame[1] += 0.01
        if a0.key() == Qt.Key.Key_Left:  self.move_camera_by_frame[0] += 0.01
        if a0.key() == Qt.Key.Key_Right: self.move_camera_by_frame[0] -= 0.01

        return super().keyPressEvent(a0)
    def keyReleaseEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() == Qt.Key.Key_Up:    self.move_camera_by_frame[1] += 0.01
        if a0.key() == Qt.Key.Key_Down:  self.move_camera_by_frame[1] -= 0.01
        if a0.key() == Qt.Key.Key_Left:  self.move_camera_by_frame[0] -= 0.01
        if a0.key() == Qt.Key.Key_Right: self.move_camera_by_frame[0] += 0.01

        return super().keyReleaseEvent(a0)