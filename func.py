from vector import *

Ox = obj(x=1, y=0, z=0)
Oy = obj(x=0, y=1, z=0)
Oz = obj(x=0, y=0, z=1)


def get_normal(vec: VectorObject3D):
    """
    Get the normalized vector

    :param vec: input vector
    :return: VectorObject3D: normalized input vector
    """
    if abs(vec):
        return vec / abs(vec)
    else:
        return vec


def dist(point: VectorObject3D, catalogue, index=False):
    """
    A function for calculating the distance field

    :param point: The point in space
    :param catalogue: list of objects in the scene
    :param index: whether the function will return the index of the closest body
    :return: float: the minimal distance; int:
    """
    arr = [i.dist(point) for i in catalogue]
    if index:
        return min(arr), arr.index(min(arr))
    else:
        return min(arr)


def get_normal_obj(point: VectorObject3D, catalogue):
    """
    A function for calculating normal vector to ANY object at a given point
    Based on the idea of approximation by gradient of distance field at the point.
    
    :param point: Тhe (intersection) point
    :param catalogue: list of objects in the scene
    :return: VectorObject3D: normal vector
    """
    eps = .001
    point_dist = dist(point, catalogue)
    return get_normal(obj(x=dist(point + Ox*eps, catalogue) - point_dist,
                          y=dist(point + Oy*eps, catalogue) - point_dist,
                          z=dist(point + Oz*eps, catalogue) - point_dist))