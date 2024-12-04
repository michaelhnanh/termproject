from terrain import *
from background import *
from character import *
from chasers import *
from hazards import *
from platforms import *

import math, time, random

def moveCharacter(app):
    # print('\n')
    print(app.character.posOnCurve)
    initialPoint = assignCurvePoint(app, app.character.posOnCurve)
    # print(f'initial point is position {app.character.posOnCurve} on curve {app.character.currentCurve}')

    # closest point may be an under or over estimate - if negative --> overestimate, if positive --> underestimate
    initialDir = -1 if (app.character.x - initialPoint.x) < 0 else 1
    initialError = distance(Point(app.character.x, app.character.y), initialPoint)
    # print(f'initial error is: {initialError} in {initialDir} direction')
    
    projectedDistanceMoved = 0
    counter = app.character.posOnCurve
    oneJump = 0

    while projectedDistanceMoved < app.character.speed:
        if counter + 2 >= len(app.terrain.pointsList[app.character.currentCurve]): 
            # character is projected to move between points of next curve
            app.character.currentCurve += 1
            counter = 0
        # print(f'curve is: {app.character.currentCurve}  counter is: {counter}')

        # print(counter, counter + 2)
        oneJump = distance(assignCurvePoint(app, counter), assignCurvePoint(app, counter + 2))
        projectedDistanceMoved += oneJump
        # print(f'this jump: {oneJump}')
        # print(f'distance moved so far: {projectedDistanceMoved}')
        counter += 2

    undershot = assignCurvePoint(app, counter - 2)
    # print(f'undershot point is {undershot}')
    overshot = assignCurvePoint(app, counter)
    # print(f'overshot point is {overshot}')
    lastJump = oneJump # distance between under and over shot points
    projectedDistanceMoved -= lastJump
    remainingInterPointDistance = app.character.speed - projectedDistanceMoved 
    # --> the remaining distance between undershot and overshot that has to be moved
    # print(f'remaining distance that has to be traversed {remainingInterPointDistance}')

    # the character does not breach new points from their initial point
    if projectedDistanceMoved == 0: 
        # print('interpoint movement')
        if initialDir < 0: # if initial position is overestimated --> moving towards undershot
            distanceToUndershot = distance(Point(app.character.x, app.character.y), undershot)
            # print('initial position is overestimated')
            if distanceToUndershot >= app.character.speed:
                # distance to undershot point is not fully traversable by speed --> would still fall short of undershot point
                # calculating angle --> take point before undershot point
                # need to correct for if undershot point is at 0th index of curve
                underUnderShotIndex = counter - 2 - 2
                if underUnderShotIndex < 0:
                    underUnderShot = assignCurvePoint2(app, 198, app.character.currentCurve - 1)
                else:
                    underUnderShot = assignCurvePoint(app, underUnderShotIndex)
                angle = math.atan2(-1 * (underUnderShot.y - undershot.y), underUnderShot.x - undershot.x)
                vectX = (undershot.x - app.character.x -
                        (distanceToUndershot - app.character.speed) * math.cos(angle))
                vectY = (undershot.y - app.character.y +
                        (distanceToUndershot - app.character.speed) * math.sin(angle))
                # print('movement to under')
                # print(f' Angle: {math.degrees(angle)}  X: {vectX},  Y:{vectY}')
                return vectX, vectY
            
            else: # distance to undershot point is surpassed by speed
                remainder = app.character.speed - distanceToUndershot
                angle = math.atan2(-1 * (overshot.y - undershot.y), overshot.x - undershot.x)
                vectX = (undershot.x - app.character.x + 
                        (remainder) * math.cos(angle))
                vectY = (undershot.y - app.character.y - 
                        (remainder) * math.sin(angle))
                
                # print(f'{undershot.x} - {app.character.x} + {remainder} * {math.cos(angle)} = {vectX}')
                # print(f'{undershot.y} - {app.character.y} - {remainder} * {math.sin(angle)} = {vectY}')
                # print('movement past under') # problem area
                # print(f' Angle: {math.degrees(angle)}  X: {vectX},  Y:{vectY}')
                return vectX, vectY
            
        elif initialDir > 0: # if initial position is underestimated --> moving towards overshot
            # print('initial position is underestimated')
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
                
                # print('movement past over')
                # print(f' X: {vectX},  Y:{vectY}')
                return vectX, vectY

            else: # final position will be within undershot and overshot points
                # print(f'total movement is: {totalMovement}')
                angle = math.atan2(-1 * (overshot.y - undershot.y), overshot.x - undershot.x)
                vectX = (undershot.x - app.character.x + (totalMovement) * math.cos(angle))
                vectY = (undershot.y - app.character.y - (totalMovement) * math.sin(angle))
                
                # print(f'{undershot.x} - {app.character.x} + {totalMovement} * {math.cos(angle)} = {vectX}')
                # print(f'{undershot.y} - {app.character.y} - {totalMovement} * {math.sin(angle)} = {vectY}')
                # print('movement between un and over') # problem area
                # print(f' Angle: {math.degrees(angle)}  X: {vectX},  Y:{vectY}')
                return vectX, vectY

    elif initialDir < 0: 
        # speed calculations move by at least one jump
        # if initial position overestimated --> projectedDistanceMoved is an overestimate
        # print('overestimated initial point')
        remainingDistanceAfterMovement = remainingInterPointDistance + initialError * initialDir
        # print(f'total distance be moving --> {remainingDistanceAfterMovement}')

        if remainingDistanceAfterMovement > lastJump:
            # moved past overshot point when error is included
            # print('moved past overshot point')
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
            
            # print(f'{overshot.x} - {app.character.x} + {remainder} * {math.cos(angle)} = {vectX}')
            # print(f'{overshot.y} - {app.character.y} - {remainder} * {math.sin(angle)} = {vectY}')
            # print(f'Angle: {math.degrees(angle)}  X: {vectX},  Y:{vectY}')
            return vectX, vectY
        
        else:
            # did not overshoot overshot
            # print('did not overshoot overshot') 
            angle = math.atan2(-1 * (overshot.y - undershot.y), overshot.x - undershot.x)
            vectX = (undershot.x - app.character.x + (remainingDistanceAfterMovement) * math.cos(angle))
            vectY = (undershot.y - app.character.y - (remainingDistanceAfterMovement) * math.sin(angle))

            # print(f'{undershot.x} - {app.character.x} + {remainingDistanceAfterMovement} * {math.cos(angle)} = {vectX}')
            # print(f'{undershot.y} - {app.character.y} - {remainingDistanceAfterMovement} * {math.sin(angle)} = {vectY}')

            # print(f'Angle: {math.degrees(angle)}  X: {vectX},  Y:{vectY}')
            return vectX, vectY
        
    elif initialDir > 0: # if initial position underestimated --> projectedDistanceMove is an underestimate
        # print('underestimated initial point')
        # check if initial error + undershot correction is larger than distance from undershot to overshot point
        remainingDistanceAfterMovement = remainingInterPointDistance + initialError * initialDir
        if remainingInterPointDistance + initialError > lastJump:
            # print('moved past overshot point --> onto next point')
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

            # print(f'{overshot.x} - {app.character.x} + {remainingDistanceAfterCorrection} * {math.cos(angle)} = {vectX}')
            # print(f'{overshot.y} - {app.character.y} - {remainingDistanceAfterCorrection} * {math.sin(angle)} = {vectY}')

            # # print(f'corrected backwards by: {remainingDistanceAfterCorrection} in {angle} direction')
            # print(f'Angle: {math.degrees(angle)}  X: {vectX},  Y:{vectY}')
            return vectX, vectY
        
        else: # if not, then the target point is in the middle of the undershot and overshot points
            # print('underestimated initial point, within bounds of under-over')
            remaining = remainingInterPointDistance + initialError * initialDir
            angle = math.atan2(-1 * (overshot.y - undershot.y),overshot.x - undershot.x)
            vectX = (undershot.x - app.character.x + (remaining) * math.cos(angle))
            vectY = (undershot.y - app.character.y - (remaining) * math.sin(angle))

            # print(f'{undershot.x} - {app.character.x} + {remaining} * {math.cos(angle)} = {vectX}')
            # print(f'{undershot.y} - {app.character.y} - {remaining} * {math.sin(angle)} = {vectY}')
            # print(f'Angle: {math.degrees(angle)}  X: {vectX},  Y:{vectY}')
            return vectX, vectY
        
