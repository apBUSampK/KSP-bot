import vector
import numpy as np


class Sphere:
    def __init__(self, pos: vector.VectorObject3D, r, scale=1, delete=False, luminosity=None):
        self.pos = pos
        self.r = r
        self.scale = scale
        self.delete = delete
        self.luminosity = luminosity

    def dist(self, point: vector.VectorObject3D):
        return self.scale * (abs(self.pos - point) - self.r)

class Parallelepiped:
    def __init__(self, pos: vector.VectorObject3D, a = vector.VectorObject3D, b = vector.VectorObject3D, c = vector.VectorObject3D, scale = 1, delete = False, luminosity = None):
        self.pos = pos
        self.a = a
        self.b = b
        self.c = c
        self.scale = scale
        self.delete = delete
        self.luminosity = luminosity
        
    def dist(self, point: vector.VectorObject3D):
        q = abs(point) - self.pos
        return self.scale * length(max(q,0.0)) + min(max(q.x,max(q.y,q.z)),0.0);

class plane:
    def __init__ (self, r = vector.VectorObject3D, n = vector.VectorObject3D, scale = 1, delete = False, luminosity = None):
        self.r = r
        self.n = n
        self.scale = scale
        self.delete = delete
        self.luminosity = luminosity
        
# vector r лежит в плоскости ху; vector n паралеллен оси z
    def dist(self, point: vector.VectorObject3D):
        return abs((np.dot(point, self.n))/abs(self.n))
