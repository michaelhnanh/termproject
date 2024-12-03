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
    app.gravity = 0.3
    app.terminal = 20
    app.drag = 0.5
    app.dragLimit = 2

    # superfluous things
    app.settings = Point(app.width * 1 / 8, app.height * 1 / 7)
    app.characterSelect = Point(app.width * 7 / 8, app.height * 1 / 7)

    # game timings  
    app.stepsPerSecond = 1 # fixed cus like 60 frames per second u know
    app.stepNum = 0
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
    app.speedMax = 0
    app.angleTakeOff = 0

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
    steps = [1, 5, 15, 30, 60]

    if key == 'p':          
        app.stepNum += 1
        app.stepNum = app.stepNum % len(steps)  
        app.stepsPerSecond = steps[app.stepNum]
    if key == 'o':
        app.stepNum -= 1
        if app.stepNum < 0:
            app.stepNum = len(steps) - 1
        app.stepsPerSecond = steps[app.stepNum]
    if app.gameState == 'startScreen':
        if (key == 'W' or 'w' or 'space' or 'up'):
            app.gameState = 'playing'
            print(app.gameState)

    elif app.gameState == 'playing':
        if (key == 'W' or key == 'w' or key == 'space' or key == 'up') and app.character.grounded == True:
            app.characterMovementVectY = 0
            app.characterMovementVectX = 0
            app.angleTakeOff = getOrientation(app)
            jump(app)
            app.speedMax = app.characterMovementVectX
        if key == 'escape':
            app.gameState = 'pause'
        # if app.character.platformed:
        #     if key == 'down' or key == 's' or key == 'S':
        #         app.character.drop()

    elif app.gameState == 'dead':
        if key:
            app.gameState = 'startScreen'
            restartGame(app)

def onKeyRelease(app, key):
    if app.gameState == 'playing':
        if app.character.rotating == True:
            app.character.rotating = False

def onKeyHold(app, keys):
    if app.gameState == 'playing':
        if ('space' in keys or 'w' in keys or 'W' in keys or 'up' in keys) and (app.character.grounded == False):
            app.character.rotating = True
        elif 'escape' in keys:
            app.gameState = 'pause'

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

        if app.character.grounded: 
            setCurrentCurve(app)
            app.character.posOnCurve = findClosestPosOnCurve(app)
            # if not continuous --> launch off
            if app.terrain.continuityList[app.character.currentCurve] == 0:
                slideOff(app)
            # print(f'curve i am currently on has c{app.terrain.continuityList[app.character.currentCurve]} continuity, next has c{app.terrain.continuityList[app.character.currentCurve + 1]} continuity')

            # movement of curve
            # slideCharacter(app)
            app.characterMovementVectX, app.characterMovementVectY = moveCharacter(app)
            app.character.orientation = getOrientation(app)
            if abs(app.character.orientation) > 180:
                app.character.orientation += 180
            moveWorld(app, worldMovementVectX, worldMovementVectY)

        else: 
            moveWorld(app, worldMovementVectX, worldMovementVectY)
            setCurrentCurve(app)
            orientationOfGround = getOrientation(app)
            app.character.posOnCurve = findClosestPosOnCurve(app)
            groundPointApproximate = assignCurvePoint(app, app.character.posOnCurve)
            app.groundPoint = groundPointApproximate
            error = distance(app.character, groundPointApproximate)
            
            if app.characterMovementVectY < app.terminal:
                app.characterMovementVectY += app.gravity # gravity   

            if app.characterMovementVectX > app.speedMax / app.dragLimit:
                app.characterMovementVectX *= 0.99
            
            if app.character.rotating:
                app.character.orientation -= app.character.rotationRate
                app.character.rotatedAmount += app.character.rotationRate
            elif app.character.rotating == False and app.character.rotatedAmount < 180: # should recenter character --> should have an exception tho uhhhhhhhhhhhhhhhhhhh
                app.character.orientation += ((orientationOfGround - app.angleTakeOff) / 30)
                
            # ground collision check
            if groundPointApproximate.y <= app.character.y:
                print('ground collision detected')
                app.character.grounded = True
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
                
                app.character.rotatedAmount = 0
                app.characterMovementVectX = vectX
                app.characterMovementVectY = vectY

                if app.character.orientation < -180:
                    app.character.orientation += 360                
                    # orientation never goes more than 180 degrees and less than -180 degrees
                if (app.character.orientation + 60 < orientationOfGround) or (app.character.orientation - 60 > orientationOfGround):
                    # print(f'character orientation: {app.character.orientation} ground orientation: {orientationOfGround} --> dead')
                    app.gameState = 'dead'
            # moveWorld(app, worldMovementVectX, worldMovementVectY)
                    
            #     # check if it if an over or under estimate in x value
            #     # then check if 
    
    elif app.gameState == 'pause':
        pass

