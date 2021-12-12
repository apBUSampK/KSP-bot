import sys
import tkinter
import vector
import camera
import obj

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 300


def main(argv):
    objects = [obj.Sphere(vector.obj(x=50, y=0, z=0), 10)]
    window = tkinter.Tk()
    cam = camera.Camera(WINDOW_WIDTH, WINDOW_HEIGHT, objects)
    canv = tkinter.Canvas(window, background='black', width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
    canv.pack()
    if argv is None:
        render_map = cam.render()
    else:
        if argv[0] == '-m':
            render_map = cam.mp_render()
        elif argv[0] == '-s':
            render_map = cam.render()
    for iter in render_map:
        if iter[2]:
            canv.create_rectangle(iter[0], iter[1], iter[0], iter[1], outline='white')
    canv.update()
    print("Rendering complete!")
    window.mainloop()


if __name__ == '__main__':
    main(sys.argv[1:])
