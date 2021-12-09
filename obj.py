import vector


class Sphere:
    def __init__(self, pos: VectorObject3D, r, scale=1, del=False):
        self.pos = pos
        self.r = r
        self.scale = scale
        self.del = del

    def dist(self, point: VectorObjeect3D):
        return scale * abs(self.pos - point)
