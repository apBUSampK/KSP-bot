import sys
from PIL import Image
import vector

import camera
import obj

WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 1200


def main(argv):
    objects = [obj.Sphere(vector.obj(x=50, y=0, z=0), 10),
               obj.Torus(vector.obj(x=50, y=0, z=0), vector.obj(x=20, y=7)),
               obj.Sphere(vector.obj(x=40, y=10, z=20), .5, luminosity=50),
               obj.Sphere(vector.obj(x=30, y=-20, z=5), .5, luminosity=50),
               obj.Plane(vector.obj(x=0, y=0, z=1), -10)]
    output = Image.new('RGB', [WINDOW_WIDTH, WINDOW_HEIGHT])
    cam = camera.Camera(WINDOW_WIDTH, WINDOW_HEIGHT, objects, position=vector.obj(x=20, y=-30, z=15),
                        dir=vector.obj(x=25, y=35, z=-15))
    data = output.load()
    render_map = cam.mp_render()
    for iter in render_map:
        if iter is not None:
            data[iter[0], iter[1]] = tuple(iter[2])
    print("Rendering complete!")
    output.save(argv[0])


if __name__ == '__main__':
    main(sys.argv[1:])
