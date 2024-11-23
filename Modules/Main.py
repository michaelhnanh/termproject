from terrain import *
from background import *
from character import *
from chasers import *
from hazards import *
from platforms import *

def onAppStart(app):
    scale = 75
    app.width = 16 * scale
    app.height = 9 * scale
    app.score = 0
    app.character = 0 # default character - austin!
    app.timeofday = 0
    app.death = False

    app.grounded = True # whether or not austin is skating
    app.orientation = 0 # the angle that austin is at 
    
    # would be constrained when grounded but freed when grounded == False


############################################################
# Start Screen

def start_redrawAll(app):
    drawLabel()

def start_onKeyPress(app, key):
    setActiveScreen('game')

############################################################
# Game Screen

def game_onScreenActivate(app):
    pass

def game_redrawAll(app):
    
    pass

def game_onKeyPress(app, key):
    # up/space to jump
    # down to drop
    pass

def game_onKeyHold(app, key):
    # hold up/space to increase orientation/to backflip
    pass

def onStep(app):
    pass

############################################################
# Death Screen

def death_redrawAll(app):
    pass
            
############################################################
# Character Selection Screen

def select_redrawAll(app):
    pass

############################################################
# Settings Screen

def settings_redrawAll(app):
    pass

############################################################


def main():
    runAppWithScreens(initialScreen='start')

main()
