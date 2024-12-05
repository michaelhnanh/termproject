from terrain import *
from background import *
from character import *
from chasers import *
from hazards import *
from platforms import *

import math, time, random

def moveCharacter(app):
    # print(app.character.posOnCurve)
    initialPoint = assignCurvePoint(app, app.character.posOnCurve)

    initialDir = -1 if (app.character.x - initialPoint.x) < 0 else 1
    initialError = distance(Point(app.character.x, app.character.y), initialPoint)
    
    projectedDistanceMoved = 0
    counter = app.character.posOnCurve
    oneJump = 0

    while projectedDistanceMoved < app.character.speed:
        if counter + 2 >= len(app.terrain.pointsList[app.character.currentCurve]): 
            app.character.currentCurve += 1
            counter = 0

        oneJump = distance(assignCurvePoint(app, counter), assignCurvePoint(app, counter + 2))
        projectedDistanceMoved += oneJump
        counter += 2

    undershot = assignCurvePoint(app, counter - 2)
    overshot = assignCurvePoint(app, counter)
    lastJump = oneJump # distance between under and over shot points
    projectedDistanceMoved -= lastJump
    remainingInterPointDistance = app.character.speed - projectedDistanceMoved 
    # --> the remaining distance between undershot and overshot that has to be moved

    # the character does not breach new points from their initial point
    if projectedDistanceMoved == 0: 
        if initialDir < 0: # if initial position is overestimated --> moving towards undershot
            distanceToUndershot = distance(Point(app.character.x, app.character.y), undershot)
            if distanceToUndershot >= app.character.speed:
                # distance to undershot point is not fully traversable by speed --> would still fall short of undershot point
                # calculating angle --> take point before undershot point
                # need to correct for if undershot point is at 0th index of curve
                underUnderShotIndex = counter - 2 - 2
                if underUnderShotIndex < 0:
                    underUnderShot = assignCurvePoint2(app, len(app.terrain.pointsList[app.character.currentCurve - 1]) - 2, app.character.currentCurve - 1)
                else:
                    underUnderShot = assignCurvePoint(app, underUnderShotIndex)
                angle = math.atan2(-1 * (underUnderShot.y - undershot.y), underUnderShot.x - undershot.x)
                vectX = (undershot.x - app.character.x -
                        (distanceToUndershot - app.character.speed) * math.cos(angle))
                vectY = (undershot.y - app.character.y +
                        (distanceToUndershot - app.character.speed) * math.sin(angle))
                return vectX, vectY
            
            else: # distance to undershot point is surpassed by speed
                remainder = app.character.speed - distanceToUndershot
                angle = math.atan2(-1 * (overshot.y - undershot.y), overshot.x - undershot.x)
                vectX = (undershot.x - app.character.x + (remainder) * math.cos(angle))
                vectY = (undershot.y - app.character.y - (remainder) * math.sin(angle))
                return vectX, vectY
            
        elif initialDir > 0: # if initial position is underestimated --> moving towards overshot
            totalMovement = app.character.speed + distance(Point(app.character.x, app.character.y), undershot)
            distanceToOvershot = distance(undershot, overshot)

            if totalMovement > distanceToOvershot: # final position will go past overshot
                remainder = totalMovement - distanceToOvershot
                overOverShotIndex = counter + 2
                if overOverShotIndex >= len(app.terrain.pointsList[app.character.currentCurve]):
                    overOverShot = assignCurvePoint2(app, 0, app.character.currentCurve + 1)
                else:
                    overOverShot = assignCurvePoint(app, overOverShotIndex)
                angle = math.atan2(-1 * (overOverShot.y - overshot.y), overOverShot.x - overshot.x)
                vectX = (overshot.x - app.character.x + (remainder) * math.cos(angle))
                vectY = (overshot.y - app.character.y - (remainder) * math.sin(angle))
                return vectX, vectY

            else: # final position will be within undershot and overshot points
                angle = math.atan2(-1 * (overshot.y - undershot.y), overshot.x - undershot.x)
                vectX = (undershot.x - app.character.x + (totalMovement) * math.cos(angle))
                vectY = (undershot.y - app.character.y - (totalMovement) * math.sin(angle))
                return vectX, vectY

    elif initialDir < 0: 
        # speed calculations move by at least one jump
        # if initial position overestimated --> projectedDistanceMoved is an overestimate
        remainingDistanceAfterMovement = remainingInterPointDistance + initialError * initialDir

        if remainingDistanceAfterMovement > lastJump:
            # moved past overshot point when error is included
            remainder = remainingDistanceAfterMovement - lastJump
            overOverShotIndex = counter + 2
            if overOverShotIndex >= len(app.terrain.pointsList[app.character.currentCurve]):
                overOverShot = assignCurvePoint2(app, 0, app.character.currentCurve + 1)
            else:
                overOverShot = assignCurvePoint(app, overOverShotIndex)
            angle = math.atan2( -1 * (overOverShot.y - overshot.y), overOverShot.x - overshot.x)
            vectX = (overshot.x - app.character.x +
                        (remainder) * math.cos(angle))
            vectY = (overshot.y - app.character.y +
                        (remainder) * math.sin(angle))
            return vectX, vectY
        
        else:
            # did not overshoot overshot
            angle = math.atan2(-1 * (overshot.y - undershot.y), overshot.x - undershot.x)
            vectX = (undershot.x - app.character.x + (remainingDistanceAfterMovement) * math.cos(angle))
            vectY = (undershot.y - app.character.y - (remainingDistanceAfterMovement) * math.sin(angle))
            return vectX, vectY
        
    elif initialDir > 0: # if initial position underestimated --> projectedDistanceMove is an underestimate
        # check if initial error + undershot correction is larger than distance from undershot to overshot point
        remainingDistanceAfterMovement = remainingInterPointDistance + initialError * initialDir
        if remainingInterPointDistance + initialError > lastJump:
            if counter + 2 >= len(app.terrain.pointsList[app.character.currentCurve]):
                afterOverShot = Point(app.terrain.pointsList[app.character.currentCurve + 1][0], 
                                      app.terrain.pointsList[app.character.currentCurve + 1][1])
                angle = math.atan2(-1 * (afterOverShot.y - overshot.y),afterOverShot.x - overshot.x)
            else:
                counter += 2
                afterOverShot = Point(app.terrain.pointsList[app.character.currentCurve][counter], 
                                      app.terrain.pointsList[app.character.currentCurve][counter + 1])
                angle = math.atan2(-1 * (afterOverShot.y - overshot.y), afterOverShot.x - overshot.x)
            
            remainingDistanceAfterCorrection = remainingInterPointDistance + initialError - lastJump
            vectX = overshot.x - app.character.x + remainingDistanceAfterCorrection * math.cos(angle)
            vectY = overshot.y - app.character.y - remainingDistanceAfterCorrection * math.sin(angle)
            return vectX, vectY
        
        else: # if not, then the target point is in the middle of the undershot and overshot points
            remaining = remainingInterPointDistance + initialError * initialDir
            angle = math.atan2(-1 * (overshot.y - undershot.y),overshot.x - undershot.x)
            vectX = (undershot.x - app.character.x + (remaining) * math.cos(angle))
            vectY = (undershot.y - app.character.y - (remaining) * math.sin(angle))
            return vectX, vectY
        
