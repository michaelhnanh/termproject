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
    app.gravity = 0.5

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

    app.character = Character(app.width/5, app.height/2)
    app.character.grounded = False
    app.character.rotating = False
    app.character.orientation = 0

    app.groundPoint = None

def restartGame(app):
    app.moveWorldVectX = 0
    app.moveWorldVectY = 0
    app.characterMovementVectX = 0
    app.characterMovementVectY = 0

    p1 = Point(0, app.height * 6 / 7)
    p2 = Point(app.width / 4, app.height * 4 / 6)
    p3 = Point(app.width * 3 / 4, app.height * 4 / 6)
    p4 = Point(app.width + 1, app.height * 6 / 7)
    app.terrain = Terrain(p1, p2, p3, p4)
    app.terrain.controlList = []
    app.terrain.pointsList = []
    app.character.continuityList = [1] # continuity figure correlates to p2 of the curve --> first curve has 1 as default
    app.character.curvesPassed = []
    app.terrain.startPreGen(app.width)

    app.character = Character(app.width/5, app.height/2)
    app.character.grounded = False
    app.character.rotating = False
    app.character.orientation = 0

    app.gameState = 'startScreen'

def onKeyPress(app, key):
    if app.gameState == 'startScreen':
        if (key == 'W' or 'w' or 'space' or 'up'):
            app.gameState = 'playing'
            print(app.gameState)

    elif app.gameState == 'playing':
        if (key == 'W' or 'w' or 'space' or 'up') and app.character.grounded == True:
            app.characterMovementVectY = 0
            app.characterMovementVectX = 0
            jump(app)
        if key == 'escape':
            app.gameState = 'pause'
        # if app.character.platformed:
        #     if key == 'down' or key == 's' or key == 'S':
        #         app.character.drop()

    elif app.gameState == 'dead':
        if key:
            app.gameState = 'startScreen'
            restartGame(app)
    

# def onKeyRelease(app, key):
#     if app.gameState == 'playing':
#         if (key == 'space' or key == 'w' or key == 'W' or key == 'up') and app.character.grounded == False:
#             app.character.rotating = False
#         if key == 'w':
#             app.moveWorldVectX = 0
#             app.moveWorldVectY = 0
#         elif key == 's':
#             app.moveWorldVectX = 0
#             app.moveWorldVectY = 0
#         elif key == 'a':
#             app.moveWorldVectX = 0
#             app.moveWorldVectY = 0
#         elif key == 'd':
#             app.moveWorldVectX = 0
#             app.moveWorldVectY = 0
  

