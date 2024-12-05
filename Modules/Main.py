from terrain import *
from background import *
from character import *
from chasers import *
from hazards import *
from platforms import *
from mainTools import *

import math, time, random

def onAppStart(app):
    app.scale = 75
    app.width = 16 * app.scale
    app.height = 9 * app.scale
    app.score = 0
    app.timeofday = 0
    app.gravity = 0.3
    app.terminal = 20
    app.naturalResistance = 0.2
    app.minSpeed = 10
    app.distanceTraveled = 0
    app.score = 0

    app.fontTitle = 'Bowlby One'
    app.fontBig = 'Domine Bold'
    app.fontMedium = 'Domine Medium'
    app.fontSmall = 'Domine'
    app.textColor = rgb(21, 22, 23)
    app.backgroundColors = [rgb(203, 245, 229), rgb(250, 224, 192)]
    app.atmosphericColors = [rgb(0, 252, 156), rgb(255, 115, 0)]

    app.colorSelect = random.randint(0, len(app.backgroundColors) - 1)

    # game timings  
    app.stepsPerSecond = 60 # fixed cus like 60 frames per second u know
    app.stepNum = 4
    app.gameState = 'startScreen'

    # world movement
    app.characterMovementVectX = 15
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
    app.speedMax = 50
    app.angleTakeOff = 0
    app.anglePortionToCorrect = 0
    app.groundPoint = None
    app.storedOrientation = 0

    # ui variables
    app.startFade = 0

    app.resetFade = 0

    # 

    app.settings = Point(app.width * 1 / 8, app.height * 1 / 7)
    app.characterSelect = Point(app.width * 7 / 8, app.height * 1 / 7)

    app.adventureSong = Sound('../Music/adventure.mp3')
    app.skiing = Sound('../Music/skiingFX.mp3')
    app.jumping = Sound('../Music/jumpFX.mp3')
    app.adventureSong.play(restart = True)

def restartGame(app):
    app.score = 0
    app.timeofday = 0
    app.gravity = 0.3
    app.terminal = 20
    app.naturalResistance = 0.2
    app.minSpeed = 10
    app.distanceTraveled = 0
    app.score = 0

    app.moveWorldVectX = 0
    app.moveWorldVectY = 0
    app.characterMovementVectX = 15
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
    app.speedMax = 50
    app.angleTakeOff = 0
    app.anglePortionToCorrect = 0
    app.groundPoint = None
    app.storedOrientation = 0

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
            app.gameState = 'prePlay'

    elif app.gameState == 'playing':
        if (key == 'W' or key == 'w' or key == 'space' or key == 'up') and app.character.grounded == True:
            app.characterMovementVectY = 0
            app.characterMovementVectX = 0
            app.angleTakeOff = getOrientation(app)
            app.jumping.play(restart = True, loop = False)
            jump(app)
            app.speedMax = app.characterMovementVectX
            app.character.grounded = False
            moveWorld(app)
        if key == 'escape':
            if app.gameState == 'playing':
                app.gameState = 'pause'
                print('paused')
            if app.gameState == 'pause':
                app.gameState = 'playing'
                print('playing')

    elif app.gameState == 'dead':
        if key:
            app.gameState = 'startScreen'
            restartGame(app)

    elif app.gameState == 'pause':
        if key == 'escape':
            app.gameState = 'playing'
            print('playing')

def onKeyRelease(app, key):
    if app.gameState == 'playing':
        if app.character.rotating == True:
            app.character.rotating = False
            app.anglePortionToCorrect = app.character.orientation - app.angleTakeOff

def onKeyHold(app, keys):
    if app.gameState == 'playing':
        if ('space' in keys or 'w' in keys or 'W' in keys or 'up' in keys) and (app.character.grounded == False):
            app.character.rotating = True
        elif 'escape' in keys:
            app.gameState = 'pause'

def onMousePress(app, mouseX, mouseY):
    pass

