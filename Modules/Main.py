from terrain import *
from character import *
from hazards import *
from mainTools import *

import math, time, random

def onAppStart(app):
    # screen instantiations
    app.scale = 75
    app.width = 16 * app.scale
    app.height = 9 * app.scale

    restartGame(app)

    # music and sound FX
    app.adventureSong = Sound('../Music/adventure.mp3')
    app.skiing = Sound('../Music/skiingFX.mp3')
    app.jumping = Sound('../Music/jumpFX.mp3')
    app.landing = Sound('../Music/landingFX.mp3')
    app.hit = Sound('../Music/hit.mp3')
    app.adventureSong.play(restart = True, loop = True)

     # graphics and fonts
    app.fontTitle = 'Bowlby One'
    app.fontBig = 'Domine Bold'
    app.fontMedium = 'Domine Medium'
    app.fontSmall = 'Domine'
    app.textColor = rgb(21, 22, 23)
    app.lightTextColor = rgb(45, 47, 48)

    app.backgroundColors = [rgb(224, 255, 243), rgb(252, 234, 212)]
    app.mountainColors = [rgb(145, 219, 190), rgb(214, 167, 131)]
    app.atmosphericColors = [rgb(0, 252, 156), rgb(255, 115, 0)]
    app.sunBlendingColors = [rgb(222, 242, 170), rgb(252, 215, 146)]

    # selecting color pallete
    app.colorSelect = random.randint(0, len(app.backgroundColors) - 1)

def restartGame(app):
    # physics intializations
    app.score = 0
    app.timeofday = 0
    app.gravity = 0.3
    app.terminal = 20
    app.naturalResistance = 0.2
    app.minSpeed = 10
    app.distanceTraveled = 0

    # game timings  
    app.stepsPerSecond = 60 # fixed cus like 60 frames per second u know
    app.stepNum = 4
    app.gameState = 'startScreen'

    # world + character movement
    app.characterMovementVectX = 15
    app.characterMovementVectY = -5
    app.cameraMove = False

    # initializing terrain
    p1 = Point(0, app.height * 6 / 7)
    p2 = Point(app.width / 4, app.height * 4 / 6)
    p3 = Point(app.width * 3 / 4, app.height * 4 / 6)
    p4 = Point(app.width + 1, app.height * 6 / 7)
    app.rockWidth = 30
    app.terrain = Terrain(p1, p2, p3, p4)
    app.terrain.controlList = []
    app.terrain.pointsList = []
    app.terrain.continuityList = [1]
    app.terrain.curvesPassed = []
    app.terrain.startPreGen(app.width)

    # initializing Austin
    app.character = Character(0, (app.height * 6 / 7) - 200)
    app.character.grounded = False
    app.character.rotating = False
    app.character.orientation = 0
    app.character.speed = 15
    app.speedMax = 50
    app.angleTakeOff = 0
    app.anglePortionToCorrect = 0
    app.groundPoint = None
    app.storedOrientation = 0

    # changing position of character when camera is following character
    app.characterTargetX = app.width/5
    app.characterTargetY = app.height/2
    app.characterToTargetSpeed = 5

    # ui variables
    app.startFade = 0
    app.resetFade = 0
    app.titleX = app.width/2
    app.titleY = app.height/5
    app.titleY2 = app.height/5*4


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
        if (key == 'W' or 'w' or 'space' or 'up') and app.resetFade == 0:
            app.gameState = 'playing'

    elif app.gameState == 'playing':
        if (key == 'W' or key == 'w' or key == 'space' or key == 'up') and app.character.grounded == True:
            app.characterMovementVectY = 0
            app.characterMovementVectX = 0
            app.angleTakeOff = app.character.orientation
            app.jumping.play(restart = True, loop = False)
            jump(app)
            app.character.grounded = False
            moveWorld(app)
        
        if key == 'escape':
            app.gameState = 'pause'
            app.skiing.pause()

    elif app.gameState == 'dead':
        if key:
            app.gameState = 'postDead'

    elif app.gameState == 'pause':
        if key == 'escape':
            app.gameState = 'playing'
            if app.character.grounded == True:
                app.skiing.play(restart = False, loop = True)

