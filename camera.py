from copy import deepcopy
from progress.bar import ChargingBar
from progress.spinner import Spinner
from multiprocessing import Pool

import vector
from numpy import pi, tan
from func import *

ROT_SPEED = .1
MOV_SPEED = 10
ITERATIONS = 200
MAX_DIST = 200
TOLERANCE = .001
Ox = vector.obj(x=1, y=0, z=0)
Oy = vector.obj(x=0, y=1, z=0)
Oz = vector.obj(x=0, y=0, z=1)


class Camera():

    """
    Класс камеры.
    Метод renderer() производит попиксельную отрисовку рейкастом с алгоритмом реймаршинга
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
        ray_dir_norm = get_normal(self.dir + self.left * (self.width - 2*i) / self.width * self.scale_x +\
                                  self.up * (self.height - 2*j) / self.height * self.scale_y)
        ray_dir = ray_dir_norm
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
            return [i, j, 1]
        else:
            brightness = 0
            for iter in self.light_src:
                light_vec = get_normal(iter.pos - ray_pos)
                brightness += light_vec.dot(get_normal_obj(ray_pos, self.catalogue))
            return [i, j, brightness]

    def mp_render(self):
        with Pool() as p:
            spinner = Spinner("Rendering")
            args = [(i, j, spinner) for i in range(self.width) for j in range(self.height)]
            render_map = p.starmap(self.render_pixel, args)
            spinner.finish()
        #scene_max_brightness = max([iter[2] for iter in render_map])
        for iter in render_map:
            if iter is not None:
                render_map[render_map.index(iter)][2] = int(iter[2] * 130 + 125)
        return render_map

    def render(self):
        bar = ChargingBar('Rendering', max=self.width * self.height)
        render_map = []
        for i in range(self.width):
            for j in range(self.height):
                render_map.append(self.render_pixel(i, j))
                bar.next()
        bar.finish()
        #scene_max_brightness = max([iter[2] for iter in render_map])
        for iter in render_map:
            if iter[2]:
                render_map[render_map.index(iter)][2] = int(iter[2] * 130 + 125)
        return render_map
