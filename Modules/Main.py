from terrain import *
from background import *
from character import *
from chasers import *
from hazards import *
from platforms import *

import math, time, random

def onAppStart(app):
    scale = 75
    app.width = 16 * scale
    app.height = 9 * scale
    app.score = 0
    app.timeofday = 0
    app.gravity = 1

    # superfluous things
    app.settings = Point(app.width * 1 / 8, app.height * 1 / 7)
    app.characterSelect = Point(app.width * 7 / 8, app.height * 1 / 7)

    # game timings
    app.stepsPerSecond = 60 # fixed cus like 60 frames per second u know
    app.gameState = 'startScreen'

    # world movement
    app.moveWorldVectX = 0
    app.moveWorldVectY = 0
    app.characterMovementVectX = 0
    app.characterMovementVectY = 0

    p1 = Point(0, app.height * 6 / 7)
    p2 = Point(app.width / 4, app.height * 4 / 6)
    p3 = Point(app.width * 3 / 4, app.height * 4 / 6)
    p4 = Point(app.width + 1, app.height * 6 / 7)
    app.terrain = Terrain(p1, p2, p3, p4)
    app.terrain.startPreGen(app.width)

    app.character = Character(600, 482)
    app.character.grounded = True
    app.character.rotating = False


def onKeyPress(app, key):
    if app.gameState == 'startScreen':
        if key:
            app.gameState = 'playing'
            print(app.gameState)

    # elif app.gameState == 'playing':
    #     # if key == 'space' or key == 'w' or key == 'W' or key == 'up':
    #     #     app.character.grounded = False
    #     #     app.character.jump()
    #     # elif key == 'escape':
    #     #     app.gameState = 'pause'
    #     # if app.character.platformed:
    #     #     if key == 'down' or key == 's' or key == 'S':
    #     #         app.character.drop()

    #     # terrain testing nav:
    #     if key == 'w':
    #         app.moveWorldVectX = 0
    #         app.moveWorldVectY = -100
    #     elif key == 's':
    #         app.moveWorldVectX = 0
    #         app.moveWorldVectY = 100
    #     elif key == 'a':
    #         app.moveWorldVectX = -100
    #         app.moveWorldVectY = 0
    #     elif key == 'd':
    #         app.moveWorldVectX = 100
    #         app.moveWorldVectY = 0

    elif app.gameState == 'dead':
        if key == 'escape':
            app.gameState = 'exit'
    

def onKeyRelease(app, key):
    if app.gameState == 'playing':
        if (key == 'space' or key == 'w' or key == 'W' or key == 'up') and app.character.grounded == False:
            app.character.rotating = False
        if key == 'w':
            app.moveWorldVectX = 0
            app.moveWorldVectY = 0
        elif key == 's':
            app.moveWorldVectX = 0
            app.moveWorldVectY = 0
        elif key == 'a':
            app.moveWorldVectX = 0
            app.moveWorldVectY = 0
        elif key == 'd':
            app.moveWorldVectX = 0
            app.moveWorldVectY = 0
  

def onKeyHold(app, keys):
    if app.gameState == 'playing':
        # if key == 'space' or key == 'w' or key == 'W' or key == 'up':
        #     app.character.grounded = False
        #     app.character.jump()
        # elif key == 'escape':
        #     app.gameState = 'pause'
        # if app.character.platformed:
        #     if key == 'down' or key == 's' or key == 'S':
        #         app.character.drop()

        # terrain testing nav:
        if 'w' in keys:
            app.moveWorldVectX = 0
            app.moveWorldVectY = -50
        if 's' in keys:
            app.moveWorldVectX = 0
            app.moveWorldVectY = 50
        if 'a' in keys:
            app.moveWorldVectX = -50
            app.moveWorldVectY = 0
        if 'd' in keys:
            app.moveWorldVectX = 50
            app.moveWorldVectY = 0
        

def onMousePress(app, mouseX, mouseY):
    pass


def onStep(app):
    if app.gameState == 'playing':
        worldMovementVectX = 0
        worldMovementVectY = 0

        # detect when need to generate new terrain --> x coordinate of the oldest/first curve is moved past the width of the app
        if app.terrain.controlList[-2][-1].x <= app.width:
            if not app.terrain.curvesPassed[0]:
                print('\ncurve that just passed: ',app.terrain.controlList[0])
                app.terrain.fullGenerator(app.width)
                app.terrain.curvesPassed[0] = True

        # detect when curve has passed x = 0 --> controlList[0][-1].x < 0 (or another variable)
        # remove from pointsList, remove from controlList
        if app.terrain.controlList[0][-1].x < 0:
            print('\ncurve removed: ',app.terrain.controlList[0])
            app.terrain.controlList.pop(0)
            app.terrain.pointsList.pop(0)
            app.terrain.curvesPassed.pop(0)
            app.character.currentCurve -= 1
            print('\n0th curve removed\n')

        # this could be made very accurate by reparametrizing the points to be evenly spaced in every curve --> do that later
        
        # make character slide to positionX and positionY calculations first btw

        if app.character.grounded: # have to update character.currentCurve if it overshoots curve
            # sliding character along slopes --> turn into function later
            setCurrentCurve(app)
            # vectX, vectY = slideCharacter(app, setClosestPosOnCurve(app), app.character.speed)
            # worldMovementVectX += vectX
            # worldMovementVectY += vectY
            slideCharacter(app)
        else: # character is in air
            

        moveWorld(app, worldMovementVectX, worldMovementVectY)

    elif app.gameState == 'pause':
        pass

