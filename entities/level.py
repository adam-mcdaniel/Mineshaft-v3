from collections import deque
from config import *

from .player import Player
from .wall import Wall

class Level(deque):
    def __init__(self, level_instructions):
        super(Level, self).__init__()

        sprites = []
        x = 0
        y = len(level_instructions) * BLOCK_HEIGHT
        for row in level_instructions:
            for column in row:
                if column == "w":
                    sprites.append(Wall(x, y))
                elif column == "p":
                    sprites.append(Player(x, y))
                    
                x += BLOCK_WIDTH
            y -= BLOCK_HEIGHT
            x = 0

        for sprite in sprites:
            self.append(sprite)

        self.width = len(level_instructions[0]) * BLOCK_HEIGHT
        self.height = len(level_instructions) * BLOCK_WIDTH

        # print(self.width)
        # print(self.height)

    def __add__(self, level):
        self.height += level.height
        for sprite in self:
            sprite.move(0, level.height)
        for sprite in level:
            self.append(sprite)
        
        # for sprite in self:
        #     print(sprite)
            
        return self