def onStep(app):
    if app.gameState == 'startScreen':
        if app.startFade < 100:
            app.startFade += 1
    elif app.gameState == 'prePlay':
        if app.startFade > 0:
            app.startFade -= 1
        if app.startFade <= 0:
            # preGame alto enters sequence
            app.gameState = 'playing'

    elif app.gameState == 'playing':
        app.distanceTraveled += app.character.speed / 100
        worldMovementVectX = 0
        worldMovementVectY = 0
        if app.character.orientation < -180:
            app.character.orientation += 360  

        # detect when need to generate new terrain --> x coordinate of the oldest/first curve is moved past the width of the app
        if app.terrain.controlList[-2][-1].x <= app.width:
            if not app.terrain.curvesPassed[0]:
                app.terrain.fullGenerator(app.width)
                app.terrain.curvesPassed[0] = True

        # detect when curve has passed x = 0 --> controlList[0][-1].x < 0 (or another variable)
        # remove from pointsList, remove from controlList
        if app.terrain.controlList[0][-1].x < 0:
            app.terrain.controlList.pop(0)
            app.terrain.pointsList.pop(0)
            app.terrain.curvesPassed.pop(0)
            app.terrain.continuityList.pop(0)
            app.character.currentCurve -= 1

        if app.character.grounded: 
            app.skiing.play(restart = False, loop = True)

            if app.character.charging == True:
                app.character.chargingTimer += 1
            if app.character.chargingTimer == 180:
                app.character.charging = False
                app.character.chargingTimer = 0

            app.character.currentCurve = findCurrentCurve(app)
            app.character.posOnCurve = findClosestPosOnCurve(app)

            app.character.orientation = getOrientation(app)

            # if not continuous --> launch off

            # movement along curve --> this is important
            app.characterMovementVectX, app.characterMovementVectY = moveCharacter(app)
            
            curveReCalc = findCurrentCurve(app)
            posReCalc = findClosestPosOnCurve(app)


            if (app.terrain.continuityList[curveReCalc] == 0):
                app.jumping.play(restart = True, loop = False)
                slideOff(app)
                app.character.orientation = app.storedOrientation
            else:
                app.character.orientation = getOrientation(app)

            # changing orientation of player character

            if abs(app.character.orientation) > 180:
                app.character.orientation += 180

            # momentum calculations
            app.character.speed += app.gravity * 1.5 * math.sin(math.radians(app.character.orientation))
                # as orientation becomes negative as character tilts upwards, 
                # it can actually be used to slow down character when going up slopes --> great
            app.character.speed -= app.naturalResistance  # friction + air resistance

            if app.character.speed < app.minSpeed:
                app.character.speed = app.minSpeed
            # never dip below a certain amount or the game stops...
            
            # movesWorld
            app.storedOrientation = app.character.orientation
            moveWorld(app)
        elif app.character.grounded == False:
            # initializing important variables
            app.character.currentCurve = findCurrentCurve(app)
            app.character.posOnCurve = findClosestPosOnCurve(app)
            orientationOfGround = getOrientation(app)  
            
            if app.characterMovementVectY < app.terminal:
                app.characterMovementVectY += app.gravity  # gravity   
                app.character.speed += app.gravity * 2 * math.sin(math.radians(app.character.orientation))

            app.character.speed -= app.naturalResistance # friction + air resistance
            # app.characterMovementVectX -= app.naturalResistance

            if app.character.speed < app.minSpeed:
                app.character.speed = app.minSpeed
            
            if app.character.rotating:
                app.character.orientation -= app.character.rotationRate
                app.character.rotatedAmount += app.character.rotationRate
            elif app.character.rotating == False and app.character.rotatedAmount < 180: # should recenter character --> should have an exception tho uhhhhhhhhhhhhhhhhhhh
                if app.character.orientation < app.angleTakeOff:
                    app.character.orientation -= ((app.anglePortionToCorrect) / 100)

            # ground collision check
            vectX, vectY = groundCollisionCheck(app)
            
            if vectX != 0 and vectY != 0:
                app.characterMovementVectX = vectX
                app.characterMovementVectY = vectY
                # death check
                if (app.character.orientation + 45 < orientationOfGround) or (app.character.orientation - 45 > orientationOfGround):
                    app.gameState = 'dead'
                else:
                    if app.character.rotatedAmount > 180:
                        app.character.speed += app.character.chargeAmount
                        app.character.charging = True
                app.character.rotatedAmount = 0
            moveWorld(app)
    
    elif app.gameState == 'pause':
        pass

def jump(app):
    app.character.charging = False
    orientation = math.radians(-app.character.orientation)
    orientationY = math.radians(app.character.orientation - 90)

    app.characterMovementVectX = (app.character.speed) * math.cos(orientation)
    app.characterMovementVectY = (app.character.vert) * math.sin(orientationY)
    app.skiing.pause()
    
