from .GameItem import GameItem

from pygame.math import Vector2

class Unit(GameItem):
    def __init__(self,position,tile):
        super().__init__(position,tile)
        self.weaponTarget = Vector2(0,0)
        self.lastBulletEpoch = -100