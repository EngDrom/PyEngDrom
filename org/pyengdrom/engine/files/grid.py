
import numpy as np
from org.pyengdrom.engine.files.mesh import Mesh
from org.pyengdrom.engine.files.texture import AtlasTexture
from org.pyengdrom.rice.hitbox.box import CubeHitBox
from org.pyengdrom.rice.manager import WorldCollisionManager

class GridChunk(Mesh):
    def __init__(self, _map, delta, atlas):
        super().__init__("<grid>")

        self._map = np.flip(np.rot90( np.array(_map) ))
        ndx, ndy = delta

        self.vao  = [ 3, 2 ]
        self.vbos = [ [], [] ]

        w, h = self._map.shape
        for dx in range(w):
            for dy in range(h):
                if self._map[dx][dy] == -1: continue

                u = len(self.indices) // 6 * 4
                self.vbos[0].extend([ndx + dx, ndy + dy, 0, ndx + dx + 1, ndy + dy, 0, ndx + dx + 1, ndy + dy + 1, 0, ndx + dx, ndy + dy + 1, 0])
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
            return Grid.from_string(project, f.read())
    @staticmethod
    def from_string(project, string):
        lines = string.split("\n")
        state = -1
        atlas = None
        grid  = None
        colliders = []

        for line in lines:
            if line.startswith("atlas: "):
                _, atlas_file = line.split(" ")
                atlas = AtlasTexture(project, project.build_path(atlas_file))
                grid  = Grid(atlas)
            elif line.startswith("layer-") and line[-1] == ":":
                state = int(line[6:-1])
                while state >= len(grid.meshes):
                    grid.meshes.append([[], [0, 0]])
            elif line.startswith("collider:"):
                state = -2
            elif line.startswith("dx: ") and state >= 0:
                grid.meshes[state][1][0] = int(line[4:])
            elif line.startswith("dy: ") and state >= 0:
                grid.meshes[state][1][1] = int(line[4:])
            else:
                if state >= 0:
                    grid.meshes[state][0].append(list(map(int, line.split(" "))))
                elif state == -2:
                    colliders.append(int(line))

        for idx in range(len(grid.meshes)):
            grid.meshes [idx] = GridChunk(grid.meshes[idx][0], grid.meshes[idx][1], atlas)
        grid.colliders = colliders
        return grid

    def paintGL(self, shader, mModel, **kwargs):
        for mesh in self.meshes:
            mesh.main_shader = self.main_shader
            mesh.paintGL(shader, mModel, **kwargs)
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

