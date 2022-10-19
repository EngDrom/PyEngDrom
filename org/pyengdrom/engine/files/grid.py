
import numpy as np
from org.pyengdrom.engine.files.mesh import Mesh
from org.pyengdrom.engine.files.texture import AtlasTexture
from org.pyengdrom.rice.hitbox.box import CubeHitBox
from org.pyengdrom.rice.manager import WorldCollisionManager

class GridChunk(Mesh):
    def __init__(self, _map, atlas):
        super().__init__("<grid>")

        self._map = np.flip(np.rot90( np.array(_map) ))

        self.vao  = [ 3, 2 ]
        self.vbos = [ [], [] ]

        w, h = self._map.shape
        for dx in range(w):
            for dy in range(h):
                if self._map[dx][dy] == -1: continue

                u = len(self.indices) // 6 * 4
                self.vbos[0].extend([dx, dy, 0, dx + 1, dy, 0, dx + 1, dy + 1, 0, dx, dy + 1, 0])
                for v in atlas.coordinates(self._map[dx][dy]): 
                    self.vbos[1].extend(v)

                self.indices.extend([u, u + 1, u + 2, u, u + 3, u + 2])
        self.vbos[0] = list(map(float, self.vbos[0]))
        self.vbos[1] = list(map(float, self.vbos[1]))
        self._texture = atlas

class Grid:
    def __init__(self, atlas):
        self.atlas = atlas
        self.meshes = []

        self.vbos = [[]]
        self.vao = [3]

        self.main_shader = 0
    def setVec3(self, color, value):
        for mesh in self.meshes:
            mesh.main_shader = self.main_shader
            mesh.setVec3(color, value)
    @staticmethod
    def from_path(path, project, *args):
        with open(path, 'r') as f:
            return Grid.from_string(f.read())
    @staticmethod
    def from_string(string):
        lines = string.split("\n")
        state = -1
        atlas = None
        grid  = None
        colliders = []

        for line in lines:
            if line.startswith("atlas: "):
                _, img, atlas_file = line.split(" ")
                atlas = AtlasTexture(img, atlas_file)
                grid  = Grid(atlas)
            elif line.startswith("layer-") and line[-1] == ":":
                state = int(line[6:-1])
            elif line.startswith("collider:"):
                state = -2
            else:
                if state >= 0:
                    while state >= len(grid.meshes):
                        grid.meshes.append([])
                    grid.meshes[state].append(list(map(int, line.split(" "))))
                elif state == -2:
                    colliders.append(int(line))

        for idx in range(len(grid.meshes)):
            grid.meshes [idx] = GridChunk(grid.meshes[idx], atlas)
        grid.colliders = colliders
        return grid

    def paintGL(self, shader, mModel):
        for mesh in self.meshes:
            mesh.main_shader = self.main_shader
            mesh.paintGL(shader, mModel)
    def initGL(self, widget, world_collision):
        self.atlas.initGL()
        for mesh in self.meshes:
            mesh.main_shader = self.main_shader
            mesh.initGL(widget, world_collision)
        
        if hasattr(self, "colliders"): self.createColliders(world_collision)
    def createColliders(self, world_collision: WorldCollisionManager):
        for collider_id in self.colliders:
            _map = self.meshes[collider_id].vbos[0]
            
            for _pid in range(0, len(_map), 12):
                min_point = _map[_pid], _map[_pid + 1], -100
                _pid += 6
                max_point = _map[_pid], _map[_pid + 1], 100

                world_collision.boxes.append(CubeHitBox(min_point, max_point))

