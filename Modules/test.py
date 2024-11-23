from cmu_graphics import *

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

def redrawAll(app):
    Polygon(25, 25, 150, 25, 200, 200, 100, 250, 25, 200)

def main():
    runApp()

main()