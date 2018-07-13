from easy_mobile.sound import Sound
from easy_mobile.sprite import Sprite
from .wall import Wall

from easy_mobile.setup import *
from config import *

MAX_SPEED = 15
FALL_SPEED = 128

class Player(Sprite):
    def __init__(self, x, y):
        self.dead = False
        self.on_ground = True
        self.xvel, self.yvel = 0, 0
        self.idle_image = "image/idle.png"
        super(Player, self).__init__(x, y, image=self.idle_image, width=BLOCK_WIDTH, height=BLOCK_HEIGHT, fps=30)

    def Die(self):
        self.dead = True

    def Dead(self):
        return self.dead

    def Slide(self, x, y):
        self.xvel += x
        self.yvel += y

        if self.xvel < -MAX_SPEED:
            self.xvel = -MAX_SPEED
        elif self.xvel > MAX_SPEED:
            self.xvel = MAX_SPEED
        if self.yvel < -FALL_SPEED:
            self.yvel = -FALL_SPEED

    def Slow(self):
        # self.xvel += -min(self.xvel, 1)
        if self.xvel > 0:
            self.xvel -= 1
        elif self.xvel < 0:
            self.xvel += 1

    def update(self, entities):
        self.on_ground = False
        self.move(0, self.yvel)
        self.hit(entities, 0, self.yvel)
        if not self.on_ground:
            self.Slide(0, -3)
        self.move(self.xvel, 0)
        self.hit(entities, self.xvel, 0)

    def Jump(self):
        if self.on_ground:
            self.Slide(0, 75)
            self.on_ground = False

    def hit(self, entities, xvel, yvel):
        for entity in entities:
            if isinstance(entity, Wall) and self.collide(entity) and entity != self:
                if xvel > 0:
                    self.goto(entity.getX() - self.getWidth(), self.getY())
                    self.xvel = 0
                if xvel < 0:
                    self.goto(entity.getX() + entity.getWidth(), self.getY())
                    self.xvel = 0
                if yvel > 0:
                    self.goto(self.getX(), entity.getY() - self.getHeight())
                    self.yvel = 0
                if yvel < 0:
                    self.goto(self.getX(), entity.getY() + entity.getHeight())
                    self.yvel = 0
                    self.on_ground = True
                    
    def __str__(self):
        return "<Player at: x={}, y={}>".format(self.getX(), self.getY())
