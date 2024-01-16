import math
from pygame.math import Vector2

class GameItem():
    def __init__(self,position,tile):
        self.status = "alive"
        self.position = position
        self.tile = tile
        self.orientation = 0    
    