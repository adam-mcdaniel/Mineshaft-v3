import sys
import time
from .setup import *
from .tools import *
from .camera import *
from .camera import Rect
from collections import deque
from kivy.app import App
import kivy.input.postproc
from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.uix.widget import Widget
from kivy.graphics.texture import Texture
from kivy.input.providers.mouse import MouseMotionEvent

kivy.input.postproc.kivy_postproc_modules["doubletap"].double_tap_time = 200
kivy.input.postproc.kivy_postproc_modules["doubletap"].double_tap_distance = 100

keyDown = lambda event, key: False
keyUp = lambda event, key: False
TheScreen = None


class Sprite(Image):
    rect = Rect(0, 0, 0, 0)
    def __init__(self, x, y, image="", width=False, height=False, fps=10):
        super(Sprite, self).__init__(allow_stretch=True, keep_ratio=False, anim_delay=1/fps)
        self.static = False
        self.touch_up = True
        self.touch = MouseMotionEvent(0, 0, (x, y))
        self.touch.pos = (x, y)
        self.pos = (0, 0)
        self.source = os.path.abspath(image)
        self.texture = CoreImage(self.source).texture
        self.rect = Rect(x, y, self.texture.width, self.texture.height)
        self.width = self.texture.width
        self.height = self.texture.height
        self.double_tap = False

        self.first_touch = True

        if width:
            self.setWidth(width)
        if height:
            self.setHeight(height)

        self.reload()

    # def setAnimationLoopDelay(self, time):
    #     self.anim_loop = time

    def draw(self, camera):
        if self.static:
            self.pos = (self.rect.x, self.rect.y)
        else:
            self.pos = camera.apply(self)

    def setStaticPosition(self, static):
        self.static = static

    def getImage(self):
        return self.source

    def setImage(self, image):
        self.source = image
        self.texture = CoreImage(self.source).texture
        # self.rect = Rect(self.rect.x, self.rect.y, self.texture.width, self.texture.height)
        # self.width = self.texture.width
        # self.height = self.texture.height
        # self.size = self.rect.rect()[2], self.rect.rect()[3]

    def update(self, entities):
        pass

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y

    def goto(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def getX(self): return self.rect.x

    def getY(self): return self.rect.y

    def getWidth(self): return self.rect.w

    def getHeight(self): return self.rect.h

    def setWidth(self, w):
        self.rect.w = w
        self.size = self.rect.rect()[2], self.rect.rect()[3]
        # print(self.size)

    def setHeight(self, h):
        self.rect.h = h
        self.size = self.rect.rect()[2], self.rect.rect()[3]
        # print(self.size)

    def getPos(self):
        return self.getX(), self.getY()

    def getDistance(self, sprite):
        return ((self.getX() - sprite.getX())**2  +  (self.getY() - sprite.getY())**2)**0.5

    def collide(self, sprite):
        if (self.rect.x > sprite.rect.x and self.rect.x < (sprite.rect.x + sprite.rect.w)) or (self.rect.x + self.rect.w > sprite.rect.x and self.rect.x + self.rect.w < (sprite.rect.x + sprite.rect.w)):
            if (self.rect.y > sprite.rect.y and self.rect.y < (sprite.rect.y + sprite.rect.h)) or (self.rect.y + self.rect.h > sprite.rect.y and self.rect.y + self.rect.h < (sprite.rect.y + sprite.rect.h)):
                return True

        if (self.rect.y > sprite.rect.y and self.rect.y < (sprite.rect.y + sprite.rect.h)) or (self.rect.y + self.rect.h > sprite.rect.y and self.rect.y + self.rect.h < (sprite.rect.y + sprite.rect.h)):
            if (self.rect.x == sprite.rect.x):
                return True

        if (self.rect.x > sprite.rect.x and self.rect.x < (sprite.rect.x + sprite.rect.w)) or (self.rect.x + self.rect.w > sprite.rect.x and self.rect.x + self.rect.w < (sprite.rect.x + sprite.rect.w)):
            if (self.rect.y == sprite.rect.y):
                return True
 
        return False

    def getTouch(self):
        return self.touch

    def getTouchPos(self):
        return [self.touch.x, self.touch.y]

    def getTouchDown(self):
        return not self.touch_up

    def getTouchUp(self):
        return self.touch_up

    def getDoubleTap(self):
        x = self.double_tap
        if x and self.first_touch:
            x = False
            self.first_touch = False
            
        self.double_tap = False
        return x

    def __str__(self):
        return "<Sprite at: x={}, y={}>".format(self.rect.x, self.rect.y)


class CollideBox(Image):
    rect = Rect(0, 0, 0, 0)
    def __init__(self, x, y, width=False, height=False, ratio=[None, None]):
        super(Sprite, self).__init__(allow_stretch=True, keep_ratio=False)
        self.static = False
        self.touch_up = True
        self.touch = MouseMotionEvent(0, 0, (x, y))
        self.touch.pos = (x, y)
        self.pos = (0, 0)
        self.rect = Rect(x, y, self.texture.width, self.texture.height)
        self.width = self.texture.width
        self.height = self.texture.height
        self.double_tap = False

        self.first_touch = True

        if width:
            self.setWidth(width)
        if height:
            self.setHeight(height)

    def setStaticPosition(self, static):
        self.static = static

    def update(self, entities):
        pass

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y

    def goto(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def getX(self): return self.rect.x

    def getY(self): return self.rect.y

    def getWidth(self): return self.rect.w

    def getHeight(self): return self.rect.h

    def setWidth(self, w):
        self.rect.w = w
        self.size = self.rect.rect()[2], self.rect.rect()[3]
        # print(self.size)

    def setHeight(self, h):
        self.rect.h = h
        self.size = self.rect.rect()[2], self.rect.rect()[3]
        # print(self.size)

    def getPos(self):
        return self.getX(), self.getY()

    def getDistance(self, sprite):
        return ((self.getX() - sprite.getX())**2  +  (self.getY() - sprite.getY())**2)**0.5

    def collide(self, sprite):
        if (self.rect.x > sprite.rect.x and self.rect.x < (sprite.rect.x + sprite.rect.w)) or (self.rect.x + self.rect.w > sprite.rect.x and self.rect.x + self.rect.w < (sprite.rect.x + sprite.rect.w)):
            if (self.rect.y > sprite.rect.y and self.rect.y < (sprite.rect.y + sprite.rect.h)) or (self.rect.y + self.rect.h > sprite.rect.y and self.rect.y + self.rect.h < (sprite.rect.y + sprite.rect.h)):
                return True

        if (self.rect.y > sprite.rect.y and self.rect.y < (sprite.rect.y + sprite.rect.h)) or (self.rect.y + self.rect.h > sprite.rect.y and self.rect.y + self.rect.h < (sprite.rect.y + sprite.rect.h)):
            if (self.rect.x == sprite.rect.x):
                return True

        if (self.rect.x > sprite.rect.x and self.rect.x < (sprite.rect.x + sprite.rect.w)) or (self.rect.x + self.rect.w > sprite.rect.x and self.rect.x + self.rect.w < (sprite.rect.x + sprite.rect.w)):
            if (self.rect.y == sprite.rect.y):
                return True
 
        return False

    def getTouch(self):
        return self.touch

    def getTouchPos(self):
        return [self.touch.x, self.touch.y]

    def getTouchDown(self):
        return not self.touch_up

    def getTouchUp(self):
        return self.touch_up

    def getDoubleTap(self):
        x = self.double_tap
        if x and self.first_touch:
            x = False
            self.first_touch = False
            
        self.double_tap = False
        return x

    def __str__(self):
        return "<CollideBox at: x={}, y={}>".format(self.rect.x, self.rect.y)


class Joystick(Sprite):
    def __init__(self, x, y, image=""):
        super(Joystick, self).__init__(x, y, image=image)
        self.x_val = 0
        self.y_val = 0
        self.setStaticPosition(True)

    def update(self, screen):
        if not self.getTouchUp():
            self.x_val = 5 * min(max((self.getTouch().pos[0] - self.getX() - self.getWidth()/2) / (96), -10), 10)
            self.y_val = 5 * min(max((self.getTouch().pos[1] - self.getY() - self.getHeight()/2) / (96), -10), 10)
        else:
            self.x_val = 0
            self.y_val = 0

    def getDirection(self):
        return self.x_val, self.y_val


class ButtonSprite(Sprite):
    def __init__(self, x, y, image=""):
        super(ButtonSprite, self).__init__(x, y, image=image)
        self.setStaticPosition(True)

    def update(self, screen):
        pass

    def getPressed(self):
        return self.getTouchDown()


class ScreenWidget(Widget):
    def __init__(self, w, h, camera):
        super(ScreenWidget, self).__init__()
        global TheScreen
        self.sprites = []
        self.surfaces = []
        self.background = False

        self.camera = camera
        self.actions = []

        self.run = None


        self.sprite_width = w
        self.sprite_height = h
        # self.width = w
        # self.height = h

        # if not fs:
        #     self.width = w
        #     self.height = h
        # else:
        #     # pass
        self.width = Config.get('graphics', 'width')
        self.height = Config.get('graphics', 'height')
        
        print(self.size)

        # self.camera.setWinWidth(self.width)
        # self.camera.setWinHeight(self.height)

        TheScreen = self

        self.touch = None
        self.touch_up = None

    def clear(self):
        del self.sprites[:]
        self.clear_widgets()

    def __len__(self):
        return len(self.sprites)

    def __getitem__(self, i):
        return self.sprites[i]

    def getScreen():
        return TheScreen

    def getSize(self):
        return self.getWidth(), self.getHeight()

    def getWidth(self):
        return self.sprite_width

    def getHeight(self):
        return self.sprite_height

    def setBackground(self, sprite):
        self.background = sprite
        self.add_widget(sprite)

    def append(self, sprite):
        self.sprites.append(sprite)
        if isinstance(sprite, Sprite):
            self.add_widget(sprite)

    def remove(self, sprite):
        try:
            self.sprites.remove(sprite)
            self.remove_widget(sprite)
        except:
            pass

    def add(self, sprites):
        list(map(self.append, sprites))

    # def addAction(self, action):
    #     self.actions.append(action)

    # def addSurface(self, surface):
    #     self.surfaces.append(surface)
    #     self.add_widget(surface)

    def fill(self, color):
        pass

    def focus(self, sprite):
        self.camera.update(sprite)

    def setLevelSize(self, width, height):
        self.camera.setLevelSize(width, height)

    def setLevelWidth(self, width):
        self.camera.setLevelWidth(width)

    def setLevelHeight(self, height):
        self.camera.setLevelHeight(height)

    def setCameraWinWidth(self, width):
        self.camera.setWinWidth(width)

    def setCameraWinHeight(self, height):
        self.camera.setWinHeight(height)

    def setCameraWinSize(self, width, height):
        self.setCameraWinWidth(width)
        self.setCameraWinHeight(height)

        
    def update(self, dt):
        self.fill((0, 0, 0))

        if self.background:
            self.background.draw(self.camera)

        for sprite in self.sprites:
            if isinstance(sprite, Sprite):
                sprite.draw(self.camera)
            sprite.update(self)

        # for sprite in self.sprites:
        #     if sprite.getRatio()[0]:
        #         sprite.setWidth(sprite.getRatio()[0] * self.width)
        #     if sprite.getRatio()[1]:
        #         sprite.setHeight(sprite.getRatio()[1] * self.width)
        
        # list(map(lambda a: a.update(self), self.actions))
        # list(map(lambda s: s.draw(self.camera), self.surfaces))
        # list(map(lambda s: s.update(self), self.surfaces))
        # list(map(lambda s: list(map(lambda p: p.update(self), s.sprites)), self.surfaces))

        self.run()

    def moveToFront(self, sprite):
        for i, item in enumerate(self.sprites):
            if item == sprite:
                if item == sprite:
                    self.remove(sprite)
                    self.append(sprite)


    def on_touch_move(self, touch):
        for surface in self.surfaces:
            for item in surface.sprites:
                if surface.collide_point(*touch.pos):
                    item.touch = touch
                    item.touch_up = False
                else:
                    if item.touch == touch:
                        item.touch_up = True

        for item in self:
            if item.collide_point(*touch.pos):
                item.touch = touch
                item.touch_up = False
            else:
                if item.touch == touch:
                    item.touch_up = True

        return True
        
    def on_touch_down(self, touch):
        for surface in self.surfaces:
            for item in surface.sprites:
                if item.collide_point(*touch.pos):
                    item.touch_up = False
                    item.touch = touch
                    item.double_tap = not touch.is_double_tap
                    break

        for item in self:
            if item.collide_point(*touch.pos):
                item.touch_up = False
                item.touch = touch
                item.double_tap = not touch.is_double_tap
                break
                
        return True
        
    def on_touch_up(self, touch):
        for surface in self.surfaces:
            for item in surface.sprites:
                if touch == item.touch:
                    item.touch_up = True
                    item.touch = touch
                    
        for item in self:
            if touch == item.touch:
                item.touch_up = True
                item.touch = touch
                # item.double_tap = False

        return True

    # def getTouch(self):
    #     return self.touch

    # def getTouchDown(self):
    #     return not self.touch_up

    # def getTouchUp(self):
    #     return self.touch_up


class Screen(App):
    def __init__(self, *args):
        super(Screen, self).__init__()
        self.s = ScreenWidget(*args)

    def clear(self):
        self.s.clear()

    def build(self):
        # print(self.getSize())
        Clock.schedule_interval(self.s.update, 1.0 / 60.0)
        return self.s

    def on_pause(self):
        return True

    def on_resume(self):
        return True

    @staticmethod
    def getScreen():
        return TheScreen

    def getWidth(self):
        return self.s.width

    def getHeight(self):
        return self.s.height

    def getSize(self):
        return [self.s.width, self.s.height]

    def setBackground(self, sprite):
        sprite.setStaticPosition(True)
        self.s.setBackground(sprite)

    def append(self, sprite):
        self.s.append(sprite)

    def remove(self, sprite):
        self.s.remove(sprite)

    def add(self, sprites):
        self.s.add(sprites)

    def addAction(self, action):
        self.s.addAction(action)

    def addSurface(self, surface):
        self.s.addSurface(surface)

    def fill(self, color):
        pass

    def focus(self, sprite):
        self.s.focus(sprite)

    def getTouch(self):
        return self.s.getTouch()

    def getTouchDown(self):
        return self.s.getTouchDown()

    def getTouchUp(self):
        return self.s.getTouchUp()

    def run(self, f):
        self.s.run = f
        super(Screen, self).run()

    def __len__(self):
        return self.s.__len__()

    def __getitem__(self, i):
        return self.s.__getitem__(i)
    
    def moveToFront(self, sprite):
        self.s.moveToFront(sprite)

    def setLevelSize(self, width, height):
        self.s.setLevelSize(width, height)

    def setLevelWidth(self, width):
        self.s.setLevelWidth(width)

    def setLevelHeight(self, height):
        self.s.setLevelHeight(height)

    def setCameraWinWidth(self, width):
        self.s.setCameraWinWidth(width)

    def setCameraWinHeight(self, height):
        self.s.setCameraWinHeight(height)

    def setCameraWinSize(self, width, height):
        self.setCameraWinSize(width, height)
