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
    app.character = 0 # default character - austin!
    app.timeofday = 0
    app.gravity = 10

    # superfluous things
    app.settings = Point(app.width * 1 / 8, app.height * 1 / 7)
    app.characterSelect = Point(app.width * 7 / 8, app.height * 1 / 7)

    # game timings
    app.stepsPerSecond = 100
    app.gameState = 'startScreen'

    # world movement
    app.worldMoveVectX = None
    app.worldMoveVectY = None

    p1 = Point(0, app.height * 6 / 7)
    p2 = Point(app.width / 4, app.height * 4 / 6)
    p3 = Point(app.width * 3 / 4, app.height * 4 / 6)
    p4 = Point(app.width, app.height * 6 / 7)
    app.terrain = Terrain(p1, p2, p3, p4)

    # x = app.width / 2
    # y = app.height * 5 / 6
    # app.character = Character()
    
    # would be constrained when grounded but freed when grounded == False

def onKeyPress(app, key):
    if app.gameState == 'startScreen':
        if key:
            slideButtons() # moves buttons off screen
            time.sleep(2)
            app.terrain.startPreGen(app.width)
            app.gameState == 'playing'

    elif app.gameState == 'playing':
        # if key == 'space' or key == 'w' or key == 'W' or key == 'up':
        #     app.character.grounded = False
        #     app.character.jump()
        # elif key == 'escape':
        #     app.gameState == 'pause'
        # if app.character.platformed:
        #     if key == 'down' or key == 's' or key == 'S':
        #         app.character.drop()

        # terrain testing nav:
        # if key == 'w':
            
        # elif key == 's':

        # elif key == 'a':

        # elif key == 'd':
        pass


    elif app.gameState == 'dead':
        if key == 'escape':
            app.gameState == 'exit'
    

def onKeyRelease(app, key):
    if app.gameState == 'playing':
        if (key == 'space' or key == 'w' or key == 'W' or key == 'up') and app.character.grounded == False:
            app.character.rotating = False

def onKeyHold(app, keys):
    if app.gameState == 'playing':
        if ('space' or 'w' or 'W' or 'up' in keys) and app.grounded == False:
            app.character.rotating = True
            app.character.rotate()

def onMousePress(app, mouseX, mouseY):
    # settings
    # if 

    # # 
    # if 

    # if 
    pass

def onStep(app):
    if app.gameState == 'startScreen':
        pass
    elif app.gameState == 'playing':
        if app.character.rotating == False:
            app.character.reCenter()

        # terrain generation loop
        # detect when need to generate new terrain --> controlList[0][-1].x < app.width
        if app.terrain.controlList[0][-1].x <= app.width:
            app.terrain.fullGenerator(app.width)

        # detect when curve has passed x = 0 --> controlList[0][-1].x < 0 (or another variable)
        # remove from pointList, remove from controlList
        if app.terrain.controlList[0][-1].x < 0:
            app.terrain.controlList.pop(0)
            app.terrain.pointList.pop(0)

    elif app.gameState == 'pause':
        pass

# function to move terrain + hazards + platforms + chasers 
@functools.cache
def moveWorld():
    if app.worldMoveVectX != 0 or app.worldMoveVectY != 0:
        for counter in range(0, len(app.terrain.curveList) + 1, 2):
            app.terrain.pointlist[counter] += app.worldMoveVectX
            app.terrain.pointlist[counter + 1] += app.worldMoveVectY 
        for point in app.terrain.controlList:
            point.x += app.worldMoveVectX
            point.y += app.worldMoveVectY

def redrawAll(app):
    # background --> draw series of shifting polygons

    # terrain --> draw polygon --> select which curves to draw based on the position of 
    # control points unpack selected pointList indexes into drawPolygon, starting and ending with anchor points
    # draw 0th curve of course
    # repeatedly check 
    drawTo = 1
    for index in range(1, len(app.terrain.controlList)):
        p1 = app.terrain.controlList[index][0]
        if p1.x <= app.width and p1.x <= app.height:
            drawTo += 1
            print('1')
    curveList = []
    curves = app.terrain.pointList[:drawTo]
    for curve in curves:
        curveList.extend(curve)
            
    anchorStart = [0, 2000] # has to be [x,y] to be placed into drawPolygon, y determined by last controlpoint
    anchorEnd = [app.width, 2000]

    drawPolygon(*anchorStart, *curveList, *anchorEnd)

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
def slideButtons():
    pass

def main():
    runApp()

main()
