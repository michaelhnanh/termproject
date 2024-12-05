#character code --> austin himself

from cmu_graphics import *
from tools import *
import math

class Character:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.orientation = 0
        self.grounded = False
        self.rotating = False
        self.platformed = False
        
        self.vert = 8
        self.weight = 60
        self.rotationRate = 4
        self.rotatedAmount = 0
        self.rotationMomentum = 0
        self.speed = 15
        self.momentumX = 0
        self.momentumY = 0
        self.charging = False
        self.chargingTimer = 0
        self.chargeAmount = 1

        self.positionX = 0.5 # starts off at the middle of the screen --> launches out --> smoothly goes back to width/4
        self.positionY = 0.5

        self.currentCurve = 0 # which curve in the terrain lists the character is on
        self.posOnCurve = 0

        # sprite links --> key frames and 1 in-between
        self.linkGrounded = './Sprites/austinGrounded.png'

        self.linkUnGrounded = './Sprites/austinUnGrounded.png'

        self.linkRotating = './Sprites/austinRotating.png'

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

    def drop(self):
        pass

    def reCenter(self):
        pass