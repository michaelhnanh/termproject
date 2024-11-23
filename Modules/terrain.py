# code for terrain generation + storage + drawing
# would probably return a set of 

from cmu_graphics import *
from tools import *
import math, random

class Terrain:
    curveList = []
    xray = []
    lineSplit = 100
    segment = 1 / lineSplit

    def __init__(self, ):
        self.p1 = 0
        p1, p2, p3, p4 = 0

    @staticmethod
    def cubicBezier(p1, p2, p3, p4, t, funkyMode = False):
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
            continuity = random.random()
            if continuity > 0.95: return 0
            else: return 1
        else:
            return 1

    # generate new curve 3 when curve 1 is passed --> curve 2 is kept in memory
    # has to generate two curves at the start of a run
    @staticmethod
    def controlPointGenerator(p11, p21, p31, p41):
        # takes in p21, p31, p41 as the new p12 is determined by p41 of the last curve - p(point #, curve #)
        # may be using p31 and possibly p21 depending on continuity

        minY = p41.y * 1.3
        # p12 = p41
        p22 = Terrain.c1(p31, p41)

        continuity = Terrain.continuousRand()
        if continuity == 0:
            scalarX = (random.random() // 0.001) + 1
            scalarY = (random.random() // 0.001) + 1

            p22 = Point(p41.x * scalarX, p41.y * scalarY)
        
        # p32 can be below or above p42, controlling whether or not the curve will flick up or down
        # generate p42 first??
        scalarX, scalarY = (random.random() // 0.001) + 1, (random.random() // 0.001) + 1
        scalarp2x, scalarp2y = (random.random() // 0.001), (random.random() // 0.001)
        
        p42 =  Point( p22.x * scalarX + p22.x * scalarp2x, )

        p32 = Point( p22.x * scalarX + p22.x * scalarp2x, )
        p42 = None

        return p41, p22, p32, p42

        
        # use random to generate x and y? use some kind of logic to set bounds?
        # what logic?
        
    
    

    

    

    

    
