#character code --> austin himself

from cmu_graphics import *
import math

class Character:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.orientation = 0
        self.grounded = True
        self.rotating = False
        self.platformed = False

        self.vert = 50
        self.rot = 2

    def jump(self):
        pass

    def rotate(self):
        pass

    def drop(self):
        pass

    def reCenter(self):
        pass