def onKeyHold(app, keys):
    if app.gameState == 'playing':
        if ('space' in keys or 'w' in keys or 'W' in keys or 'up' in keys) and (app.character.grounded == False):
            app.character.orientation -= app.character.rotationRate # rotating
        elif 'escape' in keys:
            app.gameState = 'pause'


        # # terrain testing nav:
        # if 'w' in keys:
        #     app.moveWorldVectX = 0
        #     app.moveWorldVectY = -50
        # if 's' in keys:
        #     app.moveWorldVectX = 0
        #     app.moveWorldVectY = 50
        # if 'a' in keys:
        #     app.moveWorldVectX = -50
        #     app.moveWorldVectY = 0
        # if 'd' in keys:
        #     app.moveWorldVectX = 50
        #     app.moveWorldVectY = 0

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
            app.terrain.continuityList.pop(0)
            app.character.currentCurve -= 1
            print('\n0th curve removed\n')

        # this could be made very accurate by reparametrizing the points to be evenly spaced in every curve --> do that later
        
        # make character slide to positionX and positionY calculations first btw

        if app.character.grounded: # have to update character.currentCurve if it overshoots curve
            # sliding character along slopes --> turn into function later
            # vectX, vectY = slideCharacter(app, findClosestPosOnCurve(app), app.character.speed)
            # worldMovementVectX += vectX
            # worldMovementVectY += vectY
            setCurrentCurve(app)
            # print(f'curve i am currently on has c{app.terrain.continuityList[app.character.currentCurve]} continuity, next has c{app.terrain.continuityList[app.character.currentCurve + 1]} continuity')
            # slideCharacter(app)
            app.characterMovementVectX, app.characterMovementVectY = moveCharacter(app)

            app.character.orientation = getOrientation(app)
            moveWorld(app, worldMovementVectX, worldMovementVectY)
            if app.terrain.continuityList[app.character.currentCurve] == 0:
                slideOff(app)

        else: 
            moveWorld(app, worldMovementVectX, worldMovementVectY)
            setCurrentCurve(app)
            orientationOfGround = getOrientation(app)
            
            app.character.posOnCurve = findClosestPosOnCurve(app) # continually keeps track of position on curve for collision
            if app.characterMovementVectY < 30:
                app.characterMovementVectY += app.gravity # gravity   
            # print(f'post grav: {app.characterMovementVectY}')    

            # if app.characterMovementVectX > 2:
            #     app.characterMovementVectX -= 0.25
            
            # ground collision check
            groundPointApproximate = assignCurvePoint(app, app.character.posOnCurve)
            app.groundPoint = groundPointApproximate
            error = distance(app.character, groundPointApproximate)

            if groundPointApproximate.y <= app.character.y:
                if app.character.x > groundPointApproximate.x:
                    if app.character.posOnCurve + 2 >= len(app.terrain.pointsList[app.character.currentCurve]):
                        nextPoint = assignCurvePoint2(app, 0, app.character.currentCurve + 1)
                    else:
                        nextPoint = assignCurvePoint(app, app.character.posOnCurve + 2)
                    angleToNextPoint = math.atan2(nextPoint.y - groundPointApproximate.y, nextPoint.x - groundPointApproximate.x)
                    vectX = groundPointApproximate.x - app.character.x + error * math.cos(math.radians(angleToNextPoint))
                    vectY = groundPointApproximate.y - app.character.y + error * math.sin(math.radians(angleToNextPoint))
                else:
                    if app.character.posOnCurve - 2 < 0:
                        lastPoint = assignCurvePoint2(app, 0, app.character.currentCurve - 1)
                    else:
                        lastPoint = assignCurvePoint(app, app.character.posOnCurve - 2)
                    angleToLastPoint = math.atan2(lastPoint.y - groundPointApproximate.y, lastPoint.x - groundPointApproximate.x)
                    vectX = groundPointApproximate.x - app.character.x + error * math.cos(math.radians(angleToLastPoint))
                    vectY = groundPointApproximate.y - app.character.y + error * math.sin(math.radians(angleToLastPoint))
                
                app.characterMovementVectX = vectX
                app.characterMovementVectY = vectY
                app.character.grounded = True

                if app.character.orientation < -180:
                    app.character.orientation += 360                
                    # orientation never goes more than 180 degrees and less than -180 degrees
                if (app.character.orientation + 60 < orientationOfGround) or (app.character.orientation - 45 > orientationOfGround):
                    print(f'character orientation: {app.character.orientation} ground orientation: {orientationOfGround} --> dead')
                    app.gameState = 'dead'
                    
            #     # check if it if an over or under estimate in x value
            #     # then check if 
    
    elif app.gameState == 'pause':
        pass

# character movement
def moveCharacter(app):
    speed = app.character.speed
    app.character.posOnCurve = findClosestPosOnCurve(app)
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

    characterPositionX = overshot.x + (overshootingError + initialXError) * math.cos(angle)
    characterPositionY = overshot.y - (overshootingError + initialYError) * math.sin(angle)

    app.characterMovementVectX = characterPositionX - app.character.x
    app.characterMovementVectY = characterPositionY - app.character.y
    app.character.momentum = app.characterMovementVectX
    # print(f'x move: {app.characterMovementVectX}, y move: {app.characterMovementVectY}')

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

