from copy import deepcopy
from progress.bar import ChargingBar
from progress.spinner import Spinner
from multiprocessing import Pool

import vector
from numpy import pi, tan

ROT_SPEED = .1
MOV_SPEED = 10
ITERATIONS = 200
MAX_DIST = 200
Ox = vector.obj(x=1, y=0, z=0)
Oy = vector.obj(x=0, y=1, z=0)
Oz = vector.obj(x=0, y=0, z=1)


class Camera():

    """
    Класс камеры.
    Метод render_pixel() производит попиксельную отрисовку рейкастом с алгоритмом реймаршинга
    """

    def __init__(self, width, height, catalogue, fov=90, position=vector.obj(x=0, y=0, z=0)):
        self.height = height
        self.width = width
        fov_h = fov / 360 * pi
        self.scale_x = tan(fov_h)
        self.scale_y = self.scale_x / width * height
        self.pos = position
        self.dir = Ox
        self.left = Oy
        self.up = Oz
        self.catalogue = catalogue

    def render_pixel(self, i, j, spinner=None):
        ray_pos = deepcopy(self.pos)
        ray_dir = self.dir + self.left * (self.width - 2*i) / self.width * self.scale_x +\
            self.up * (self.height - 2*j) / self.height * self.scale_y
        ray_dir /= abs(ray_dir)
        for iter in range(ITERATIONS):
            if abs(ray_pos - self.pos) > MAX_DIST:
                if spinner is not None:
                    spinner.next()
                return i, j, False
            dist = min([i.dist(ray_pos) for i in self.catalogue])
            if dist <= 0:
                break
            else:
                ray_pos += ray_dir * dist
        if spinner is not None:
            spinner.next()
        return i, j, True

    def mp_render(self):
        with Pool() as p:
            spinner = Spinner("Rendering")
            args = [(i, j, spinner) for i in range(self.width) for j in range(self.height)]
            render_map = p.starmap(self.render_pixel, args)
            spinner.finish()
            return render_map

    def render(self):
        bar = ChargingBar('Rendering', max=self.width * self.height)
        render_map = []
        for i in range(self.width):
            for j in range(self.height):
                render_map.append(self.render_pixel(i, j))
                bar.next()
        bar.finish()
