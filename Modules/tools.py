import math
from cmu_graphics import *

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def display(self, radius, color = 'black'):
        drawCircle(self.x, self.y, radius, fill = color)

    def __add__(self, point2):
        newpoint = Point(self.x + point2.x, self.y + point2.y)
        return newpoint

    def __sub__(self, point2):
        newpoint = Point(self.x - point2.x, self.y - point2.y)
        return newpoint
    
    def __mul__(self, point2):
        newpoint = Point(self.x * point2.x, self.y * point2.y)
        return newpoint
    
    def __eq__(self, point2):
        return (self.x == point2.x) and (self.y == point2.y)

    def __repr__(self):
        return f'({self.x}, {self.y})'
    
    def dot(point1, point2):
        return ((point1.x * point2.x) + (point1.y * point2.y))

    def clamp(value, upperbound, lowerbound):
        return 
    