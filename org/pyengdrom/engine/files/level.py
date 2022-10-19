'''
version: 0
mesh: 
    mesh_path
material:
    path *args
instances:
#   <mid> (X, Y, Z) (RX, RY, RZ) (SX, SY, SZ) [material_indices]
    (0), (1, 1, 1) (0, 0, 0) (1, 1, 1) ()
script:
    a.dmd
'''

import enum
from org.pyengdrom.api.controller import AttachedCameraController2D, CameraController2D
from org.pyengdrom.engine.files.grid import Grid
from org.pyengdrom.engine.files.instance import MeshInstance

from org.pyengdrom.engine.files.mesh import Mesh
from org.pyengdrom.engine.files.texture import AtlasTexture
from org.pyengdrom.rice.manager import Proxy

class Level:
    LAST_VERSION = "0"
    def __init__(self, path):
        self.path = path

        self.mesh_types = []
        self.materials  = []
        self.instances  = []
        self.scripts    = []

        self.camera_controller = CameraController2D()
    def initGL(self, widget, world_collision):
        self.widget = widget
        
        for mesh in self.mesh_types:
            mesh.initGL(widget, world_collision)
        for material in self.materials:
            material.initGL()
        for instance in self.instances:
            instance.initGL(self.mesh_types, self.materials)
        self.camera_controller = CameraController2D()
    def paintGL(self):
        for instance in self.instances:
            instance.paintGL()
    def paintBackBuffer(self):
        for instance in self.instances:
            instance.paintBackBuffer()
    def getInstanceByTrace(self, trace):
        for idx, instance in enumerate(self.instances):
            print(idx, instance.uniqueColor() - trace)
            if (abs(instance.uniqueColor() - trace) <= 10 ** -4 * 2).all():
                return idx

        return -1
    
    @staticmethod
    def read(path, project) -> "Level":
        text = ""
        with open(path, "r") as file: text = file.read()

        version, file = text.split("\n", 1)
        version_code = version[9:] if "version: " in version else Level.LAST_VERSION

        return getattr(Level, f"read_version_{version_code}")(file, path, project)
    @staticmethod
    def read_version_0(string, path, project):
        class ReadMode(enum.Enum):
            MESH = 0
            MAT  = 1
            INST = 2
            SCRP = 3
            UNKN = 4

        mode = ReadMode.UNKN
        level = Level(path)

        lines = string.split("\n")
        for line in lines:
            line = line.strip()
            if line[-1] == ":":
                nmode = line[:-1]
                if nmode == "mesh"     : mode = ReadMode.MESH
                if nmode == "instances": mode = ReadMode.INST
                if nmode == "material" : mode = ReadMode.MAT
                if nmode == "script"   : mode = ReadMode.SCRP
            else:
                if mode == ReadMode.SCRP:
                    level.scripts.append(line)
                elif mode == ReadMode.MAT:
                    level.materials.append(
                        project.load_mat(*line.split(" "))
                    )
                elif mode == ReadMode.MESH:
                    level.mesh_types.append(
                        project.load_mesh(*line.split(" "))
                    )
                else:
                    line = line[1:-1]
                    level.instances.append(
                        MeshInstance(
                            *map(lambda x: x.split(", "), line.split(") ("))
                        )
                    )
        
        return level