def getOrientation(app):
    # print(f'orientation check --> {app.character.posOnCurve - 2}, {app.character.posOnCurve}, {app.character.posOnCurve + 2}')
    preceedingPoint = assignCurvePoint(app, app.character.posOnCurve - 2)
    if app.character.posOnCurve + 2 >= len(app.terrain.pointsList[app.character.currentCurve]):
        app.character.currentCurve += 1
        proceedingPoint = assignCurvePoint(app, 0)
        app.character.currentCurve -= 1
    else:
        proceedingPoint = assignCurvePoint(app, app.character.posOnCurve + 2)
    angle = math.atan2((proceedingPoint.y - preceedingPoint.y), proceedingPoint.x - preceedingPoint.x)
    # print(f'character orientation is {math.degrees(angle)}')
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

def setCurrentCurve(app):
    satisfied = False
    for i in range(len(app.terrain.controlList)):
        curve = app.terrain.controlList[i]
        firstPoint = curve[0]
        lastPoint = curve[-1]
        if firstPoint.x <= app.character.x and app.character.x <= lastPoint.x:
            app.character.currentCurve = i        

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

def slideCharacter(app):
    # print('\n')
    app.character.posOnCurve = findClosestPosOnCurve(app) # finds it every time character moves
    initial = assignCurvePoint(app, app.character.posOnCurve)
    # print(f'{initial} --> ')
    
    initialXError = app.character.x - initial.x
    initialYError = app.character.y - initial.y
    # print(initialXError, initialYError)
    # print(f'initial error is {initialError * errorDir}')
    distanceMoved = 0

    stored = initial
    i = app.character.posOnCurve

    while distanceMoved < app.character.speed:
        i += 2
        if i >= len(app.terrain.pointsList[app.character.currentCurve]):
            app.character.currentCurve += 1
            i = 0
        
        current = assignCurvePoint(app, i)
        newDistance = distance(stored, current) # distance moved from one point to another
        distanceMoved += newDistance
        stored = current # resetting jumping point

    overshot = assignCurvePoint(app, i)
    undershot = assignCurvePoint(app, i-2)
    # print(f'{undershot} -- [target] -- {overshot}')

    overshootingError = distanceMoved - app.character.speed
    # print(f'point overshot by: {overshootingError}')
    # direction of this error should be calculated
    angle = math.radians(math.atan2(overshot.x - undershot.x, (overshot.y - undershot.y)))
    # print(math.degrees(angle))

    characterPositionX = undershot.x + (overshootingError + initialXError) * math.cos(angle)
    characterPositionY = undershot.y + (overshootingError + initialYError) * math.sin(angle)

    app.characterMovementVectX = characterPositionX - app.character.x
    app.characterMovementVectY = characterPositionY - app.character.y
    print(app.characterMovementVectX, app.characterMovementVectY)
    app.character.momentum = app.characterMovementVectX
    # print(f'x move: {app.characterMovementVectX}, y move: {app.characterMovementVectY}')