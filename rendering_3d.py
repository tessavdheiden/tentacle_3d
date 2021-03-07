import numpy as np
import pyglet
from pyglet.gl import *
from gym.envs.classic_control.rendering import Viewer, Geom, Transform, LineWidth, RAD2DEG


class Viewer3D(Viewer):
    def __init__(self, h, w):
        super(Viewer3D, self).__init__(h, w)
        self.x = [.5, -.5, .5]

    def render(self, return_rgb_array=False):
        glClearColor(1,1,1,1)
        self.window.clear()
        self.window.switch_to()
        self.window.dispatch_events()

        self.transform.enable()

        gluLookAt(*self.x,
                  0, 0, 0,
                  0, 1, 0)
        glPushMatrix()
        for geom in self.geoms:
            geom.render()
        for geom in self.onetime_geoms:
            geom.render()
        self.transform.disable()
        arr = None
        if return_rgb_array:
            buffer = pyglet.image.get_buffer_manager().get_color_buffer()
            image_data = buffer.get_image_data()
            arr = np.frombuffer(image_data.get_data(), dtype=np.uint8)
            # In https://github.com/openai/gym-http-api/issues/2, we
            # discovered that someone using Xmonad on Arch was having
            # a window of size 598 x 398, though a 600 x 400 window
            # was requested. (Guess Xmonad was preserving a pixel for
            # the boundary.) So we use the buffer height/width rather
            # than the requested one.
            arr = arr.reshape(buffer.height, buffer.width, 4)
            arr = arr[::-1, :, 0:3]

        self.window.flip()
        self.onetime_geoms = []
        glPopMatrix()
        return arr if return_rgb_array else self.isopen


class Line3D(Geom):
    def __init__(self, start=(0.0, 0.0, 0.0), end=(0.0, 0.0, 0.0)):
        Geom.__init__(self)
        self.start = start
        self.end = end
        self.linewidth = LineWidth(3)
        self.add_attr(self.linewidth)

    def render1(self):
        glBegin(GL_LINES)
        glVertex3f(*self.start)
        glVertex3f(*self.end)
        glEnd()


class Point3D(Geom):
    def __init__(self, p=(0.0, 0.0, 0.0)):
        Geom.__init__(self)
        self.p = p
    def render1(self):
        glPointSize(5.)
        glBegin(GL_POINTS) # draw point
        glVertex3f(*self.p)
        glEnd()


class Transform3D(Transform):
    def __init__(self, translation=(0.0, 0.0, 0.0), rotation=0.0, scale=(1,1)):
        super(Transform3D, self).__init__(translation, rotation, scale)
    def enable(self):
        glPushMatrix()
        glTranslatef(self.translation[0], self.translation[1], self.translation[2]) # translate to GL loc ppint
        glRotatef(RAD2DEG * self.rotation, 0, 0, 1.0)
        glScalef(self.scale[0], self.scale[1], 1)
    def set_translation(self, newx, newy, newz):
        self.translation = (float(newx), float(newy), float(newz))


def make_axes():
    xaxis = Line3D(end=(.1, 0, 0))
    xaxis.set_color(1., 0, 0)
    yaxis = Line3D(end=(0, .1, 0))
    yaxis.set_color(0., 1., 0)
    zaxis = Line3D(end=(0, 0, .1))
    zaxis.set_color(0., 0., 1)
    return [xaxis, yaxis, zaxis]

