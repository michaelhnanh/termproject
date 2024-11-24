# code for terrain generation + storage + drawing
# would probably return a set of 

from cmu_graphics import *
from tools import *
import math, random

class Terrain:
    xray = []
    lineSplit = 100
    segment = 1 / lineSplit

    def __init__(self, p1, p2, p3, p4):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.pointList = []
        self.controlList = [] # 2d list containing lists of control points

    @staticmethod
    def cubicBezier(p1, p2, p3, p4, t):
        thirdX =      ((1 - t) ** 3) * p1.x 
        thirdY =      ((1 - t) ** 3) * p1.y

        secondX = 3 * ((1 - t) ** 2) * t * p2.x
        secondY = 3 * ((1 - t) ** 2) * t * p2.y

        firstX =  3 * ((1 - t)     ) * (t ** 2) * p3.x
        firstY =  3 * ((1 - t)     ) * (t ** 2) * p3.y

        zeroX =                        (t ** 3) * p4.x
        zeroY =                        (t ** 3) * p4.y

        return ((thirdX + secondX + firstX + zeroX), (thirdY + secondY + firstY + zeroY))

    @staticmethod
    def cubicTangent(p1, p2, p3, p4, t):
        p1x = (-3 * ((1 - t) ** 2) * p1.x)
        p2x = ((3 * ((1 - t) ** 2)) * p2.x) - ((6 * t * (1 - t)) * p2.x)
        p3x = ((6 * t * (1 - t)) * p3.x) - ((3 * t ** 2) * p3.x)
        p4x = (3 * (t ** 2) * p4.x)

        p1y = (-3 * ((1 - t) ** 2) * p1.y)
        p2y = ((3 * ((1 - t) ** 2)) * p2.y) - ((6 * t * (1 - t)) * p2.y)
        p3y = ((6 * t * (1 - t)) * p3.y) - ((3 * t ** 2) * p3.y)
        p4y = (3 * (t ** 2) * p4.y)

        return ((p1x + p2x + p3x + p4x), (p1y + p2y + p3y + p4y))

    @staticmethod
    def genCurve(p1, p2, p3, p4):
        curve = []
        for t in range(0, 1 + Terrain.segment, Terrain.segment):
            x, y = Point.cubicBezier(p1, p2, p3, p4, t)
            curve.append(x)
            curve.append(y)
        return curve
    
    # calculate c1 continuity with the previous curve and returns a control point for joined curve
    @staticmethod
    def c1(p3, p4):
        vectorX = p4.x - p3.x
        vectorY = p4.y - p3.y
        p5 = Point(p3.x + vectorX * 2, p3.y * vectorY * 2)
        return p5

    # c2 continuity - may not be used - returns 2 control points
    @staticmethod
    def c2(p2, p3, p4):
        vectorX = p4.x - p3.x
        vectorY = p4.y - p3.y
        p5 = Point(p3.x + vectorX * 2, p3.y * vectorY * 2)
        p6 = Point(p2.x + vectorX * 4, p2.y * vectorY * 4)
        return p5, p6
    
    # decides if the next curve should be c0 or c1 continuous
    @staticmethod
    def continuousRand(p4, p5):
        # should weight c0 much less than c1 
        # --> should although should have c0 to allow for platforms to be reached
        # beginning of game should not have much c0s
        # c0 should require the tangent of p41 to be upward sloping (or negative, in this instance)
        if p4.y > p5.y:
            continuity = random.randrange(1, 20)
            if continuity == 13: return 0
            else: return 1
        else:
            return 1

    # generate new curve 3 when curve 1 is passed --> curve 2 is kept in memory
    # has to generate two curves at the start of a run
    @staticmethod
    def controlPointGenerator(p31, p41, width):
        # takes in p21, p31, p41 as the new p12 is determined by p41 of the last curve - p(point #, curve #)
        # may be using p31 and possibly p21 depending on continuity
        # p12 = p41

        # some formula to allow for a wider normal distribution
        totalLength = width * normalScalar() * 3

        # can determine p22, p32, p42 using an angle instead of just a x and y scalar - more control
        continuity = Terrain.continuousRand(p41, p22)
        if continuity == 0:
            lengthp22 = totalLength / 3 * normalScalar()
            anglep22 = math.radians(random.randrange(270, 315, 1))
            p22 = Point(p41.x + lengthp22 * math.cos(anglep22), 
                        p41.y + lengthp22 * math.sin(anglep22))
        elif continuity == 1:
            p22 = Terrain.c1(p31, p41)

        # limit slope between 6 - 70 degrees
        anglep42 = math.radians(normalRandom(290, 354, 1))
        # p32 can be below or above p42, controlling whether or not the curve will flick up or down
        anglep32 = math.radians(normalRandom(135, 225, 1)) # --> angle from p42

        p42 = Point(p41.x + totalLength * math.cos(anglep42), p41.y + totalLength * math.sin(anglep42))
        lengthp32 = totalLength / 3 * normalScalar()
        p32 = Point(p42.x + lengthp32 * math.cos(anglep32), p42.y + lengthp32 * math.cos(anglep32))

        return p41, p22, p32, p42
        
def normalScalar():
    return ((random.random() - random.random() + 1)/2)//0.001 # truncate it as more accuracy is not important

def normalRandom(min, max, step = 1):
    center = min + max
    return (random.randrange(min, max, step) - random.randrange(min, max, step) + center)/2


    

    
