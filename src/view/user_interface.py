import pygame
from model import GameState
from pygame.math import Vector2
from .layer import Layer, ArrayLayer, UnitsLayer, BulletsLayer, ExplosionsLayer
from controller import MoveCommand, TargetCommand, ShootCommand, MoveBulletCommand, DeleteDestroyedCommand,Command,GameController


class UserInterface():
    
    def __init__(self):
        self.controller = GameController()

        pygame.init()
        self.window = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Tower Defense")
        pygame.display.set_icon(pygame.image.load("assets/icon.png"))
        # Game state
        self.gameState = GameState.getInstance()

        # Font
        self.titleFont = pygame.font.Font("assets/BD_Cartoon_Shout.ttf", 72)
        self.itemFont = pygame.font.Font("assets/BD_Cartoon_Shout.ttf", 48)
        self.messageFont = pygame.font.Font("assets/BD_Cartoon_Shout.ttf", 36)


        # Menu
        self.menuCursor = pygame.image.load("assets/cursor.png")
        for item in self.gameState.menu.menuItems:
            surface = self.itemFont.render(item['title'], True, (200, 0, 0))
            self.menuWidth = max(self.gameState.menu.menuWidth, surface.get_width())
            item['surface'] = surface     

        # Layers
        self.layers = [
            ArrayLayer(self.gameState.level.cellSize,"assets/ground.png",self.gameState,self.gameState.level.ground,0),
            ArrayLayer(self.gameState.level.cellSize,"assets/walls.png",self.gameState,self.gameState.level.walls),
            UnitsLayer(self.gameState.level.cellSize,"assets/units.png",self.gameState,self.gameState.level.units),
            BulletsLayer(self.gameState.level.cellSize,"assets/explosions.png",self.gameState,self.gameState.bullets),
            ExplosionsLayer(self.gameState.level.cellSize,"assets/explosions.png"),
        ]   

        for layer in self.layers:
            self.gameState.addObserver(layer)
        
        # Loop properties
        self.clock = pygame.time.Clock()

    def renderMenu(self):
        window=self.window
        darkSurface = pygame.Surface(window.get_size(),flags=pygame.SRCALPHA)
        pygame.draw.rect(darkSurface, (0,0,0,150), darkSurface.get_rect())
        window.blit(darkSurface, (0,0))
        # Initial y
        y = 50
        
        # Title
        surface = self.titleFont.render("TANK BATTLEGROUNDS !!", True, (200, 0, 0))
        x = (window.get_width() - surface.get_width()) // 2
        window.blit(surface, (x, y))
        y += (200 * surface.get_height()) // 100
        
        # Draw menu items
        menu = self.gameState.menu
        x = (window.get_width() - menu.menuWidth) // 2
        for index, item in enumerate(menu.menuItems):
            # Item text
            surface = item['surface']
            window.blit(surface, (x, y))
            
            # Cursor
            if index == menu.currentMenuItem:
                cursorX = x - self.menuCursor.get_width() - 10
                cursorY = y + (surface.get_height() - self.menuCursor.get_height()) // 2
                window.blit(self.menuCursor, (cursorX, cursorY))
            
            y += (120 * surface.get_height()) // 100      

    def renderMessage(self):
        surface = self.messageFont.render(self.gameState.message, True, (200, 0, 0))
        x = (self.window.get_width() - surface.get_width()) // 2
        y = (self.window.get_height() - surface.get_height()) // 2
        self.window.blit(surface, (x, y))

    def renderLevel(self):
        for layer in self.layers:
            layer.render(self.window)

    def updateLayers(self):
        self.layers = [
            ArrayLayer(self.gameState.level.cellSize,"assets/ground.png",self.gameState,self.gameState.level.ground,0),
            ArrayLayer(self.gameState.level.cellSize,"assets/walls.png",self.gameState,self.gameState.level.walls),
            UnitsLayer(self.gameState.level.cellSize,"assets/units.png",self.gameState,self.gameState.level.units),
            BulletsLayer(self.gameState.level.cellSize,"assets/explosions.png",self.gameState,self.gameState.bullets),
            ExplosionsLayer(self.gameState.level.cellSize,"assets/explosions.png"),
        ]   

    def run(self):
        state = self.gameState
        controller = self.controller
        window=self.window
        while state.running:
            # Inputs and updates are exclusives
            if state.currentActiveMode == 'Overlay':
                controller.processInputMenu()
            elif state.currentActiveMode == 'Play':
                try:
                    
                    controller.processInputLevel()
                    controller.update()
                except Exception as ex:
                    print(ex)
                    darkSurface = pygame.Surface(window.get_size(),flags=pygame.SRCALPHA)
                    pygame.draw.rect(darkSurface, (0,0,0,150), darkSurface.get_rect())
                    window.blit(darkSurface, (0,0))
                    state.currentActiveMode = 'Overlay'
                    controller.showMessage("Error during the game update...")
            elif state.currentActiveMode == 'Message':
                controller.processInputMessage()
            else:
                break

            # Render game (if any), and then the overlay (if active)
            if state.currentActiveMode == 'Overlay':
                self.renderMenu()
            elif state.currentActiveMode == 'Play':
                try:
                    self.renderLevel()
                except Exception as ex:
                    print(ex)
                    state.currentActiveMode = 'Overlay'
                    self.renderMessage("Error during the game rendering...")
            elif state.currentActiveMode == 'Message':
                self.renderMessage()
            else:
                break
            
            
                    
                
            # Update display
            pygame.display.update()    
            self.clock.tick(60)
    