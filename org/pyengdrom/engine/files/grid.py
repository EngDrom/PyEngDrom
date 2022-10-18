
import numpy as np
from org.pyengdrom.engine.files.mesh import Mesh

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
        print(self.vbos)
        print(self.indices)

class Grid:
    def __init__(self, atlas):
        self.atlas = atlas
        self.meshes = [
            GridChunk(
                 [[-1, -1, 7 * 7, -1, -1, -1, -1], [-1, 8, 7, 7, 7, 15, -1], [12, 22, 1, 29, 29, 36, 12], [13, 22, 29, 29, 3, 36, 13]], atlas
                # [[0, 7, 14], [1, 8, 15], [2, 9, 16]], atlas
            )
        ]