def groundCollisionCheck(app):
    groundPointApproximate = assignCurvePoint(app, app.character.posOnCurve)
    error = distance(app.character, groundPointApproximate)
    if groundPointApproximate.y <= app.character.y:
        app.character.grounded = True
        if app.character.x > groundPointApproximate.x:
            if app.character.posOnCurve + 2 >= len(app.terrain.pointsList[app.character.currentCurve]):
                nextPoint = assignCurvePoint2(app, 0, app.character.currentCurve + 1)
            else:
                nextPoint = assignCurvePoint(app, app.character.posOnCurve + 2)
            angleToNextPoint = math.atan2(nextPoint.y - groundPointApproximate.y, nextPoint.x - groundPointApproximate.x)
            vectX = groundPointApproximate.x - app.character.x + error * math.cos(angleToNextPoint)
            vectY = groundPointApproximate.y - app.character.y + error * math.sin(angleToNextPoint)
            return vectX, vectY
        else:
            if app.character.posOnCurve - 2 < 0:
                lastPoint = assignCurvePoint2(app, 0, app.character.currentCurve - 1)
            else:
                lastPoint = assignCurvePoint(app, app.character.posOnCurve - 2)
            angleToLastPoint = math.atan2(lastPoint.y - groundPointApproximate.y, lastPoint.x - groundPointApproximate.x)
            vectX = groundPointApproximate.x - app.character.x + error * math.cos(angleToLastPoint)
            vectY = groundPointApproximate.y - app.character.y + error * math.sin(angleToLastPoint)
            return vectX, vectY
    else:
        return 0, 0
        
def getOrientation(app):
    if app.character.posOnCurve - 2 < 0:
        predex = len(app.terrain.pointsList[app.character.currentCurve - 1]) - 4
        preCurve = app.character.currentCurve - 1
    else:
        predex = app.character.posOnCurve - 2
        preCurve = app.character.currentCurve
    if app.character.posOnCurve + 2 >= len(app.terrain.pointsList[app.character.currentCurve]):
        prodex = 0
        proCurve = app.character.currentCurve + 1
    else:
        prodex = app.character.posOnCurve + 2
        proCurve = app.character.currentCurve
    prodex = app.character.posOnCurve
    proCurve = app.character.currentCurve

    preceedingPoint = assignCurvePoint2(app, predex, preCurve)
    proceedingPoint = assignCurvePoint2(app, prodex, proCurve)
    angle = math.atan2(proceedingPoint.y - preceedingPoint.y, proceedingPoint.x - preceedingPoint.x)
    return math.degrees(angle)
    
def findClosestPosOnCurve(app): # finds the closest point the character is on on the currentCurve
    satisfied = False
    currentPoint = assignCurvePoint(app, 0)
    smallestDifference = abs(currentPoint.x - app.character.x)
    smallestDifferenceIndex = 0
    for i in range(2, len(app.terrain.pointsList[app.character.currentCurve]), 2):
        currentPoint = assignCurvePoint(app, i) 
        newDifference = abs(currentPoint.x - app.character.x)
        if newDifference <= smallestDifference: 
            smallestDifference = newDifference
            smallestDifferenceIndex = i
    # print(f'found closest at point # {smallestDifferenceIndex // 2} of curve {app.character.currentCurve}')
    return smallestDifferenceIndex

def findCurrentCurve(app):
    satisfied = False
    for i in range(len(app.terrain.controlList)):
        curve = app.terrain.controlList[i]
        firstPoint = curve[0]
        lastPoint = curve[-1]
        if firstPoint.x <= app.character.x and app.character.x <= lastPoint.x:
            return i
        elif lastPoint.x <= app.character.x and app.character.x <= app.terrain.controlList[i + 1][0].x:
            return i
  
def assignCurvePoint(app, i):
    return Point(app.terrain.pointsList[app.character.currentCurve][i], 
                app.terrain.pointsList[app.character.currentCurve][i + 1])

def assignCurvePoint2(app, i, curve = None):
    if curve == None:
        curve = app.character.currentCurve
    return Point(app.terrain.pointsList[curve][i], 
                app.terrain.pointsList[curve][i + 1])

def distance(point1, point2):
    return ((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2 ) ** 0.5
