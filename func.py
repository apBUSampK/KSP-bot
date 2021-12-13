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


def phong_calc(point: VectorObject3D, light_vector: VectorObject3D, viewer_vector: VectorObject3D, catalogue,
               color_Diffuse=(255, 255, 255), color_Specular=(130, 130, 130), color_Ambient=(105, 105, 105), alpha=4):
    """
    A function for calculating pixel brightness based on the Phong shading model

    :param point: The (intersection) point
    :param light_vector: The vector pointing from the intersection point to the light source
    :param viewer_vector: normalized vector that is antiparallel to the ray direction vector
    :param catalogue: list of objects in the scene
    :param color_Diffuse: color for Diffuse component
    :param color_Specular: color for Specular component
    :param alpha: exponent constant
    :return: tuple(int, int, int): unweighted rgb pixel color
    """
    norm = get_normal_obj(point, catalogue)
    return [color_Ambient[i] + color_Diffuse[i] * get_normal(light_vector).dot(norm) + color_Specular[i] * viewer_vector.\
            dot(2*norm.dot(get_normal(light_vector)) * norm - get_normal(light_vector))**alpha for i in range(3)]


def phong_normalize(render_map):
    """
    Color normalization function

    :param render_map: input render_map
    :return: scaled render_map
    """
    max_color = 0
    for i in render_map:
        if i is not None:
            for j in i[2]:
                if j > max_color:
                    max_color = j
    for i in range(len(render_map)):
        if render_map[i] is not None:
            for j in range(3):
                render_map[i][2][j] = int(render_map[i][2][j] / max_color * 255)
                if render_map[i][2][j] < 0:
                    render_map[i][2][j] = 0
    return render_map
