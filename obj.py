import vector


class Sphere:
    def __init__(self, pos: vector.VectorObject3D, r, scale=1, delete=False):
        self.pos = pos
        self.r = r
        self.scale = scale
        self.delete = delete

    def dist(self, point: vector.VectorObject3D):
        return self.scale * (abs(self.pos - point) - self.r)
