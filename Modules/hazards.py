# code for hazard objects such as rocks, campfires, and other collisions 
# 

class Rock:
    def __init__(self, x, y, orientation, image):
        self.x = x
        self.y = y
        self.orientation = orientation
        self.image = f'./Sprites/rock{image}.png'
        self.size = 50

    def __repr__(self):
        return f'({self.x}, {self.y}, {self.orientation})'
    
    def __eq__(self, rock2):
        if type(rock2) == Rock:
            return (self.x == rock2.x) and (self.y == rock2.y)
        else:
            return False