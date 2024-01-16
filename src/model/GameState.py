from pygame.math import Vector2
from .Unit import Unit
from .Level import Level
from .Menu import Menu


class GameState():
    _instance = None

    @staticmethod
    def getInstance():
        if GameState._instance is None:
            GameState()
        return GameState._instance

    def __init__(self):
        if GameState._instance is not None:
            raise Exception("GameState class is a singleton. Use getInstance() method to get the instance.")
        GameState._instance = self

        self.epoch = 0
        self.worldSize = Vector2(16,10)
        self.running = True
        self.level = Level("empty level")
        self.bullets = []
        self.bulletSpeed = 0.1
        self.bulletRange = 4
        self.bulletDelay = 10
        self.observers = []
        

        # Mode of the game
        self.currentActiveMode = 'Overlay' # 'Play' or 'Overlay'

        #Menu
        self.menu = Menu()

        # Message
        self.message = None    

    
    @property
    def worldWidth(self):
        """
        Returns the world width as an integer
        """
        return int(self.worldSize.x)
    
    @property
    def worldHeight(self):
        """
        Returns the world height as an integer
        """
        return int(self.worldSize.y)

    def isInside(self,position):
        """
        Returns true is position is inside the world
        """
        return position.x >= 0 and position.x < self.worldWidth \
           and position.y >= 0 and position.y < self.worldHeight

    def findUnit(self,position):
        """
        Returns the index of the first unit at position, otherwise None.
        """
        for unit in self.level.units:
            if  int(unit.position.x) == int(position.x) \
            and int(unit.position.y) == int(position.y):
                return unit
        return None
    
    def findLiveUnit(self,position):
        """
        Returns the index of the first live unit at position, otherwise None.
        """
        unit = self.findUnit(position)
        if unit is None or unit.status != "alive":
            return None
        return unit
    
    def addObserver(self,observer):
        """
        Add a game state observer. 
        All observer is notified when something happens (see GameStateObserver class)
        """
        self.observers.append(observer)
        
    def notifyUnitDestroyed(self,unit):
        for observer in self.observers:
            observer.unitDestroyed(unit)

    def notifyBulletFired(self,unit):
        for observer in self.observers:
            observer.bulletFired(unit)
