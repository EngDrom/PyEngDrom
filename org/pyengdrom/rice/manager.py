
import numpy as np

class Force:
    def __init__(self, x, y, z):
        self.f = np.array([x, y, z])

class Weight(Force):
    def __init__(self, mass):
        super().__init__(0, - 16 * mass, 0)


MOVEMODE_Component = 1
MOVEMODE_Bijection = 2

class Proxy:
    def __init__(self, mesh, mass, move_mode, manager : "WorldCollisionManager"):
        self.mesh = mesh
        self._mass = mass
        self.manager = manager
        self.move_mode = move_mode

    def move(self, x, y, z):
        self.mesh.move(x, y, z)
        box = self.mesh.compute_hitbox()

        if self.manager.collides(box):
            self.mesh.move(-x, -y, -z)
            if MOVEMODE_Component & self.move_mode != 0 \
                and not (x == y == 0 or x == z == 0 or y == z == 0):
                self.move(x, 0, 0)
                self.move(0, y, 0)
                self.move(0, 0, z)
            elif MOVEMODE_Bijection & self.move_mode != 0:
                self.move_bijection(x, y, z)
            return True
        return False
    def move_bijection(self, x, y, z):
        a = 0
        b = 1

        for i in range(8):
            m = (a + b) / 2
            self.mesh.move(x * m, y * m, z * m)

            box = self.mesh.compute_hitbox()

            if self.manager.collides(box):
                b = m
            else: a = m

            self.mesh.move(- x * m, - y * m, - z * m)
        
        self.mesh.move(x * a, y * a, z * a)
    def mass(self):
        return self._mass

class Manager:
    def __init__(self, proxy) -> None:
        self.proxy = proxy
        self.speed = np.array([0.0, 0.0, 0.0])
        self._forces = [Weight(self.proxy.mass())]
        self.forces = []
    def get_acceleration(self):
        acc = np.array([0.0, 0.0, 0.0])
        for f in self.forces:
            acc = acc + f.f
        for f in self._forces:
            acc = acc + f.f
        return acc / self.proxy.mass()
    def frame(self, delta_t):
        dv = self.get_acceleration() * delta_t
        self.forces.clear()

        self.speed += dv
        if self.proxy.move(*(self.speed * delta_t)):
            self.speed[::] = 0.0

class WorldCollisionManager:
    def __init__(self):
        self.boxes = []
    def collides(self, box):
        for _box in self.boxes:
            if box.collide(_box):
                return True
        
        return False

def run_calculation(managers, time):
    for manager in managers:
        manager.frame(time)
