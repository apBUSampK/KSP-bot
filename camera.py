import tkinter

import numpy
import vector

ROT_SPEED = .1
MOV_SPEED = 10
ITERATIONS = 50
MAX_DIST = 1000
Ox = vector.obj(x=1, y=0, z=0)
Oy = vector.obj(x=0, y=1, z=0)
Oz = vector.obj(x=0, y=0, z=1)


class Camera(tkinter.Canvas):

    """
    Класс камеры. Наследует виджет-класс Canvas модуля Tkinter. Метод update() перегружен для отрисовки сцены.
    Метод renderer() производит попиксельную отрисовку рейкастом с алгоритмом реймаршинга
    Перемещение камеры по сцене - WASD + LShift и LAlt для вертикального смещения
    Поворот камеры - стрелки клавиатуры (крен не предусмотрен)
    """

    def __init__(self, master: tkinter.Tk, catalogue, width, height, fov_h=90, position=vector.obj(x=0, y=0, z=0)):
        super().__init__(master, height=height, width=width, bg="black")
        self.height = height
        self.width = width
        self.fov_h = fov_h / 180 * numpy.pi
        self.fov_v = fov_h / width * height
        self.pos = position
        self.dir = Ox
        self.left = Oy
        self.up = Oz
        self.catalogue = catalogue
        self.theta = self.phi = 0
        self.forward = self.sideways = self.upwards = 0
        self.bind('<KeyPress-Left>', self._chphi(-ROT_SPEED))
        self.bind('<KeyRelease-Left>', self._chphi(ROT_SPEED))
        self.bind('<KeyPress-Right>', self._chphi(ROT_SPEED))
        self.bind('<KeyRelease-Right>', self._chphi(-ROT_SPEED))
        self.bind('<KeyPress-Up>', self._chtheta(-ROT_SPEED))
        self.bind('<KeyRelease-Up>', self._chtheta(ROT_SPEED))
        self.bind('<KeyPress-Down>', self._chtheta(ROT_SPEED))
        self.bind('<KeyRelease-Down>', self._chtheta(-ROT_SPEED))
        self.bind('<KeyPress-w>', self._chfwd(1))
        self.bind('<KeyRelease-w>', self._chfwd(-1))
        self.bind('<KeyPress-s>', self._chfwd(-1))
        self.bind('<KeyRelease-s>', self._chfwd(1))
        self.bind('<KeyPress-a>', self._chsdw(1))
        self.bind('<KeyRelease-a>', self._chsdw(-1))
        self.bind('<KeyPress-d>', self._chsdw(-1))
        self.bind('<KeyRelease-d>', self._chsdw(1))
        self.bind('<KeyPress-Shift_L>', self._chup(1))
        self.bind('<KeyRelease-Shift_L>', self._chup(-1))
        self.bind('<KeyPress-Alt_L>', self._chup(-1))
        self.bind('<KeyRelease-Alt_L>', self._chup(1))

    def _chtheta(self, val):
        self.theta += val

    def _chphi(self, val):
        self.phi += val

    def _chfwd(self, val):
        self.forward += val

    def _chsdw(self, val):
        self.sideways += val

    def _chup(self, val):
        self.upwards += val

    def renderer(self):
        for i in range(self.width):
            for j in range(self.height):
                ray_pos = self.pos
                ray_dir = self.dir.rotate_axis(self.up, self.fov_h * (self.width/2 - i/self.width)).\
                    rotate_axis(self.left, self.fov_v * (self.height/2 - i/self.width))
                for iter in range(ITERATIONS):
                    if abs(ray_pos - self.pos) > MAX_DIST:
                        break
                    dist = min([i.dist(ray_pos) for i in self.catalogue])
                    if dist <= 0:
                        bright = int(255 * iter / ITERATIONS)
                        self.create_rectangle(i, j, i, j, outline="#{:x}{:x}{:x}".format(bright, bright, bright))
                        break
                    else:
                        ray_pos += ray_dir * dist

    def update(self):
        speed = self.dir * self.forward + self.left * self.sideways + self.up * self.upwards
        speed = speed * MOV_SPEED / abs(speed)
        self.pos += speed
        self.dir.rotate_axis(self.up, self.phi)
        self.left.rotate_axis(self.up, self.phi)
        self.dir.rotate_axis(self.left, self.theta)
        self.up.rotate_axis(self.left, self.theta)
        self.renderer()
        super().update()
