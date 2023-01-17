
import numpy as np
from math import ceil, floor
from org.pyengdrom.engine.files.mesh import Mesh
from org.pyengdrom.engine.files.texture import AtlasTexture
from org.pyengdrom.rice.hitbox.box import CubeHitBox
from org.pyengdrom.rice.hitbox.grid import GridLayerHitBox
from org.pyengdrom.rice.manager import WorldCollisionManager

from io import StringIO

SUBDIVISION_SIZE = 16

class GridLayer:
    def modify (self, x, y, new_value):
        rx, ry = x - self.delta[0], y - self.delta[1]
        px, py = floor(rx / SUBDIVISION_SIZE), floor( ry / SUBDIVISION_SIZE)
        ix, iy = rx - px * SUBDIVISION_SIZE, ry - py * SUBDIVISION_SIZE

        px, py = py, px
        if not px in self.chunks:
            self.chunks[px] = {}
        if not py in self.chunks[px]:
            self.chunks[px][py] = GridChunk(np.array([[ -1 ]]), (self.delta[0] + py * SUBDIVISION_SIZE, self.delta[1] + px * SUBDIVISION_SIZE), self.atlas)
            self.chunks[px][py].gridlayer_mesh_id = len(self.meshes)
            self.meshes.append(self.chunks[px][py])
        self.chunks[px][py].modify(ix, iy, new_value)
        self.needsInit.append(self.meshes[self.chunks[px][py].gridlayer_mesh_id])

    def make_submap(self, dx, dy, delta, atlas):
        dx *= SUBDIVISION_SIZE
        dy *= SUBDIVISION_SIZE
        ex, ey = min(self.sx, dx + SUBDIVISION_SIZE), min(self.sy, dy + SUBDIVISION_SIZE)

        return GridChunk( self._map[dx:ex, dy:ey], (delta[0] + dx, delta[1] + dy), atlas )
    def __init__(self, _map, delta, atlas):
        self.atlas = atlas
        self.needsInit = []
        self._map = np.flip(np.rot90( np.array(_map) ))
        self.sx, self.sy = self._map.shape
        self.delta = delta

        ex, ey = ceil(self.sx / SUBDIVISION_SIZE), ceil(self.sy / SUBDIVISION_SIZE)
        self.chunks = {
            j: {
                i: self.make_submap(i, j, delta, atlas)
                for i in range(ex)
            }
            for j in range(ey)
        }
        self.meshes = []
        # for x in self.chunks:
        #     for i in self.chunks[x]:
        #         self.chunks[x][i].gridlayer_mesh_id = len(self.meshes)
        #         self.meshes.append(self.chunks[x][i])
    def createChunk (self, j, i, map):
        dx = j * SUBDIVISION_SIZE
        dy = i * SUBDIVISION_SIZE

        chunk = GridChunk(map, (dx + self.delta[0], dy + self.delta[1]), self.atlas)

        if i not in self.chunks: self.chunks[i] = {}
        self.chunks[i][j] = chunk

        self.chunks[i][j].gridlayer_mesh_id = len(self.meshes)
        self.meshes.append(chunk)
        self.needsInit.append(self.meshes[-1])

    def paintGL(self, shader, mModel, **kwargs):
        for mesh in self.needsInit:
            mesh.main_shader = self.main_shader
            mesh.initGL(self.widget, self.collisions)
        self.needsInit.clear()
        for mesh in self.meshes:
            mesh.main_shader = self.main_shader
            mesh.paintGL(shader, mModel, **kwargs)
    def initGL(self, widget, world_collision):
        self.collisions = world_collision
        self.widget     = widget
        for mesh in self.meshes:
            mesh.main_shader = self.main_shader
            mesh.initGL(widget, world_collision)
    def setVec3(self, color, value):
        for mesh in self.meshes:
            mesh.main_shader = self.main_shader
            mesh.setVec3(color, value)
    def save(self, buffer):
        for j in self.chunks:
            for i in self.chunks[j]:
                buffer.write(f"chunk-{i}/{j}:\n")
                self.chunks[j][i].save(buffer)

