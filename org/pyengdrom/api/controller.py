


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

class CameraController2D(AbstractCameraController):
    def move(self, camera: Camera, dp: List[float], speed=1):
        camera.translate(dp[0] * speed, dp[1] * speed, 0)
    def rotate(self, camera, d_mouvemove, speed=1):
        camera.translate(d_mouvemove[0] * speed, d_mouvemove[1] * speed, 0)
