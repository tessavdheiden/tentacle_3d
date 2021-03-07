from segment import Segment


class Tentacle(object):
    def __init__(self, x, y, z):
        self.n = 20
        self.segments = [None]*self.n
        self.L = .5
        self.length = self.L / self.n
        self.base = (x, y, z)
        base = self.base
        for i in range(self.n):
            self.segments[i] = Segment(*base, self.length)
            base = self.segments[i].end