class GridChunk(Mesh):
    def padding_map (self):
        _map = np.ndarray((SUBDIVISION_SIZE, SUBDIVISION_SIZE), dtype=np.int32)

        for idx in range(SUBDIVISION_SIZE):
            for jdx in range(SUBDIVISION_SIZE):
                _map[idx][jdx] = -1
                if idx < self._map.shape[0] and jdx < self._map.shape[1]:
                    _map[idx][jdx] = self._map[idx][jdx]
        self._map = _map
    def __init__(self, _map, delta, atlas):
        super().__init__("<grid>")

        self._map = _map
        self.padding_map()

        self.delta = delta
        self.atlas = atlas
        ndx, ndy = delta

        self.vao  = [ 3, 2 ]
        self.vbos = [ [], [] ]
        self.rebuild_collision = True

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
    def modify(self, dx, dy, value):
        self.rebuild_collision = True
        self._map[dx][dy] = value
        self.vao  = [ 3, 2 ]
        self.vbos = [ [], [] ]
        ndx, ndy = self.delta

        w, h = self._map.shape
        for dx in range(w):
            for dy in range(h):
                if self._map[dx][dy] == -1: continue

                u = len(self.indices) // 6 * 4
                self.vbos[0].extend([ndx + dx, ndy + dy, 0, ndx + dx + 1, ndy + dy, 0, ndx + dx + 1, ndy + dy + 1, 0, ndx + dx, ndy + dy + 1, 0])
                for v in self.atlas.coordinates(self._map[dx][dy]): 
                    self.vbos[1].extend(v)

                self.indices.extend([u, u + 1, u + 2, u, u + 3, u + 2])
        self.vbos[0] = list(map(float, self.vbos[0]))
        self.vbos[1] = list(map(float, self.vbos[1]))
    def save(self, buffer):
        w, h = self._map.shape
        for dx in range(w):
            for dy in range(h):
                buffer.write(str(self._map[dy][dx]))
                buffer.write(" ")
            buffer.write("\n")
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

        line_index = 0
        while line_index < len(lines):
            line = lines[line_index]
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
            elif line.startswith("chunk-") and line[-1] == ':':
                if not isinstance(grid.meshes [state], GridLayer):
                    _map, _delta = grid.meshes[state]
                    grid.meshes[state] = GridLayer([[-1]], _delta, atlas)
                
                mesh = grid.meshes[state]

                j, i = list(map(int, line[6:-1].split("/")))
                
                chunk_map = []
                line_index += 1
                for delta in range(16):
                    words = lines[line_index].split(" ")
                    chunk_map.append([])
                    for word_id in range(16):
                        chunk_map[-1].append(int(words[word_id]))

                    line_index += 1
                
                chunk_map = np.rot90(np.flip(np.array(chunk_map), axis=1))
                line_index -= 1

                grid.meshes[state].createChunk(j, i, chunk_map)
            elif state == -2 and line.strip() != "":
                colliders.append(int(line))
            
            line_index += 1

        #for idx in range(len(grid.meshes)):
        #    grid.meshes [idx] = GridLayer(grid.meshes[idx][0], grid.meshes[idx][1], atlas)
        grid.colliders = colliders
        grid.__project = project
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
        self.__collision_manager = world_collision
        self.__collision_ids     = []

        for collider_id in self.colliders:
            world_collision.boxes.append(GridLayerHitBox(self.meshes[collider_id]))

    def modify(self, layer, x, y, new_value):
        self.meshes[layer].modify(x, y, new_value)
    def save (self):
        path = self._Mesh__path
        
        with open(path, "w") as write_buffer:
            write_buffer.write(f"atlas: {self.__project.unbuild_path(self.atlas.atlas_path)}\n")
            
            for idx, layer in enumerate(self.meshes):
                write_buffer.write(f"layer-{idx}:\n")
                write_buffer.write(f"dx: {layer.delta[0]}\ndy: {layer.delta[1]}\n")
            
                layer.save(write_buffer)
            
            write_buffer.write("collider:\n")
            for collider in self.colliders:
                write_buffer.write(f"{collider}\n")