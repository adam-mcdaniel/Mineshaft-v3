from easy_mobile.sound import Sound
from easy_mobile.sprite import Sprite

from easy_mobile.setup import *
from config import *

class Wall(Sprite):
    def __init__(self, x, y):
        self.xvel, self.yvel = 0, 0
        super(Wall, self).__init__(x, y, image="image/wall.png", width=BLOCK_WIDTH, height=BLOCK_HEIGHT)
