from easy_mobile.sound import Sound
from easy_mobile.sprite import Sprite

from easy_mobile.setup import *

class TapButton(Sprite):
    def __init__(self, x, y, image, pressed_image, width=SCREEN_WIDTH/(3), height=SCREEN_HEIGHT/6.25):
        self.image = image
        self.is_pressed = False
        self.pressed_image = pressed_image
        self.width = width
        self.height = height
        super(TapButton, self).__init__(x, y, image=image, width=width, height=height)

    def update(self, entities):
        if self.getTouchDown():
            self.Press()
            # print(self.Pressed())
        else:
            self.Release()
            # print("released")

    def Press(self):
        self.setImage(self.pressed_image)
        self.is_pressed = True

        self.setWidth(self.width)
        self.setHeight(self.height)

    def Release(self):
        self.setImage(self.image)
        self.is_pressed = False

        self.setWidth(self.width)
        self.setHeight(self.height)

    def Pressed(self):
        pressed = self.is_pressed
        self.is_pressed = False
        return pressed


class Controls():
    def __init__(self, screen):
        self.leftArrow  = TapButton(0, 0, 'image/left_arrow.png', 'image/left_arrow_pressed.png')
        self.rightArrow = TapButton(self.leftArrow.getWidth(), 0, 'image/right_arrow.png', 'image/right_arrow_pressed.png')
        self.jumpButton = TapButton(self.rightArrow.getX() + self.rightArrow.getWidth(), 0, 'image/right_arrow.png', 'image/right_arrow_pressed.png')
        sprites = [self.leftArrow, self.rightArrow, self.jumpButton]
        for s in sprites:
            s.setStaticPosition(True)

        screen.add(sprites)
    # def update(self, entities):
    #     pass

    def getLeft(self):
        return self.leftArrow.Pressed()

    def getRight(self):
        return self.rightArrow.Pressed()

    def getJump(self):
        return self.jumpButton.Pressed()