# character movement
def moveCharacter(app):
    print('\n')
    print(app.character.posOnCurve)
    initialPoint = assignCurvePoint(app, app.character.posOnCurve)
    print(f'initial point is; {initialPoint}')

    # closest point may be an under or over estimate - if negative --> overestimate, if positive --> underestimate
    initialDir = -1 if (app.character.x - initialPoint.x) < 0 else 1
    initialError = distance(Point(app.character.x, app.character.y), initialPoint)
    print(f'initial error is: {initialError} in {initialDir} direction')
    
    projectedDistanceMoved = 0
    counter = app.character.posOnCurve

    while projectedDistanceMoved < app.character.speed:
        if counter + 2 >= len(app.terrain.pointsList[app.character.currentCurve]): 
            # character is projected to move between points of next curve
            app.character.currentCurve += 1
            counter = 0
        print(f'curve is: {app.character.currentCurve}  counter is: {counter}')

        # print(counter, counter + 2)
        oneJump = distance(assignCurvePoint(app, counter), assignCurvePoint(app, counter + 2))
        projectedDistanceMoved += oneJump
        print(f'this jump: {oneJump}')
        print(f'distance moved so far: {projectedDistanceMoved}')
        counter += 2

    undershot = assignCurvePoint(app, counter - 2)
    print(f'undershot point is {undershot}')
    overshot = assignCurvePoint(app, counter)
    print(f'overshot point is {overshot}')
    lastJump = oneJump # distance between under and over shot points
    projectedDistanceMoved -= lastJump
    remainingInterPointDistance = app.character.speed - projectedDistanceMoved # the remaining distance the character has to
    print(f'remaining distance that has to be traversed {remainingInterPointDistance}')
    # move between undershot and overshot points (not considering initial error correction)

    # if projectedDistanceMoved == 0: # if the character will be moving only between two points
    #     if initialDir < 0: # if initial position is overestimated --> moving towards undershot
    #         if distance(Point(app.character.x, app.charactery), undershot) < app.character.speed:
    #         # if distance to undershot point is gaming
    #     elif initialDir > 0: # if initial position is underestimated --> moving towards overshot

        

    if initialDir < 0: # if initial position overestimated --> projectedDistanceMoved is an overestimate
        print('overestimated initial point')
        angle = math.atan2((overshot.y - undershot.y), overshot.x - undershot.x)
        vectX = (undershot.x - app.character.x + 
        (remainingInterPointDistance + initialError * initialDir) * math.cos(math.radians(angle)))
        vectY = (undershot.y - app.character.y - 
        (remainingInterPointDistance + initialError * initialDir) * math.sin(math.radians(angle)))
        print(f'Angle: {angle}  X: {vectX},  Y:{vectY}')

        if 

        return vectX, vectY
    elif initialDir > 0: # if initial position underestimated --> projectedDistanceMove is an underestimate
        # check if initial error + undershot correction is larger than distance from undershot to overshot point
        if remainingInterPointDistance + initialError > lastJump:
            print('underestimated initial point, OUTSIDE bounds of under-over')
            if counter + 2 >= len(app.terrain.pointsList[app.character.currentCurve]):
                afterOverShot = Point(app.terrain.pointsList[app.character.currentCurve + 1][0], 
                                      app.terrain.pointsList[app.character.currentCurve + 1][1])
                angle = math.atan2((afterOverShot.y - overshot.y),afterOverShot.x - overshot.x)
            else:
                counter += 2
                afterOverShot = Point(app.terrain.pointsList[app.character.currentCurve][counter], 
                                      app.terrain.pointsList[app.character.currentCurve][counter + 1])
                angle = math.atan2((afterOverShot.y - overshot.y), afterOverShot.x - overshot.x)
            
            remainingDistanceAfterCorrection = lastJump - (remainingInterPointDistance + initialError)
            vectX = overshot.x - app.character.x - remainingDistanceAfterCorrection * math.cos(math.radians(angle))
            vectY = overshot.y - app.character.y - remainingDistanceAfterCorrection * math.sin(math.radians(angle))
            print(f'corrected backwards by: {remainingDistanceAfterCorrection} in {angle} direction')
            print(f'X: {vectX},  Y:{vectY}')
            return vectX, vectY
        
        else: # if not, then the target point is in the middle of the undershot and overshot points
            print('underestimated initial point, within bounds of under-over')
            angle = math.atan2((overshot.y - undershot.y),overshot.x - undershot.x)
            vectX = (undershot.x - app.character.x + 
            (remainingInterPointDistance + initialError * initialDir) * math.cos(math.radians(angle)))
            vectY = (undershot.y - app.character.y - 
            (remainingInterPointDistance + initialError * initialDir) * math.sin(math.radians(angle)))
            print(f'Angle: {angle}  X: {vectX},  Y:{vectY}')
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

    characterPositionX = undershot.x + (overshootingError + initialXError) * math.cos(angle)
    characterPositionY = undershot.y + (overshootingError + initialYError) * math.sin(angle)

    app.characterMovementVectX = characterPositionX - app.character.x
    app.characterMovementVectY = characterPositionY - app.character.y
    print(app.characterMovementVectX, app.characterMovementVectY)
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
    orientation = math.radians(app.character.orientation)
    orientationY = math.radians(app.character.orientation - 90)
    if app.character.orientation > 0:
        app.characterMovementVectX = (app.character.vert + app.character.momentum) * math.cos(orientation)
        app.characterMovementVectY = (app.character.vert) * math.sin(orientation - 90)
    elif app.character.orientation > 20:
        app.characterMovementVectX = (app.character.momentum) * math.cos(orientation)
        app.characterMovementVectY = (app.character.vert) * math.sin(orientationY)
    else:
        app.characterMovementVectX = (app.character.momentum) * math.cos(orientation)
        app.characterMovementVectY = (app.character.vert) * math.sin(orientationY)
    # app.characterMovementVectX = (app.character.momentum) * math.cos(math.radians(app.character.orientation)) + (app.character.vert) * math.cos(math.radians(app.character.orientation - 90))
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
        # drawRect(app.character.x, app.character.y, 15, 7, fill='coral', border=None, borderWidth=2, dashes=False,      
        #             rotateAngle = app.character.orientation, align = 'center')

        drawImage(app.character.linkGrounded, playerImageCenterX, playerImageCenterY+3, 
                  width = app.character.width, height = app.character.width, align = 'center', 
                  rotateAngle = app.character.orientation)
        
        for i in range(len(app.terrain.controlList)):
            firstPoint = app.terrain.controlList[i][0]
            drawCircle(firstPoint.x, firstPoint.y, 10, fill='red')
        # drawLabel(math.floor(app.character.orientation), 30, 30)

    if app.gameState == 'dead':
    #     drawRect(app.character.x, app.character.y, 15, 7, fill='coral', border=None, borderWidth=2, dashes=False,      
    #                 rotateAngle = app.character.orientation, align = 'center')
        drawImage(app.character.linkGrounded, playerImageCenterX, playerImageCenterY+3, 
                  width = app.character.width, height = app.character.width, align = 'center', 
                rotateAngle = app.character.orientation)
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
