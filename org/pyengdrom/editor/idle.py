
from org.pyengdrom.api.controller import CameraController2D
from org.pyengdrom.editor.base import EditorMode


class IdleEditorMode(EditorMode):
    def restartGL(self, engine):
        engine._project.level.restartGL()

        self.controller = CameraController2D(True, True)
    def paintGL(self, engine):
        controller = self.controller
        controller.move(engine.camera, engine.move_camera_by_frame, engine.TRANSLATE_SPEED)
        controller.frame(engine.camera)

        return
    def rotateGL(self, engine, dx, dy):
        self.controller.rotate(engine.camera, [dx / min(engine.width(), engine.height()), - dy / min(engine.width(), engine.height())], engine.ROTATE_SPEED)
