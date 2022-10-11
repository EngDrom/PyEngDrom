


from typing import List
from org.pyengdrom.engine.camera import Camera


class AbstractCameraController:
    def __new__(cls: type):
        assert cls != AbstractCameraController, "An AbstractCameraController can't be created"
        return super(AbstractCameraController, cls).__new__(cls)

    def move(self, camera, dp, speed=1):
        pass
    def rotate(self, camera, d_mouvemove, speed=1):
        pass
    def frame(self, engine):
        pass

class CameraController2D(AbstractCameraController):
    def __init__(self, move_enabled=True, slide_enabled=False):
        self.move_enabled  = move_enabled
        self.slide_enabled = slide_enabled
    def move(self, camera: Camera, dp: List[float], speed=1):
        if not self.move_enabled: return
        camera.translate(dp[0] * speed, dp[1] * speed, 0)
    def rotate(self, camera, d_mouvemove, speed=1):
        if not self.slide_enabled: return
        camera.translate(d_mouvemove[0] * speed, d_mouvemove[1] * speed, 0)
    def frame(self, engine):
        pass
