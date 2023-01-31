
from org.pyengdrom.api.controller import CameraController2D
from org.pyengdrom.editor.base import EditorMode


class IdleEditorMode(EditorMode):
    def __init__(self,*args,**kwargs):
        super().__init__()
        self.controller=CameraController2D(True, True)
    def restartGL(self, engine):
        print("restartGL")
        engine._project.level.restartGL()

        #self.controller = CameraController2D(True, True)
        #super().restartGL()
    def startPaintGL(self, engine):
        #self.controller = CameraController2D(True, True)
        controller = self.controller
        controller.move(engine.camera, engine.move_camera_by_frame, engine.TRANSLATE_SPEED)
        controller.frame(engine.camera)

        return
    def rotateGL(self, engine, dx, dy):
        self.controller.rotate(engine.camera, [dx / min(engine.width(), engine.height()), - dy / min(engine.width(), engine.height())], engine.ROTATE_SPEED)
