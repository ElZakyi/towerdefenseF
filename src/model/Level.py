import json
from pygame.math import Vector2
from .Unit import Unit


class Level():
    def __init__(self, name):
        self.name = name
        self.ground = [ [ Vector2(5,1) ] * 16 ] * 10
        self.walls = [ [ None ] * 16 ] * 10
        self.units = [ Unit(Vector2(8,9),Vector2(1,0)) ]
        self.cellSize = Vector2(64,64)
        self.gameOver = False
        
    @property
    def cellWidth(self):
        return int(self.cellSize.x)

    @property
    def cellHeight(self):
        return int(self.cellSize.y)

    def __str__(self):
        return self.name
    