
from org.pyengdrom.editor.base import EditorMode

from org.pyengdrom.rice.manager import run_calculation

class RunningMode(EditorMode):
    def restartGL(self, engine):
        engine._project.level.restartGL()
    def startPaintGL(self, engine):
        run_calculation(engine.physics_managers, 1 / 60)
        
        controller = engine._project.level.camera_controller
        controller.move(engine.camera, engine.move_camera_by_frame, engine.TRANSLATE_SPEED)
        controller.frame(engine.camera)

        return
    def rotateGL(self, engine, dx, dy):
        engine._project.level.camera_controller.rotate(engine.camera, [dx / min(engine.width(), engine.height()), - dy / min(engine.width(), engine.height())], engine.ROTATE_SPEED)
