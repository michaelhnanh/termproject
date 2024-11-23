from cmu_graphics import *
from tools import *
import math

def onAppStart(app):
    app.width = 1000
    app.height = 500

    app.t = 0
    app.speed = 0.05
    app.quadpos = [Point(10,10), Point(350,50), Point(650,700), Point(950,450)]

    app.quadcurve = []

    genCurve(app)

def linearCurve(point1, point2, t, color, trigger = True):
    P1_x = (1 - t) * point1.x
    P1_y = (1 - t) * point1.y

    P2_x = t * point2.x
    P2_y = t * point2.y

    curve = Point(P1_x + P2_x, P1_y + P2_y)

    if trigger:
        drawLine(point1.x, point1.y, point2.x, point2.y, fill=color, lineWidth = 2)
        drawLine(point1.x, point1.y, curve.x, curve.y, fill=color, lineWidth = 2)
        curve.display(8)
        return curve
    else:
        curve.display(8)
        return curve


def quadraticCurve(point1, point2, point3, point4, t, color, curveList, trigger = True):
    # P1_x = ((1 - t) ** 2) * point1.x
    # P1_y = ((1 - t) ** 2) * point1.y

    # P2_x = 2 * (1 - t) * t * point2.x
    # P2_y = 2 * (1 - t) * t * point2.y

    # P3_x = t ** 2 * point3.x
    # P3_y = t ** 2 * point3.y

    thirdX =      ((1 - t) ** 3) * point1.x
    thirdY =      ((1 - t) ** 3) * point1.y

    secondX = 3 * ((1 - t) ** 2) * t * point2.x
    secondY = 3 * ((1 - t) ** 2) * t * point2.y

    firstX =  3 * ((1 - t)     ) * (t ** 2) * point3.x
    firstY =  3 * ((1 - t)     ) * (t ** 2) * point3.y

    constantX =   (t ** 3) * point4.x
    constantY =   (t ** 3) * point4.y

    
    curve = Point(thirdX + secondX + firstX + constantX, thirdY + secondY + firstY + constantY)

    # if trigger:
    #     drawLine(point1.x, point1.y, point2.x, point2.y, fill=color, lineWidth = 2)
    #     drawLine(point1.x, point1.y, curve.x, curve.y, fill=color, lineWidth = 2)

    #     a = linearCurve(point1, point2, t, 'grey', True)
    #     b = linearCurve(point2, point3, t, 'grey', True)

    #     drawLine(a.x, a.y, b.x, b.y, fill='cyan', lineWidth = 2)
    #     curve.display(8, color)
    curveList.append(curve)

def cubicBezierConstructor(point1, point2, point3, point4, t, curveList):
    pass

def genCurve(app):
    app.t = 0
    app.quadcurve = []
    while app.t < 1:
        quadraticCurve(app.quadpos[0], app.quadpos[1], app.quadpos[2], app.quadpos[3], app.t, 'lightgreen', app.quadcurve)
        app.t += app.speed

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