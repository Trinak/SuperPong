'''
Created on Jul 24, 2013

@author: Devon
'''

from pyHopeEngine import engineCommon as ECOM
from pyHopeEngine import ActorManager
from pyHopeEngine import Event_SetControlledActor
from superPong.pongActorFactory import PongActorFactory

class PongActorManager(ActorManager):
    def __init__(self):
        super().__init__()
        
        self.actorFactory = PongActorFactory()
        self.players = []
        self.enemies = []
        self.balls = []
    
    
    def addPlayer(self, actor):
        self.players.append(actor)
        event = Event_SetControlledActor(actor.actorID)
        ECOM.eventManager.queueEvent(event)
        
    
    def addEnemy(self, actor):
        self.enemies.append(actor)
        
    
    def addBall(self, actor):
        self.balls.append(actor)
    
    
    def getBall(self, num = 0):
        return self.balls[num]
    
    def cleanUp(self):
        super().cleanUp()
        
        self.players.clear()
        self.enemies.clear()
        self.balls.clear()