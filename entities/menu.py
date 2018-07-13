from .controls import TapButton
from easy_mobile.sound import Sound
from easy_mobile.sprite import Sprite

from easy_mobile.setup import *
from config import *

class MainMenu():
    def __init__(self, screen):
        self.screen = screen
        self.Icon = Sprite(SCREEN_WIDTH/4, SCREEN_HEIGHT-SCREEN_WIDTH/2-64, image="image/tomb.png", width=SCREEN_WIDTH/2, height=SCREEN_WIDTH/2)
        # self.Icon = Sprite(screen.getWidth()/2-123, screen.getHeight()-246-123, image="image/test.gif")
        # self.Icon.setAnimationLoopDelay(0.125/2)
        print([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.Background = Sprite(0, 0, image="image/menu_background.png", width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        
        buttonHeight = (SCREEN_HEIGHT - SCREEN_WIDTH/2)/3
        self.start = TapButton(0,   self.Icon.getY()-buttonHeight, 'image/right_arrow.png', 'image/right_arrow_pressed.png', width=SCREEN_WIDTH/2, height=buttonHeight)
        self.relics = TapButton(0,  self.start.getY()-buttonHeight, 'image/right_arrow.png', 'image/right_arrow_pressed.png', width=SCREEN_WIDTH, height=buttonHeight)
        self.credits = TapButton(0, self.relics.getY()-buttonHeight, 'image/right_arrow.png', 'image/right_arrow_pressed.png', width=SCREEN_WIDTH, height=buttonHeight)
        
        # self.sprites = [self.Background, self.Icon, self.start]
        self.sprites = [self.Background, self.Icon, self.start, self.relics, self.credits]

        for s in self.sprites:
            s.setStaticPosition(True)

        screen.add(self.sprites)
    # def update(self, entities):
    #     pass

    def getStart(self):
        return self.start.Pressed()

    # def getRelics(self):
    #     return self.relics.Pressed()

    # def getCredits(self):
    #     return self.credits.Pressed()

    def getRelics(self):
        return False

    def getCredits(self):
        return False

    def exit(self):
        for item in self.sprites:
            self.screen.remove(item)
