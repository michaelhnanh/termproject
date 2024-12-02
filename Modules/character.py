#character code --> austin himself

from cmu_graphics import *
from tools import *
import math

class Character:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.orientation = 0
        self.grounded = False
        self.rotating = True
        self.platformed = False
        
        self.vert = 50
        self.rotationRate = 2
        self.speed = 1

        self.positionX = 0.5 # starts off at the middle of the screen --> launches out --> smoothly goes back to width/4
        self.positionY = 0.5

        self.currentCurve = 0 # which curve in the terrain lists the character is on
        self.posOnCurve = 0

        # sprite links --> key frames and 1 in-between
        self.linkGrounded = None
        self.linkGroundtoUn = None
        self.linkUngrounded = None

        self.linkUntoRotating1 = None
        self.linkUntoRotating2 = None
        self.linkRotating = None

        self.linkHitGround = None
        self.linkTripped = None

        # also the issue of the player losing velocity while in the air --> how
        # another kind of bezier interpolation that reduces speed convincingly ig
        # how to implement that to go along with onstep? no idea
            # no need to implement losing horizontal velocity, just need to implement smooth jump correctly and 
            # re-add gravity pull back in afterwards so that character is pulled downwards.

    # character should be controlled at the base of feet --> just a Point(x,y)
    # character sprite is centered at a point height/2 away from base, perpendicular to orientation of character, with the sprite
    # rotated in that orientation



    def jump(self):
        # small jump effect --> moves off of center line in order to convey jumping effect
        pass

    def rotate(self):
        pass

    def drop(self):
        pass

    def reCenter(self):
        pass