def moveCharacter(app, posOnCurve, speed):
    app.character.posOnCurve = posOnCurve
    initialPoint = assignCurvePoint(app, app.character.posOnCurve)

    # closest point may be an under or over estimate - if negative --> overestimate, if positive --> underestimate
    initialDir = app.character.x - initialPoint.x
    initialError = distance(Point(app.character.x, app.character.y), initialPoint)
    
    projectedDistanceMoved = 0
    counter = app.character.posOnCurve

    while projectedDistanceMoved < speed:
        if counter + 2 >= len(app.terrain.pointsList[app.character.currentCurve]): 
            # character is projected to move between points of next curve
            app.character.currentCurve += 1
            counter = 0
        
        print(counter, counter + 2)
        oneJump = distance(assignCurvePoint(app, counter), assignCurvePoint(app, counter + 2))
        projectedDistanceMoved += oneJump
        counter += 2

    undershot = assignCurvePoint(app, counter - 2)
    overshot = assignCurvePoint(app, counter)
    lastJump = oneJump # distance between under and over shot points
    projectedDistanceMoved -= lastJump
    remainingInterPointDistance = speed - projectedDistanceMoved # the remaining distance the character has to
    # move between undershot and overshot points (not considering initial error correction)

    if initialDir < 0: # if initial position overestimated --> projectedDistanceMoved is an overestimate
        # check if initial error + undershot correction will place character potentially multiple points back
        if remainingInterPointDistance + initialError < 0:
            backtrackDistance = remainingInterPointDistance + initialError
            # move in opposite direction until initial error is satiated
            # we start again at undershot point
            projectedDistanceBacktracked = 0
            backtrackCounter = app.character.posOnCurve + counter - 2
            
            while projectedDistanceBacktracked < backtrackDistance:
                if counter >= len(app.terrain.pointsList[app.character.currentCurve]): 
                # character is projected to move between points of next curve
                    app.character.currentCurve += 1
                    counter = 0

                backJump = distance(assignCurvePoint(app, counter - 2), assignCurvePoint(app, counter))
                projectedDistanceBacktracked += backJump
                backtrackCounter -= 2
            
            underBackshot = assignCurvePoint(app, backtrackCounter + 2)
            overBackshot = assignCurvePoint(app, backtrackCounter)
            lastBackJump = backJump
            projectedDistanceBacktracked -= lastBackJump
            remainingInterPointBacktrackDistance =  backtrackDistance - projectedDistanceBacktracked

            angle = math.atan2(overBackshot.x - underBackshot.x, -1 * (overBackshot.y - underBackshot.y))
            backVectX = underBackshot.x - app.character.x - remainingInterPointBacktrackDistance * math.cos(math.radians(angle))
            backVectY = underBackshot.y - app.character.y - remainingInterPointBacktrackDistance * math.sin(math.radians(angle))
            return backVectX, backVectY
            
        else:
            # if it does not, as in remainingInterPointDistance > initialError, move like normal
            angle = math.atan2(overshot.x - undershot.x, -1 * (overshot.y - undershot.y))
            vectX = undershot.x - app.character.x + (remainingInterPointDistance + initialError) * math.cos(math.radians(angle))
            vectY = undershot.y - app.character.y + (remainingInterPointDistance + initialError) * math.sin(math.radians(angle))
            return vectX, vectY
        
    else: # if initial position underestimated --> projectedDistanceMove is an underestimate
        # check if initial error + undershot correction is larger than distance from undershot to overshot point
        if remainingInterPointDistance + initialError > lastJump:
            if counter + 2 >= len(app.terrain.pointsList[app.character.currentCurve]):
                afterOverShot = Point(app.terrain.pointsList[app.character.currentCurve + 1][0], 
                                      app.terrain.pointsList[app.character.currentCurve + 1][1])
                angle = math.atan2(afterOverShot.x - overshot.x, -1 * (afterOverShot.y - overshot.y))
            else:
                afterOverShot = Point(app.terrain.pointsList[app.character.currentCurve][counter + 2], 
                                      app.terrain.pointsList[app.character.currentCurve][counter + 3])
                angle = math.atan2(afterOverShot.x - overshot.x, -1 * (afterOverShot.y - overshot.y))
            
            remainingDistanceAfterCorrection = lastJump - (remainingInterPointDistance + initialError)
            vectX = overshot.x - app.character.x + remainingDistanceAfterCorrection * math.cos(math.radians(angle))
            vectY = overshot.y - app.character.y + remainingDistanceAfterCorrection * math.sin(math.radians(angle))
            return vectX, vectY
        
        else: # if not, then the target point is in the middle of the undershot and overshot points
            angle = math.atan2(overshot.x - undershot.x, -1 * (overshot.y - undershot.y))
            vectX = undershot.x - app.character.x + (remainingInterPointDistance + initialError) * math.cos(math.radians(angle))
            vectY = undershot.y - app.character.y + (remainingInterPointDistance + initialError) * math.sin(math.radians(angle))
            return vectX, vectY

