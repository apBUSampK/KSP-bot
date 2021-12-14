from copy import deepcopy
from progress.spinner import Spinner
from multiprocessing import Pool

import vector
from numpy import pi, tan
from func import *

ROT_SPEED = .1
MOV_SPEED = 10
ITERATIONS = 20
MAX_DIST = 500
TOLERANCE = .001
Ox = vector.obj(x=1, y=0, z=0)
Oy = vector.obj(x=0, y=1, z=0)
Oz = vector.obj(x=0, y=0, z=1)


class Camera():

    """
    Класс камеры.
    Метод render_pixel() производит попиксельную отрисовку рейкастом с алгоритмом реймаршинга
    """

    def __init__(self, width, height, catalogue, fov=90, position=vector.obj(x=0, y=0, z=0), dir=Ox):
        self.height = height
        self.width = width
        fov_h = fov / 360 * pi
        self.scale_x = tan(fov_h)
        self.scale_y = self.scale_x / width * height
        self.pos = position
        self.dir = get_normal(dir)
        self.left = get_normal(Oz.cross(dir))
        self.up = self.dir.cross(self.left)
        self.catalogue = catalogue
        self.light_src = [i for i in catalogue if i.luminosity is not None]

    def render_pixel(self, i, j, spinner=None):
        ray_pos = deepcopy(self.pos)
        ray_dir = get_normal(self.dir + self.left * (self.width - 2*i) / self.width * self.scale_x +
                             self.up * (self.height - 2*j) / self.height * self.scale_y)
        for iter in range(ITERATIONS):
            if abs(ray_pos - self.pos) > MAX_DIST:
                if spinner is not None:
                    spinner.next()
                return None
            min_dist = dist(ray_pos, self.catalogue, index=True)
            if min_dist[0] <= TOLERANCE:
                break
            else:
                ray_pos += ray_dir * min_dist[0]
        if spinner is not None:
            spinner.next()
        if self.catalogue[min_dist[1]].luminosity is not None:
            return [i, j, [1.6 * len(self.light_src), 1.6 * len(self.light_src), 1.6 * len(self.light_src)]]
        else:
            brightness = .6 * len(self.light_src)
            for iter in self.light_src:
                light_vec = get_normal(iter.pos - ray_pos)
                brightness += light_vec.dot(get_normal_obj(ray_pos, self.catalogue))
            return [i, j, [brightness, brightness, brightness]]

    def mp_render(self):
        with Pool() as p:
            spinner = Spinner("Rendering")
            args = [(i, j, spinner) for i in range(self.width) for j in range(self.height)]
            render_map = p.starmap(self.render_pixel, args)
            spinner.finish()
        return phong_normalize(render_map)