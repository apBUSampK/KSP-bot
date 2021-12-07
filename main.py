import tkinter
import camera

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 300

if __name__ == '__main__':
    objects = []
    window = tkinter.Tk()
    cam = camera.Camera(window, objects, WINDOW_WIDTH, WINDOW_HEIGHT)
    cam.pack()
    while True:
        cam.update()
