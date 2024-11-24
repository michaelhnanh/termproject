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

    x = app.width / 2
    y = app.height * 5 / 6
    app.character = Character()
    
    # would be constrained when grounded but freed when grounded == False

def onKeyPress(app, key):
    if app.gameState == 'startScreen':
        if key:
            slideButtons() # moves buttons off screen
            time.sleep(2)
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
        if key == 'w':
            
        elif key == 's':

        elif key == 'a':

        elif key == 'd':


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
        # detect when need to generate new terrain --> controlList[0][0].x < 0

        # controlPointGenerator takes in p3, p4, and width
        # --> spits out 4 new control points --> add to a list --> add list to controlList

        # feed control points into genCurve --> spits out list of points for drawing
        # append to pointList

        # detect when curve has passed x = 0 --> controlList[0][-1].x < app.width (or another variable)
        # remove from pointList, remove from controlList

        # detecting when to generate and when to remove is easy --> detect when 


    elif app.gameState == 'pause':
        pass

# function to move terrain + hazards + platforms + chasers 
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

    # terrain --> draw polygon that is shifting and stuff

    # overlays --> slide to the outside and disappear when game starts

    if app.gameState == 'startScreen':
        drawImage() # logo
        drawLabel('Press any key to play', ) 
            # settings
        drawImage()
        drawLabel('Settings')
            # character select
        drawImage()
        drawLabel('Characters')
    if app.gameState == 'playing':
        drawImage() # logo
        drawLabel('Press any key to play', ) 
            # settings
        drawImage()
        drawLabel('Settings')
            # character select
        drawImage()
        drawLabel('Characters')

    if app.gameState == 'pause':
        # overlay pause screen on top
        pass

# superfluous UI things
def slideButtons():
    pass

def main():
    runApp()

main()
