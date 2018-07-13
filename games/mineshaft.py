from easy_mobile.sound import Sound
from easy_mobile.sprite import Sprite
from config import *

from entities.player import Player
from entities.wall import Wall

from entities.controls import Controls
from entities.menu import MainMenu
from entities.level import Level

class Mineshaft:
    def __init__(self, screen):
        self.screen = screen

        self.player = Player(192, 32768)
        self.menu = None
        self.controls = None
        self.state = None

        self.startMenu()

    def buildLevel(self, level):
        level = level + Level([[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']])
        level = level + Level([[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']])
        level = level + Level([[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']])
        self.screen.clear()
        self.screen.setLevelWidth(SCREEN_WIDTH)
        print("SCREEN_WIDTH: {}".format(SCREEN_WIDTH))
        for sprite in level:
            if not isinstance(sprite, Player):
                self.screen.append(sprite)
            else:
                self.player = sprite
                self.screen.append(sprite)
                # print(self.player)
        self.controls = Controls(self.screen)

    def startMenu(self):
        self.state = "Menu"
        self.screen.clear()
        self.menu = MainMenu(self.screen)

    def startGame(self):
        self.state = "Game"
        self.buildLevel(
            Level([
                ['w','w','w','w','w','w','w','w','w','w'],
                ['w',' ',' ',' ',' ',' ',' ',' ',' ','w'],
                ['w',' ',' ',' ',' ',' ',' ',' ',' ','w'],
                ['w',' ',' ',' ',' ',' ',' ',' ',' ','w'],
                ['w',' ',' ',' ',' ',' ',' ',' ',' ','w'],
                ['w',' ',' ','w','w',' ',' ',' ',' ','w'],
                ['w',' ',' ',' ',' ',' ',' ',' ',' ','w'],
                ['w',' ',' ',' ',' ',' ',' ',' ',' ','w'],
                ['w',' ',' ',' ',' ',' ',' ',' ',' ','w'],
            ]) + Level([
                ['w','w','w','w','w','w','w',' ',' ','w'],
                ['w',' ',' ',' ',' ',' ',' ',' ',' ','w'],
                ['w',' ',' ',' ',' ',' ',' ',' ',' ','w'],
                ['w',' ',' ',' ',' ',' ',' ',' ',' ','w'],
                ['w',' ',' ',' ',' ',' ',' ',' ',' ','w'],
                ['w',' ',' ','w','w',' ',' ',' ',' ','w'],
                ['w',' ',' ',' ',' ',' ',' ',' ',' ','w'],
                ['w',' ',' ',' ',' ',' ',' ',' ',' ','w'],
                ['w',' ',' ',' ',' ',' ',' ',' ',' ','w'],
            ]) + Level([
                ['w','w','w',' ',' ','w','w','w','w','w'],
                ['w',' ',' ',' ',' ',' ',' ',' ',' ','w'],
                ['w',' ',' ',' ',' ',' ',' ',' ',' ','w'],
                ['w',' ',' ',' ','p',' ',' ',' ',' ','w'],
                ['w',' ',' ',' ',' ',' ',' ',' ',' ','w'],
                ['w',' ',' ','w','w',' ',' ',' ',' ','w'],
                ['w',' ',' ',' ',' ',' ',' ',' ',' ','w'],
                ['w',' ',' ',' ',' ',' ',' ',' ',' ','w'],
                ['w',' ',' ',' ',' ',' ',' ',' ',' ','w'],
                ['w','w','w','w','w','w',' ',' ','w','w'],
            ]) + Level([
                ['w',' ',' ',' ',' ',' ',' ',' ',' ','w'],
                ['w',' ',' ',' ',' ',' ',' ',' ',' ','w'],
                ['w',' ',' ',' ',' ',' ',' ',' ',' ','w'],
                ['w',' ',' ',' ',' ',' ',' ',' ',' ','w'],
                ['w',' ',' ',' ',' ',' ',' ',' ',' ','w'],
                ['w',' ',' ',' ',' ',' ',' ',' ',' ','w'],
                ['w',' ',' ',' ',' ',' ',' ',' ',' ','w'],
                ['w',' ',' ',' ',' ',' ',' ',' ',' ','w'],
                ['w','w','w','w','w','w','w','w','w','w'],
            ])      
        )


    def menuUpdate(self):
        if self.menu.getStart():
            self.startGame()
        if self.menu.getRelics():
            print("relics!")
        if self.menu.getCredits():
            print("credits!")

    def gameUpdate(self):
        if self.player.Dead():
            self.startMenu()

        if self.controls.getLeft():
            self.player.Slide(-2, 0)
        elif self.controls.getRight():
            self.player.Slide(2, 0)
        else:
            self.player.Slow()

        if self.controls.getJump():
            self.player.Jump()

        self.screen.focus(self.player)

    def update(self):    
        if self.state == "Menu":
            self.menuUpdate()
        elif self.state == "Game":
            self.gameUpdate()