from easy_mobile.sound import Sound
from easy_mobile.sprite import Sprite

MAX_SPEED = 10
FALL_SPEED = 128

class Arrow(Sprite):
    def __init__(self, x, y, xvel, yvel):            
        super(Arrow, self).__init__(x, y, 'image/arrow/right.png')
        self.xvel = xvel
        self.yvel = yvel

    def Slide(self, x, y):
        self.xvel += x
        self.yvel += y

        if self.xvel < -MAX_SPEED:
            self.xvel = -MAX_SPEED
        elif self.xvel > MAX_SPEED:
            self.xvel = MAX_SPEED
        if self.yvel < -FALL_SPEED:
            self.yvel = -FALL_SPEED

    def CheckDirection(self):
        if self.xvel < 0:
            self.setImage('image/arrow/left.png')
        if self.xvel > 0:
            self.setImage('image/arrow/right.png')

    def update(self, entities):
        self.CheckDirection()
        self.move(self.xvel, self.yvel)
        self.Slide(0, -1)
