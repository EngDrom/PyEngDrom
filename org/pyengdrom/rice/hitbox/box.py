

class HitBox:
    def __init__(self): pass
    def collide (self, box: "HitBox"): return False

class CubeHitBox:
    def __init__(self, p0, p1):
        self.p0 = p0
        self.p1 = p1

    def __in__(self, point):
        for x in range(3): 
            if not (self.p0[x] <= point[x] <= self.p1[x]):
                return False
        
        return True
    def points(self):
        if hasattr(self, "_points"): return self._points
        points = []

        p = [self.p0, self.p1]
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    points.append([p[i][0], p[j][1], p[k][2]])

        self._points = points
        return points
    def _collide_cube(self, box: "CubeHitBox"):
        for p in self.points(): 
            if box.__in__(p): return True
        for p in box.points(): 
            if self.__in__(p): return True
        return False
    def __str__(self):
        return str(self.p0) + " " + str(self.p1)
    def collide(self, box: "HitBox"):
        if isinstance(box, CubeHitBox): return self._collide_cube(box)

        return False

class NoHitBox(HitBox):
    def __init__(self): pass
    def collide(self, box: "HitBox"): return False