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
    def __init__(self, pos: vector.VectorObject3D, R: vector.VectorObject3D, scale = 1, delete = False, luminosity = None):
        self.pos = pos
        self.R = R
        self.scale = scale
        self.delete = delete
        self.luminosity = luminosity

           
    def dist(self, point: vector.VectorObject3D):
        s = vector.obj(x = abs( (point - self.pos).x), y = abs( (point - self.pos).y), z = abs( (point - self.pos).z) ) 
        q = s - self.R
        return self.scale * (  (  (max(q.x, 0))^2 + (max(q.y, 0))^2 + (max(q.z, 0))^2  )^0.5   + min(max (q.x, max(q.y , q.z ) ), 0 ) )


class Plane:
    def __init__(self, n: vector.VectorObject3D, z, delete=False, luminosity=None):
        self.n = n
        self.z = z
        self.delete = delete
        self.luminosity = luminosity

    def dist(self, point: vector.VectorObject3D):
        return point.dot(self.n)/abs(self.n) - self.z


class Torus:
    def __init__(self, pos: vector.VectorObject3D, t: vector.VectorObject2D, scale = 1, delete = False, luminosity = None):
        self.pos = pos
        self.t = t 
        self.scale = scale
        self.delete = delete
        self.luminosity = luminosity
        
    def dist(self, point: vector.VectorObject3D):
        s = vector.obj(x =  (point - self.pos).x, y = (point - self.pos).y, z = (point - self.pos).z ) 
        w = vector.obj(x =  s.x, y = 0, z = s.z )
        q = vector.obj(x = abs(w) - self.t.x, y = s.y )
        return self.scale * (abs(q) - self.t.y)