def jump(app):
    app.character.grounded = False
    if app.character.orientation > 0:
        app.characterMovementVectX = (app.character.vert + app.character.momentum) * math.cos(app.character.orientation)
        app.characterMovementVectY = (app.character.vert) * math.sin(app.character.orientation + 90)
    elif app.character.orientation > 20:
        app.characterMovementVectX = (app.character.momentum) * math.cos(app.character.orientation)
        app.characterMovementVectY = (app.character.vert + app.character.momentum) * math.sin(app.character.orientation)
    else:
        app.characterMovementVectX = (app.character.momentum) * math.cos(app.character.orientation)
        app.characterMovementVectY = (app.character.vert) * math.sin(app.character.orientation + 90)
    app.characterMovementVectX = (app.character.momentum) * math.cos(math.radians(app.character.orientation)) + (app.character.vert) * math.cos(math.radians(app.character.orientation - 90))
    app.characterMovementVectY = (app.character.vert) * math.sin(math.radians(app.character.orientation - 90))
    print(f'jumpX: {app.characterMovementVectX} jumpY: {app.characterMovementVectY}')
    
def slideOff(app):
    app.character.grounded = False
    app.terrain.continuityList[app.character.currentCurve] = 1


# function to move terrain + hazards + platforms + chasers + character
def moveWorld(app, worldMovementVectX, worldMovementVectY):
    # if app.moveWorldVectX != 0 or app.moveWorldVectY != 0:
    for curvePoints in app.terrain.pointsList:
        for counter in range(0, len(curvePoints), 2):
            curvePoints[counter] -= (app.characterMovementVectX)
            curvePoints[counter + 1] -= (app.characterMovementVectY)
    for curve in app.terrain.controlList:
        for controlPoint in curve:
            controlPoint.x -= (app.characterMovementVectX)
            controlPoint.y -= (app.characterMovementVectY)

def redrawAll(app):
    # background --> draw series of shifting polygons

    # terrain --> draw polygon --> select which curves to draw based on the position of 
    # control points unpack selected pointsList indexes into drawPolygon, starting and ending with anchor points
    terrainGradient = gradient('white', rgb(173, 237, 208), start='bottom')
    drawRect(0, 0, app.width, app.height, fill=terrainGradient)

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

    if app.gameState == 'startScreen':
        drawLabel("AUSTIN'S", app.width/2, app.height/5, align = 'center', size = 150, font = 'monospace', bold = True)
        drawLabel("ADVENTURE", app.width/2, app.height/5 + 90, align = 'center', size = 100, font = 'monospace', bold = True)
        drawLabel("Press any key to play", app.width/2, app.height/5*4, align = 'center', size = 15, font = 'monospace', bold = False)
        drawLabel("Press W, space, or the up arrow key to jump/flip", app.width/2, app.height/5*4 + 15, align = 'center', size = 15, font = 'monospace', bold = False)

    imageOffsetAngle = app.character.orientation - 90
    playerImageCenterX = app.character.x + app.character.width/2 * math.cos(math.radians(imageOffsetAngle))
    playerImageCenterY = app.character.y + app.character.height/2 * math.sin(math.radians(imageOffsetAngle))


    if app.gameState == 'playing':
        drawRect(app.character.x, app.character.y, 15, 7, fill='coral', border=None, borderWidth=2, dashes=False,      
                    rotateAngle = app.character.orientation, align = 'center')

        # drawImage(app.character.linkGrounded, app.character.x, app.character.y, 
        #           width = app.character.width, height = app.character.width, align = 'bottom', 
        #           rotateAngle = app.character.  orientation)
        # drawLabel(math.floor(app.character.orientation), 45, 45)

    if app.gameState == 'dead':
    #     drawRect(app.character.x, app.character.y, 15, 7, fill='coral', border=None, borderWidth=2, dashes=False,      
    #                 rotateAngle = app.character.orientation, align = 'center')
        drawImage(app.character.linkGrounded, playerImageCenterX, playerImageCenterY+3, 
                  width = app.character.width, height = app.character.width, align = 'center', 
                rotateAngle = app.character.  orientation)
        drawLabel("GAME OVER", app.width/2, app.height/5 , align = 'center', size = 100, font = 'monospace', bold = True)
    
    # if app.character.grounded == False and app.groundPoint != None:
    #     drawCircle(app.groundPoint.x, app.groundPoint.y, 10, fill='cyan')


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