def slideCharacter(app):
    print('\n')
    app.character.posOnCurve = setClosestPosOnCurve(app) # finds it every time character moves
    initial = assignCurvePoint(app, app.character.posOnCurve)
    print(f'{initial} --> ')
    
    initialXError = app.character.x - initial.x
    initialYError = app.character.y - initial.y
    print(initialXError, initialYError)
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
    print(f'{undershot} -- [target] -- {overshot}')

    overshootingError = distanceMoved - app.character.speed
    print(f'point overshot by: {overshootingError}')
    # direction of this error should be calculated
    angle = math.radians(math.atan2(overshot.x - undershot.x, (overshot.y - undershot.y)))
    print(math.degrees(angle))

    characterPositionX = overshot.x + (overshootingError + initialXError) * math.cos(angle)
    characterPositionY = overshot.y - (overshootingError + initialYError) * math.sin(angle)

    app.characterMovementVectX = characterPositionX - app.character.x
    app.characterMovementVectY = characterPositionY - app.character.y
    print(f'x move: {app.characterMovementVectX}, y move: {app.characterMovementVectY}')

def setClosestPosOnCurve(app): # finds the closest point the character is on on the currentCurve
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
    print(f'found closest at point # {smallestDifferenceIndex // 2} of curve {app.character.currentCurve}')
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


# function to move terrain + hazards + platforms + chasers + character
def moveWorld(app, worldMovementVectX, worldMovementVectY):
    # if app.moveWorldVectX != 0 or app.moveWorldVectY != 0:
    for curvePoints in app.terrain.pointsList:
        for counter in range(0, len(curvePoints), 2):
            curvePoints[counter] -= (app.characterMovementVectX + worldMovementVectX)
            curvePoints[counter + 1] -= (app.characterMovementVectY + worldMovementVectX)
    for curve in app.terrain.controlList:
        for controlPoint in curve:
            controlPoint.x -= (app.characterMovementVectX + worldMovementVectY)
            controlPoint.y -= (app.characterMovementVectY + worldMovementVectY)

def redrawAll(app):
    # background --> draw series of shifting polygons

    # terrain --> draw polygon --> select which curves to draw based on the position of 
    # control points unpack selected pointsList indexes into drawPolygon, starting and ending with anchor points
    drawTo = 1
    for index in range(1, len(app.terrain.controlList)):
        p1 = app.terrain.controlList[index][0]
        if p1.x <= app.width and p1.y <= app.height:
            drawTo += 1

    drawnpointsList = []
    validPoints = app.terrain.pointsList[:drawTo] # drawn points is 2d list
    for points in validPoints: # point is a list
        drawnpointsList.extend(points)
            
    anchorStart = [0, app.height] # has to be [x,y] to be placed into drawPolygon, y determined by last controlpoint
    anchorEnd = [app.width, app.height]

    drawPolygon(*anchorStart, *drawnpointsList, *anchorEnd, fill = 'lightgreen')

    drawCircle(app.character.x, app.character.y, 25, fill='coral')

    # overlays --> slide to the outside and disappear when game starts

    # if app.gameState == 'startScreen':
    #     drawImage() # logo
    #     drawLabel('Press any key to play', ) 
    #         # settings
    #     drawImage()
    #     drawLabel('Settings')
    #         # character select
    #     drawImage()
    #     drawLabel('Characters')
    # if app.gameState == 'playing':
    #     drawImage() # logo
    #     drawLabel('Press any key to play', ) 
    #         # settings
    #     drawImage()
    #     drawLabel('Settings')
    #         # character select
    #     drawImage()
    #     drawLabel('Characters')

    # if app.gameState == 'pause':
        # overlay pause screen on top

# superfluous UI things

def distance(point1, point2):
    return ((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2 ) ** 0.5

def main():
    runApp()

main()
