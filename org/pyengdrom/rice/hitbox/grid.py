

from org.pyengdrom.rice.hitbox.box import CubeHitBox


class GridLayerHitBox:
    def __init__(self, layer):
        self.layer = layer
    def _collide_cube(self, box):
        for mesh in self.layer.meshes:
            for mesh_box in mesh.boxes:
                if mesh_box.collide(box):
                    return True
        return False
    def rebuild_collision(self, mesh):
        _map = mesh.vbos[0]
        mesh.boxes = []
                
        for _pid in range(0, len(_map), 12):
            min_point = _map[_pid], _map[_pid + 1], -100
            _pid += 6
            max_point = _map[_pid], _map[_pid + 1], 100

            mesh.boxes.append(CubeHitBox(min_point, max_point))
    def rebuild_all(self):
        for mesh in self.layer.meshes:
            if mesh.rebuild_collision:
                self.rebuild_collision(mesh)
                mesh.rebuild_collision = False
    def collide(self, box):
        self.rebuild_all()
        if isinstance(box, CubeHitBox): return self._collide_cube(box)

        return False 
