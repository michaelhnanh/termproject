# code for terrain generation + storage + drawing
# would probably return a set of 

from cmu_graphics import *
from tools import *
import math, random

class Terrain:
    xray = []
    lineSplit = 75
    segment = 1 / lineSplit

    def __init__(self, p1, p2, p3, p4):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        # these points would store the LAST control points after the last curve was generated,
        # be updated, and stored again

        self.pointsList = []
        self.controlList = [] # 2d list containing lists of control points
        self.lengthList = [] # length of the list of points in pointsList corresponding to controlList[0]
        self.continuityList = [1] # continuity figure correlates to p2 of the curve --> first curve has 1 as default
 
        self.curvesPassed = []

    def startPreGen(self, width):
        # for the start of the game only, pre-generates one curve ahead of time + starting curve
        self.controlList.append([self.p1, self.p2, self.p3, self.p4])

        curve = self.genCurve()
        self.lengthList.append(len(curve))
        self.pointsList.append(curve)

        self.curvesPassed.append(False)

        self.fullGenerator(width)

    def fullGenerator(self, width):
        # controlPointGenerator takes in p3, p4, and width
        # --> spits out 4 new control points --> add to a list --> add list to controlList
        self.p1, self.p2, self.p3, self.p4, scalar = self.controlPointGenerator(width)
        self.controlList.append([self.p1, self.p2, self.p3, self.p4])
        
        # feed control points into genCurve --> spits out list of points for drawing
        # append to pointsList
        lineSplit = 150 * scalar
        segment = 1 / lineSplit
        print(lineSplit)
        curve = self.genCurve()
        self.lengthList.append(len(curve))
        self.pointsList.append(curve)

        self.curvesPassed.append(False)

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

    def genCurve(self):
        curve = []
        t = 0
        while t < 1 + Terrain.segment:
            x, y = Terrain.cubicBezier(self.p1, self.p2, self.p3, self.p4, t)
            curve.append(x)
            curve.append(y)
            t += Terrain.segment
        return curve
    
    # calculate c1 continuity with the previous curve and returns an angle for the first control point of the next curve
    @staticmethod
    def c1(p3, p4):
        # print('c1 calculation with: ',p3, p4)
        vectorX = p4.x - p3.x
        vectorY = p4.y - p3.y
        return vectorX, vectorY
    
    @staticmethod
    def c1Angle(p3, p4):
        return math.atan2(p4.y - p3.y, p4.x - p3.x)

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
            if continuity > 13: 
                return 0
            else: 
                return 1
        else:
            return 1

    # generate new curve 3 when curve 1 is passed --> curve 2 is kept in memory
    # has to generate two curves at the start of a run
    def controlPointGenerator(self, width):
        pastLength = ((self.p4.x - self.p1.x) ** 2 + (self.p4.y - self.p1.x) ** 2) ** 0.5
        p12 = Point(self.p4.x, self.p4.y)

        # some formula to allow for a wider normal distribution
        scalar = normalScalar() * 2
        if scalar < 0.9:
            scalar = 0.9
        if scalar > 1.1:
            scalar = 1.1
        totalLength = width * scalar

        lengthp22 = totalLength / 3
        c1vectX, c1vectY = Terrain.c1(self.p3, self.p4)
        c1vectX = c1vectX / pastLength * totalLength 
        c1vectY = c1vectY / pastLength * totalLength
        p22 = Point(p12.x + c1vectX, p12.y + c1vectY)

        continuity = Terrain.continuousRand(self.p4, p22)
        if continuity == 0:
            anglep22 = math.radians(random.randrange(270, 315, 1))
            p22 = Point(self.p4.x + lengthp22 * math.cos(anglep22), 
                        self.p4.y - lengthp22 * math.sin(anglep22))
            
        # if continuity == 1 do nothing

        # limit slope between 0 - 45 degrees
        anglep42 = math.radians(normalRandom(325, 354, 1))
        # p32 can be below or above p42, controlling whether or not the curve will flick up or down
        if scalar > 1:
            anglep32 = math.radians(normalRandom(135, 205, 1))
        else:
            anglep32 = math.radians(normalRandom(135, 225, 1))

        p42 = Point(p12.x + totalLength * math.cos(anglep42), p12.y - (totalLength * math.sin(anglep42)))
        lengthp32 = totalLength / 3 
        p32 = Point(p42.x + lengthp32 * math.cos(anglep32), p42.y - (lengthp32 * math.sin(anglep32)))
        self.continuityList.append(continuity)
        
        return p12, p22, p32, p42, scalar
        
def normalScalar():
    return ((random.random() - random.random() + 1)/2)

def normalRandom(min, max, step = 1):
    center = min + max
    return (random.randrange(min, max, step) - random.randrange(min, max, step) + center)/2

    