def slideOff(app):
    app.character.grounded = False
    app.terrain.continuityList[app.character.currentCurve] = 1
    orientation = math.radians(-app.storedOrientation)

    app.characterMovementVectX = (app.character.speed) * math.cos(orientation)
    app.characterMovementVectY = -1 * (app.character.speed) * math.sin(orientation)
    app.character.rotating = False
    app.anglePortionToCorrect = 0
    app.skiing.pause()

# function to move terrain + hazards + platforms + chasers + character
def moveWorld(app):
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
    drawRect(0, 0, app.width, app.height, fill=app.backgroundColors[app.colorSelect])

    drawTo = 1
    for index in range(1, len(app.terrain.controlList)):
        p1 = app.terrain.controlList[index][0]
        if p1.x <= app.width and p1.y <= app.height:
            drawTo += 1

    drawnpointsList = []
    validPoints = app.terrain.pointsList[:drawTo] # drawn points is 2d list
    for points in validPoints: # point is a list
        drawnpointsList.extend(points)
            
    anchorStart = [0, app.height]
    anchorEnd = [app.width, app.height]

    # the terrain!
    drawPolygon(*anchorStart, *drawnpointsList, *anchorEnd, fill = 'white')

    imageOffsetAngle = app.character.orientation - 90
    
    playerImageCenterX = app.character.x + app.character.width/2 * math.cos(math.radians(imageOffsetAngle))
    playerImageCenterY = app.character.y + app.character.height/2 * math.sin(math.radians(imageOffsetAngle))

    if app.gameState == 'startScreen' or app.gameState == 'prePlay':
        drawLabel("AUSTIN'S", app.width/2, app.height/5, align = 'center', size = 135, 
                  font = app.fontTitle, bold = True, fill = app.textColor, opacity = app.startFade)
        drawLabel("ADVENTURE", app.width/2, app.height/5 + 110, align = 'center', size = 100, 
                  font = app.fontTitle, bold = False, fill =app.textColor, opacity = app.startFade)
        drawLabel("Press any key to play", app.width/2, app.height/5*4, align = 'center', size = 15, 
                  font = app.fontSmall, bold = False, fill =app.textColor, opacity = app.startFade)
        drawLabel("Press W, space, or the up arrow key to jump/flip", app.width/2, app.height/5*4 + 18, align = 'center', size = 15, 
                  font = app.fontSmall, bold = False, fill =app.textColor, opacity = app.startFade)
        drawLabel("Hold to flip", app.width/2, app.height/5*4 + 36, align = 'center', 
                  size = 15, font = app.fontSmall, bold = False, fill = app.textColor, opacity = app.startFade)

    elif app.gameState == 'playing' or app.gameState == 'dead':
        if app.character.grounded == True:
            playerImage = app.character.linkGrounded
        elif app.character.grounded == False:
            playerImage = app.character.linkUnGrounded
        
        if app.character.rotating == True:
            playerImage = app.character.linkRotating

        imagewidth, imageheight = getImageSize(playerImage)
        imageheight = imageheight * 30 / imagewidth
        imagewidth = 30

        drawImage(playerImage, playerImageCenterX, playerImageCenterY + 4, 
                  width = imagewidth, height = imageheight, align = 'center', 
                  rotateAngle = app.character.orientation)

        drawLabel(f"{math.floor(app.distanceTraveled)}m", app.width - 30, 40, align = 'right', 
                  size = 30, font = app.fontSmall, bold = False, fill = app.textColor)

    if app.gameState == 'dead':
        drawLabel("Back to UHS", app.width/2, app.height/5 , align = 'center', size = 100, font = app.fontTitle, bold = True)

    # overlays --> slide to the outside and disappear when game starts

    # if app.gameState == 'pause':
        # overlay pause screen on top
                    
    # drawLabel(f'orientation: {math.floor(app.character.orientation)}', 80, 30)
    # drawLabel(f'speed: {math.floor(app.character.speed)}', 80, 45)
    # drawLabel(f'rotated amount: {math.floor(app.character.rotatedAmount)}', 80, 60)

    # atmospheric layer on top
    drawRect(0, 0, app.width, app.height, fill=app.atmosphericColors[app.colorSelect], opacity = 10)

# superfluous UI things

def main():
    runApp()

main()