def onKeyRelease(app, key):
    if app.gameState == 'playing':
        if app.character.rotating == True:
            app.character.rotating = False
            app.anglePortionToCorrect = app.character.orientation - app.angleTakeOff

def onKeyHold(app, keys):
    if app.gameState == 'playing':
        if ('space' in keys or 'w' in keys or 'W' in keys or 'up' in keys) and (app.character.grounded == False):
            app.character.rotating = True

def onStep(app):
    if app.gameState == 'startScreen':
        if app.startFade < 100:
            app.startFade += 1

    elif app.gameState == 'postDead':
        if app.resetFade < 100:
            app.resetFade += 2
        if app.resetFade >= 100:
            app.gameState = 'startScreen'
            restartGame(app)

    if app.resetFade != 0 and app.gameState == 'startScreen':
        app.resetFade -= 2
            
    elif app.gameState == 'playing':
        if app.character.x >= app.characterTargetX:
            app.cameraMove = True

        app.distanceTraveled += app.character.speed / 100

        app.score += app.character.speed / 300

        # ree
        if app.character.orientation < -180:
            app.character.orientation += 360  

        # detect when need to generate new terrain --> x coordinate of the oldest/first curve is moved past the width of the app
        if app.terrain.controlList[-2][-1].x <= app.width:
            if not app.terrain.curvesPassed[0]:
                app.terrain.fullGenerator(app.width)
                app.terrain.curvesPassed[0] = True

        # detect when curve has passed x = 0 --> controlList[0][-1].x < 0 (or another variable)
        # remove from pointsList, remove from controlList
        # remove all things that move past the left side of the screen, essentially
        if app.terrain.controlList[0][-1].x < 0:
            app.terrain.controlList.pop(0)
            app.terrain.pointsList.pop(0)
            app.terrain.curvesPassed.pop(0)
            app.terrain.continuityList.pop(0)
            app.terrain.rocksList.pop(0)
            app.terrain.treesList.pop(0)
            app.character.currentCurve -= 1

        # character on the ground ############################################################################
        if app.character.grounded: 
            if rockCollisionCheck(app):
                app.skiing.pause()
            else:
                app.skiing.play(restart = False, loop = True)

            if app.character.charging == True:
                app.character.chargingTimer += 1
            if app.character.chargingTimer == 180:
                app.character.charging = False
                app.character.chargingTimer = 0

            app.character.currentCurve = findCurrentCurve(app)
            app.character.posOnCurve = findClosestPosOnCurve(app)

            # if not continuous --> launch off

            # movement along curve --> this is important
            app.characterMovementVectX, app.characterMovementVectY = slideCharacter(app)
            
            curveReCalc = findCurrentCurve(app)
            posReCalc = findClosestPosOnCurve(app)

            if (app.terrain.continuityList[curveReCalc] == 0):
                app.jumping.play(restart = True, loop = False)
                slideOff(app)
                app.character.orientation = app.storedOrientation
            else:
                try:
                    app.character.orientation = getOrientation(app)
                except:
                    pass

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
            
            app.storedOrientation = app.character.orientation

            # movesWorld
            if app.cameraMove == True:
                moveWorld(app)
            else:
                moveCharacter(app)

        # character in the air ##############################################################################3
        elif app.character.grounded == False:

            # initializing important variables
            app.character.currentCurve = findCurrentCurve(app)
            app.character.posOnCurve = findClosestPosOnCurve(app)
            try:
                orientationOfGround = getOrientation(app) 
            except:
                pass
            
            if app.characterMovementVectY < app.terminal:
                app.characterMovementVectY += app.gravity  # gravity   
                app.character.speed += app.gravity * 2 * math.sin(math.radians(app.character.orientation))

            if app.character.speed > app.minSpeed:
                app.character.speed -= app.naturalResistance # air resistance
            
            if app.character.rotating:
                app.character.orientation -= app.character.rotationRate
                app.character.rotatedAmount += app.character.rotationRate
            elif app.character.rotating == False and app.character.rotatedAmount < 180: 
                # should recenter character given that they have not made a half-flip
                if app.character.orientation < app.angleTakeOff:
                    app.character.orientation -= ((app.anglePortionToCorrect) / 100)
            elif app.character.rotating == False and app.character.rotatedAmount > 180:
                app.character.orientation -= 1

            # ground collision check
            vectX, vectY = groundCollisionCheck(app)
            rockCollisionCheck(app)
            
            if vectX != 0 and vectY != 0:
                app.characterMovementVectX = vectX
                app.characterMovementVectY = vectY
                # death check
                if (app.character.orientation + 60 < orientationOfGround) or (app.character.orientation - 60 > orientationOfGround):
                    app.gameState = 'dead'
                else:
                    if app.character.rotatedAmount > 180:
                        app.character.speed += app.character.chargeAmount
                        app.character.charging = True
                        app.score += math.ceil(app.character.rotatedAmount / 360) * 100
                app.character.rotatedAmount = 0
            if app.cameraMove == True:
                moveWorld(app)
            else:
                moveCharacter(app)
    
    elif app.gameState == 'pause':
        pass

