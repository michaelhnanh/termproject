from terrain import *
from background import *
from character import *
from chasers import *
from hazards import *
from platforms import *

import math, time, random, functools

def onAppStart(app):
    scale = 75
    app.width = 16 * scale
    app.height = 9 * scale
    app.score = 0
    app.timeofday = 0
    app.gravity = 10

    # superfluous things
    app.settings = Point(app.width * 1 / 8, app.height * 1 / 7)
    app.characterSelect = Point(app.width * 7 / 8, app.height * 1 / 7)

    # game timings
    app.stepsPerSecond = 60 # fixed cus like 60 frames per second u know
    app.gameState = 'startScreen'

    # world movement
    app.characterMovementVectX = 0
    app.characterMovementVectY = 0

    p1 = Point(0, app.height * 6 / 7)
    p2 = Point(app.width / 4, app.height * 4 / 6)
    p3 = Point(app.width * 3 / 4, app.height * 4 / 6)
    p4 = Point(app.width + 1, app.height * 6 / 7)
    app.terrain = Terrain(p1, p2, p3, p4)

    app.character = Character(600, 482) # placeholder positions
    app.character.grounded = True
    app.character.rotating = False


def onKeyPress(app, key):
    if app.gameState == 'startScreen':
        if key:
            app.terrain.startPreGen(app.width)
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
        # if (key == 'space' or key == 'w' or key == 'W' or key == 'up') and app.character.grounded == False:
        #     app.character.rotating = False
        # if key == 'w':
        #     app.moveWorldVectX = 0
        #     app.moveWorldVectY = 0
        # elif key == 's':
        #     app.moveWorldVectX = 0
        #     app.moveWorldVectY = 0
        # elif key == 'a':
        #     app.moveWorldVectX = 0
        #     app.moveWorldVectY = 0
        # elif key == 'd':
        #     app.moveWorldVectX = 0
        #     app.moveWorldVectY = 0
        # print(app.terrain.controlList)
        pass
        

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
        pass

def onMousePress(app, mouseX, mouseY):
    pass

def onStep(app):
    if app.gameState == 'playing':
        
        moveWorld(app)

        # detect when need to generate new terrain --> x coordinate of the oldest/first curve is moved past the width of the app
        if app.terrain.controlList[-2][-1].x <= app.width:
             # detection works --> need to limit it to drawing ONE
            if not app.terrain.curvesPassed[0]:
                print('\ncurve that just passed: ',app.terrain.controlList[0])
            # if app.curvespassed[]
                app.terrain.fullGenerator(app.width)
                app.terrain.curvesPassed[0] = True

        # detect when curve has passed x = 0 --> controlList[0][-1].x < 0 (or another variable)
        # remove from pointList, remove from controlList
        if app.terrain.controlList[0][-1].x < 0:
            print('\ncurve removed: ',app.terrain.controlList[0])
            app.terrain.controlList.pop(0)
            app.terrain.pointList.pop(0)
            app.terrain.curvesPassed.pop(0)
            print('\n0th curve removed\n')

            # initial option was to use the derivative of the curve the player was on and naively move player in that direction
            # * player speed. This could lead to the player overshooting and falling out of the curve. 
            # revisiting this, however, this could be avoided with some ease.
            # taking the naive approximation of the player's position,
            # onstep could actually look forward in pointsList to find the closest point to this approximation
                # onstep could at the series of points until the next point gets farther away from the approximation
            # we could then accept this point as the next position --> or we could...

            # actually scratch that we could just add the distances between the points until it goes over the "distance"
            # the player is supposed to travel. The average between the overshooting point (pn) and pn-1 can then be averaged...
            # or the remaining distance the player has to travel after pn-1 can be calculated, 
            # the tangent of pn-1 can be calculated, and the player can then be placed there.

            # this could be made very accurate by reparametrizing the points to be evenly spaced in every curve --> do that later
        
        # make character slide to positionX and positionY calculations first btw
        
        if app.character.grounded:
            satisfied = False
            currentPoint = app.terrain.pointsList[0][0]
            difference = distance(currentPoint, app.character.pos)
            i = 1
            while satisfied == False:
                currentPoint = app.terrain.pointsList[0][i]
                newDifference = distance(currentPoint, app.character.pos)
                if newDifference > difference: 
                    satisfied = True
                    i -= 1
                else:
                    i += 1
            
            
            
            currentPos = Point(app.character.x, app.character.y)
            app.character.speed
            distanceTotal = 0
            pn = None
            while distanceTotal < app.character.speed:
                
            

        else:
            pass
        
        

    elif app.gameState == 'pause':
        pass

def findStartinPosition(app):

# function to move terrain + hazards + platforms + chasers

def moveWorld(app):
    # if app.moveWorldVectX != 0 or app.moveWorldVectY != 0:
    for curvePoints in app.terrain.pointList:
        for counter in range(0, len(curvePoints), 2):
            curvePoints[counter] -= app.moveWorldVectX
            curvePoints[counter + 1] -= app.moveWorldVectY 
    for curve in app.terrain.controlList:
        for controlPoint in curve:
            controlPoint.x -= app.moveWorldVectX
            controlPoint.y -= app.moveWorldVectY

def redrawAll(app):
    # background --> draw series of shifting polygons

    # terrain --> draw polygon --> select which curves to draw based on the position of 
    # control points unpack selected pointList indexes into drawPolygon, starting and ending with anchor points
    drawTo = 1
    for index in range(1, len(app.terrain.controlList)):
        p1 = app.terrain.controlList[index][0]
        if p1.x <= app.width and p1.y <= app.height:
            drawTo += 1

    drawnPointList = []
    validPoints = app.terrain.pointList[:drawTo] # drawn points is 2d list
    for points in validPoints: # point is a list
        drawnPointList.extend(points)
            
    anchorStart = [0, app.height] # has to be [x,y] to be placed into drawPolygon, y determined by last controlpoint
    anchorEnd = [app.width, validPoints[-1][-1].y]

    drawPolygon(*anchorStart, *drawnPointList, *anchorEnd, fill = 'lightgreen')

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
