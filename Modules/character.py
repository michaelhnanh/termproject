#character code --> austin himself

from cmu_graphics import *
from tools import *
import math

class Character:

    def __init__(self, x, y):
        self.pos = Point(x, y)
        self.orientation = 0
        self.grounded = False
        self.rotating = True
        self.platformed = False
        
        self.vert = 50
        self.rotationRate = 2
        self.speed = 15

        self.positionX = 0.5 # starts off at the middle of the screen --> launches out --> smoothly goes back to width/4
        self.positionY = 0.5

        # sprite links --> key frames and 1 in-between
        self.linkGrounded = None
        self.linkGroundtoUn = None
        self.linkUngrounded = None

        self.linkUntoRotating1 = None
        self.linkUntoRotating2 = None
        self.linkRotating = None

        self.linkHitGround = None
        self.linkTripped = None

        # self.x --> vector moving to character.positionX 
        # self.y --> vector moving upwards for jumps + vector moving downwards (gravity) to self.positionY
        # terrain movement around character (x) --> vector moving to character.positionX + 
                                            #       vector moving opposite direction of character movement vector
        # vector to move character to self.positionX should also be applied to terrain + hazards + chasers + platforms


        # gravity not applied would reduce possible complications with calculations, reduce number of collision checks greatly,
        # would allow for character to "slide" hassle free down slopes --> 
            # find curve which contacts character hitbox --> calculate angle of slope and speed of slope --> 
            # --> give to character? move terrain opposite of this vector? how to then calculate an increase in speed in the character?

        # every character should have a... 
        # terminal velocity sliding down the slope --> max speed --> each character should have a "weight" attribute
        # each character should accelerate the same, but have different max speeds due to their weight (if their weight is different

        # player could jump from one point of the curve to another --> nah, highly variable depending on the curve kinda fucky
        # 
                    # figure out how to place character onto points along the curve --> this transfers over to hazards and environment as well

               # using cubic curve formula --> when character makes contact with curve, detect whch curve and load control points
               # place control points into formula --> t increases by speed value every step -->
               # meaning that player moves along curve by the speed value for every single step -->
               # take terrain movement vector = abs( current character position - next character position according to bezier)
               # move terrain by vector

        # also the issue of the player losing velocity while in the air --> how the fuck to implement that
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