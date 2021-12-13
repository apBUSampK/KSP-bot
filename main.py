import sys
from PIL import Image
import vector

import camera
import obj

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 300


def main(argv):
    objects = [obj.Sphere(vector.obj(x=50, y=0, z=0), 10),
               obj.Sphere(vector.obj(x=40, y=10, z=20), .5, luminosity=50),
               obj.Plane(vector.obj(x=0, y=0, z=1), -10)]
    output = Image.new('RGB', [WINDOW_WIDTH, WINDOW_HEIGHT])
    cam = camera.Camera(WINDOW_WIDTH, WINDOW_HEIGHT, objects)
    data = output.load()
    render_map = cam.mp_render()
    for iter in render_map:
        if iter is not None:
            data[iter[0], iter[1]] = tuple(iter[2])
    print("Rendering complete!")
    output.save('output.png')


if __name__ == '__main__':
    main(sys.argv[1:])
