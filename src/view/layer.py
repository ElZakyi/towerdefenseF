import pygame
import math
from model import GameStateObserver
from pygame.math import Vector2
from pygame.rect import Rect

class Layer(GameStateObserver):
    def __init__(self,cellSize,imageFile):
        self.cellSize = cellSize
        self.texture = pygame.image.load(imageFile)
        
    def setTileset(self,cellSize,imageFile):
        self.cellSize = cellSize
        self.texture = pygame.image.load(imageFile)

    @property
    def cellWidth(self):
        return int(self.cellSize.x)

    @property
    def cellHeight(self):
        return int(self.cellSize.y)        
    
    def unitDestroyed(self,unit):
        pass
        
    def renderTile(self,surface,position,tile,angle=None):
        # Location on screen
        spritePoint = position.elementwise()*self.cellSize
        
        # Texture
        texturePoint = tile.elementwise()*self.cellSize
        textureRect = Rect(int(texturePoint.x), int(texturePoint.y), self.cellWidth, self.cellHeight)
        
        # Draw
        if angle is None:
            surface.blit(self.texture,spritePoint,textureRect)
        else:
            # Extract the tile in a surface
            textureTile = pygame.Surface((self.cellWidth,self.cellHeight),pygame.SRCALPHA)
            textureTile.blit(self.texture,(0,0),textureRect)
            # Rotate the surface with the tile
            rotatedTile = pygame.transform.rotate(textureTile,angle)
            # Compute the new coordinate on the screen, knowing that we rotate around the center of the tile
            spritePoint.x -= (rotatedTile.get_width() - textureTile.get_width()) // 2
            spritePoint.y -= (rotatedTile.get_height() - textureTile.get_height()) // 2
            # Render the rotatedTile
            surface.blit(rotatedTile,spritePoint)

    def render(self,surface):
        raise NotImplementedError() 
    
class ArrayLayer(Layer):
    def __init__(self,ui,imageFile,gameState,array,surfaceFlags=pygame.SRCALPHA):
        super().__init__(ui,imageFile)
        self.gameState = gameState
        self.array = array
        self.surface = None
        self.surfaceFlags = surfaceFlags
    
    def setTileset(self,cellSize,imageFile):
        super().setTileset(cellSize,imageFile)
        self.surface = None
        
    def render(self,surface):
        if self.surface is None:
            self.surface = pygame.Surface(surface.get_size(),flags=self.surfaceFlags)
            for y in range(self.gameState.worldHeight):
                for x in range(self.gameState.worldWidth):
                    tile = self.array[y][x]
                    if not tile is None:
                        self.renderTile(self.surface,Vector2(x,y),tile)
        surface.blit(self.surface,(0,0))

class UnitsLayer(Layer):
    def __init__(self,ui,imageFile,gameState,units):
        super().__init__(ui,imageFile)
        self.gameState = gameState
        self.units = units
        
    def render(self,surface):
        for unit in self.units:
            self.renderTile(surface,unit.position,unit.tile,unit.orientation)
            if unit.status == "alive":
                size = unit.weaponTarget - unit.position
                angle = math.atan2(-size.x,-size.y) * 180 / math.pi
                self.renderTile(surface,unit.position,Vector2(0,6),angle)
                
class BulletsLayer(Layer):
    def __init__(self,ui,imageFile,gameState,bullets):
        super().__init__(ui,imageFile)
        self.gameState = gameState
        self.bullets = bullets
        
    def render(self,surface):
        for bullet in self.bullets:
            if bullet.status == "alive":
                self.renderTile(surface,bullet.position,bullet.tile,bullet.orientation)
                
class ExplosionsLayer(Layer):
    def __init__(self,ui,imageFile):
        super().__init__(ui,imageFile)
        self.explosions = []
        self.maxFrameIndex = 27
        
    def add(self,position):
        self.explosions.append({
            'position': position,
            'frameIndex': 0
        })

    def unitDestroyed(self,unit):
        self.add(unit.position)
        
    def render(self,surface):
        for explosion in self.explosions:
            frameIndex = math.floor(explosion['frameIndex'])
            self.renderTile(surface,explosion['position'],Vector2(frameIndex,4))
            explosion['frameIndex'] += 0.5
        self.explosions = [ explosion for explosion in self.explosions if explosion['frameIndex'] < self.maxFrameIndex ]
            
      