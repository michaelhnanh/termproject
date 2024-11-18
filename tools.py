import math
from cmu_graphics import *

class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def display(self, radius, color = 'black'):
        drawCircle(self.x, self.y, radius, fill = color)


def subtract(point1, point2):
    newpoint = point(point1.x - point2.x, point1.y - point2.y)
    return newpoint

def dot(point1, point2):
    return ((point1.x * point2.x) + (point1.y * point2.y))

def clamp(value, upperbound, lowerbound):
    return 