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
    app.stepsPerSecond = 10
    app.gameState = 'startScreen'

    # world movement
    app.moveWorldVectX = 0
    app.moveWorldVectY = 0

    p1 = Point(0, app.height * 6 / 7)
    p2 = Point(app.width / 4, app.height * 4 / 6)
    p3 = Point(app.width * 3 / 4, app.height * 4 / 6)
    p4 = Point(app.width + 1, app.height * 6 / 7)
    app.terrain = Terrain(p1, p2, p3, p4)

    x = app.width / 2
    y = app.height * 5 / 6
    app.character = Character(2, 5)
    
    # would be constrained when grounded but freed when grounded == False

def onKeyPress(app, key):
    if app.gameState == 'startScreen':
        if key:
            app.terrain.startPreGen(app.width)
            app.gameState = 'playing'
            print(app.gameState)

    elif app.gameState == 'playing':
        # if key == 'space' or key == 'w' or key == 'W' or key == 'up':
        #     app.character.grounded = False
        #     app.character.jump()
        # elif key == 'escape':
        #     app.gameState = 'pause'
        # if app.character.platformed:
        #     if key == 'down' or key == 's' or key == 'S':
        #         app.character.drop()

        # terrain testing nav:
        if key == 'w':
            app.moveWorldVectX = 0
            app.moveWorldVectY = -100
        elif key == 's':
            app.moveWorldVectX = 0
            app.moveWorldVectY = 100
        elif key == 'a':
            app.moveWorldVectX = -100
            app.moveWorldVectY = 0
        elif key == 'd':
            app.moveWorldVectX = 100
            app.moveWorldVectY = 0

    elif app.gameState == 'dead':
        if key == 'escape':
            app.gameState = 'exit'
    

def onKeyRelease(app, key):
    if app.gameState == 'playing':
        # if (key == 'space' or key == 'w' or key == 'W' or key == 'up') and app.character.grounded == False:
        #     app.character.rotating = False
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
    # if app.gameState == 'playing':
    #     if ('space' or 'w' or 'W' or 'up' in keys) and app.grounded == False:
    #         app.character.rotating = True
    #         app.character.rotate()
    pass

def onMousePress(app, mouseX, mouseY):
    pass

def onStep(app):
    if app.gameState == 'playing':

        moveWorld(app)

        # detect when need to generate new terrain --> x coordinate of the oldest/first curve is moved past the width of the app
        if app.terrain.controlList[0][-1].x <= app.width: # detection works --> need to limit it to drawing ONE
            if not app.terrain.curvesPassed[0]:
                print('\n0th curve has been passed\n')
            # if app.curvespassed[]
                app.terrain.fullGenerator(app.width)
                app.terrain.curvesPassed[0] = True

        # detect when curve has passed x = 0 --> controlList[0][-1].x < 0 (or another variable)
        # remove from pointList, remove from controlList
        if app.terrain.controlList[0][-1].x < 0:
            app.terrain.controlList.pop(0)
            app.terrain.pointList.pop(0)
            app.terrain.curvesPassed.pop(0)
            print('\n0th curve removed\n')

    elif app.gameState == 'pause':
        pass

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
        if p1.x <= app.width and p1.x <= app.height:
            drawTo += 1

    drawnPointList = []
    validPoints = app.terrain.pointList[:drawTo] # drawn points is 2d list
    for points in validPoints: # point is a list
        drawnPointList.extend(points)
            
    anchorStart = [0, 2000] # has to be [x,y] to be placed into drawPolygon, y determined by last controlpoint
    anchorEnd = [app.width, 2000]

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

def main():
    runApp()

main()
