from cmu_graphics import *
import math
from tools import *

def onAppStart(app):
    app.width = 500
    app.height = 500

    app.t = 0
    app.speed = 0.05
    app.quadpos = [point(50,50), point(250,600), point(450,100)]

    app.quadcurve = []

    genCurve(app)
    

####################################################################### 
# https://github.com/Josephbakulikira/Bezier-Curve-animation-using-python/blob/master/curves.py

def linearCurve(point1, point2, t, color, trigger = True):
    P1_x = (1 - t) * point1.x
    P1_y = (1 - t) * point1.y

    P2_x = t * point2.x
    P2_y = t * point2.y

    curve = point(P1_x + P2_x, P1_y + P2_y)

    if trigger:
        drawLine(point1.x, point1.y, point2.x, point2.y, fill=color, lineWidth = 2)
        drawLine(point1.x, point1.y, curve.x, curve.y, fill=color, lineWidth = 2)
        curve.display(8)
        return curve
    else:
        curve.display(8)
        return curve


def quadraticCurve(point1, point2, point3, t, color, curveList, trigger = True):
    P1_x = (1 - t) ** 2 * point1.x
    P1_y = (1 - t) ** 2 * point1.y

    P2_x = 2 * (1 - t) * t * point2.x
    P2_y = 2 * (1 - t) * t * point2.y

    P3_x = t ** 2 * point3.x
    P3_y = t ** 2 * point3.y

    curve = point(P1_x + P2_x + P3_x, P1_y + P2_y + P3_y)

    # if trigger:
    #     drawLine(point1.x, point1.y, point2.x, point2.y, fill=color, lineWidth = 2)
    #     drawLine(point1.x, point1.y, curve.x, curve.y, fill=color, lineWidth = 2)

    #     a = linearCurve(point1, point2, t, 'grey', True)
    #     b = linearCurve(point2, point3, t, 'grey', True)

    #     drawLine(a.x, a.y, b.x, b.y, fill='cyan', lineWidth = 2)
    #     curve.display(8, color)
    curveList.append(curve)

def genCurve(app):
    app.t = 0
    app.quadcurve = []
    while app.t < 1:
        quadraticCurve(app.quadpos[0], app.quadpos[1], app.quadpos[2], app.t, 'lightgreen', app.quadcurve)
        app.t += app.speed

def onStep(app):
    # app.t += app.speed
    # if app.t >= 1:
    #     app.t = 0
    #     app.quadcurve = []  
    pass

def onKeyHold(app, keys):
    if 'up' in keys:
        app.speed += 0.001
        genCurve(app)
    if 'down' in keys and app.speed > 0:
        app.speed -= 0.001
        genCurve(app)

def redrawAll(app):
    drawLabel(f'line "speed" currently {str(app.speed)[:7]}', 100, 10)

    if len(app.quadcurve) > 2:
        for i in range(len(app.quadcurve)-1):
            a = app.quadcurve[i]
            b = app.quadcurve[i+1]
            drawLine(a.x, a.y, b.x, b.y, fill='red', lineWidth = 5)

def main():
    runApp()

main()