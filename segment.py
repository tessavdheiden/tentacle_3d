import numpy as np
import math
from pyglet.gl import *
from gym.envs.classic_control.rendering import Line


class Segment(Line):
    def __init__(self, x, y, z, length):
        super(Segment, self).__init__()
        self.start = np.array([x, y, z])
        self.length = length
        self.theta = 0
        self.phi = 0
        self.calc_end(self.theta, self.phi, self.start)

    def calc_end(self, angle_xy, angle_xz, start):
        x, y, z = start
        self.end = (x - self.length * math.cos(angle_xy), y - self.length * math.sin(angle_xy), z - self.length * math.sin(angle_xz))

    def set_start(self, start):
        self.start = start
        self.calc_end(self.theta, self.phi, self.start)

    def follow(self, tx, ty, tz):
        target = np.array([tx, ty, tz])
        dir = self.start - target
        distance = np.sqrt(np.square(dir).sum())
        rev_theta = np.arctan2(dir[1], dir[0])
        rev_phi = np.arcsin(dir[2] / distance)
        self.start = target + np.array([self.length * math.cos(rev_theta), self.length * math.sin(rev_theta), self.length * math.sin(rev_phi)])
        self.calc_end(rev_theta, rev_phi, self.start)
        self.theta = rev_theta
        self.phi = rev_phi

    def render1(self):
        glBegin(GL_LINES)
        glVertex3f(*self.start)
        glVertex3f(*self.end)
        glEnd()