# function to move terrain + hazards + platforms + chasers + character
def moveWorld(app, vectX = None, vectY = None):
    if vectX == None and vectY == None:
        vectX = app.characterMovementVectX
        vectY = app.characterMovementVectY

    for curvePoints in app.terrain.pointsList:
        for counter in range(0, len(curvePoints), 2):
            curvePoints[counter] -= vectX
            curvePoints[counter + 1] -= vectY
    for curve in app.terrain.controlList:
        for controlPoint in curve:
            controlPoint.x -= vectX
            controlPoint.y -= vectY
    for curveRocks in app.terrain.rocksList:
        for rock in curveRocks: # list of rock objects
            rock.x -= vectX
            rock.y -= vectY
    for curveTrees in app.terrain.treesList:
        for tree in curveTrees: # list of rock objects
            tree.x -= vectX
            tree.y -= vectY

    app.titleX -= vectX
    app.titleY -= vectY
    app.titleY2 -= vectY

def moveCharacter(app, vectX = None, vectY = None):
    if vectX == None and vectY == None:
        vectX = app.characterMovementVectX
        vectY = app.characterMovementVectY

    app.character.x += vectX
    app.character.y += vectY

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

    mountainGrad = gradient(app.mountainColors[app.colorSelect], app.backgroundColors[app.colorSelect], start = 'top')
    drawPolygon(0, app.height / 6 * 5, app.width / 5, app.height / 7 * 4, app.width / 2, app.height / 3, 
                app.width / 9 * 7, app.height / 2, app.width, app.height / 6 * 5, fill = mountainGrad)

    # draw trees
    for treeList in app.terrain.treesList[:drawTo]:
        for tree in treeList:
            if tree.x + tree.width / 2 > 0:
                treeBase = tree.y + 50
                drawPolygon(tree.x - tree.width/2, treeBase, 
                        tree.x + tree.width / 2, treeBase, 
                        tree.x, treeBase - tree.height, fill = rgb(53, 74, 61))            
    
    # the terrain!
    anchorStart = [0, app.height]
    anchorEnd = [app.width, app.height]

    drawPolygon(*anchorStart, *drawnpointsList, *anchorEnd, fill = 'white')

    imageOffsetAngle = app.character.orientation - 90

    if ((app.gameState == 'startScreen' or app.gameState == 'prePlay' or app.gameState == 'playing' or 
         app.gameState == 'pause' or app.gameState == 'dead')) and app.titleX > -app.width:
        drawLabel("AUSTIN'S", app.titleX, app.titleY, align = 'center', size = 135, 
                  font = app.fontTitle, bold = True, fill = app.textColor, opacity = app.startFade)
        drawLabel("ADVENTURE", app.titleX, app.titleY + 110, align = 'center', size = 100, 
                  font = app.fontTitle, bold = False, fill =app.textColor, opacity = app.startFade)
        drawLabel("Press any key to play", app.titleX, app.titleY2, align = 'center', size = 15, 
                  font = app.fontSmall, bold = False, fill =app.textColor, opacity = app.startFade)
        drawLabel("Press w, space, or the up arrow key to jump - hold to flip", app.titleX, app.titleY2 + 20, align = 'center', size = 15, 
                  font = app.fontSmall, bold = False, fill =app.textColor, opacity = app.startFade)
        drawLabel("Flip to build speed! Ski and flip to get points", app.titleX, app.titleY2 + 40, align = 'center', 
                  size = 15, font = app.fontSmall, bold = False, fill = app.textColor, opacity = app.startFade)
        drawLabel("~ Carpe Diem ~", app.titleX, app.titleY2 + 60, align = 'center', 
                  size = 15, font = app.fontSmall, bold = False, fill = app.textColor, opacity = app.startFade)

    if app.gameState == 'playing' or app.gameState == 'dead' or app.gameState == 'pause' or app.gameState == 'postDead':
        if app.character.grounded == True:
            playerImage = app.character.linkGrounded
        elif app.character.grounded == False:
            playerImage = app.character.linkUnGrounded
        
        if app.character.rotating == True:
            playerImage = app.character.linkRotating

        # draw player -->
        playerImageCenterX = app.character.x + app.character.width/2 * math.cos(math.radians(imageOffsetAngle))
        playerImageCenterY = app.character.y + app.character.height/2 * math.sin(math.radians(imageOffsetAngle))
        imagewidth, imageheight = getImageSize(playerImage)
        imageheight = imageheight * 30 / imagewidth
        imagewidth = 30

        drawImage(playerImage, playerImageCenterX, playerImageCenterY + 4, 
                  width = imagewidth, height = imageheight, align = 'center', 
                  rotateAngle = app.character.orientation)
        
        drawLabel(f"{math.floor(app.distanceTraveled)}m", app.width - 30, 40, align = 'right', 
                  size = 30, font = app.fontSmall, bold = False, fill = app.textColor)
        drawLabel(f"{math.floor(app.score)}", app.width - 30, 70, align = 'right', 
                  size = 15, font = app.fontSmall, bold = False, fill = app.lightTextColor)
        
    # drawing rocks
    for rocklist in app.terrain.rocksList[:drawTo]:
        for rock in rocklist:
            imagewidth, imageheight = getImageSize(rock.image)
            imageheight = imageheight * rock.size / imagewidth
            imagewidth = rock.size

            rockOffsetAngle = rock.orientation - 90
            rockImageCenterX = rock.x + imagewidth/2 * math.cos(math.radians(rockOffsetAngle))
            rockImageCenterY = rock.y + imageheight/2 * math.sin(math.radians(rockOffsetAngle))

            drawImage(rock.image, rockImageCenterX, rockImageCenterY, width = imagewidth, height = imageheight, 
                    align = 'center', rotateAngle = rock.orientation)
    
    if app.gameState == 'dead' or app.gameState == 'postDead':
        drawLabel("Back to UHS", app.width/2, app.height/5 , align = 'center', size = 100, font = app.fontTitle, bold = True)
        drawLabel(f"Distance Traveled: {math.floor(app.distanceTraveled)}m", app.width/2, app.height / 4 + 50, align = 'center', 
                  size = 30, font = app.fontSmall, bold = False, fill = app.textColor)
        drawLabel(f"Score: {math.floor(app.score)}", app.width/2, app.height / 4 + 90, align = 'center', 
                  size = 30, font = app.fontSmall, bold = False, fill = app.textColor)

    if app.gameState == 'pause':
        drawLabel("Paused", app.width/2, app.height/5 , align = 'center', size = 100, font = app.fontTitle, bold = True)

    # restart layer
    if app.gameState != 'playing':
        drawRect(0, 0, app.width, app.height, fill=app.textColor, opacity = app.resetFade)

    # atmospheric layer on top
    sunGrad = gradient(rgb(255, 252, 201), app.atmosphericColors[app.colorSelect], start = 'left-top')
    drawRect(0, 0, app.width, app.height, fill = sunGrad, opacity = 10)

def main():
    runApp()

main()
