from kivy.config import Config

def desktopSetup(width=320, height=240):
    Config.set('graphics', 'width', str(width))
    Config.set('graphics', 'height', str(height))

desktopSetup(640, 800)

from easy_mobile.setup import *
from games.mineshaft import Mineshaft
from config import *


screen = setup(level_height=32768)

screen.setCameraWinWidth(SCREEN_WIDTH)
screen.setCameraWinHeight(SCREEN_HEIGHT)

game = Mineshaft(screen)
def f():
    game.update()

    
screen.run(f)
