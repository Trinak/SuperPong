'''
Created on Jul 24, 2013

@author: Devon
'''
import random

from pyHopeEngine import engineCommon as ECOM
from pyHopeEngine import ActorManager
from pyHopeEngine import Event_SetControlledActor
from pyHopeEngine import Vec2d
from superPong.actors.pongActorFactory import PongActorFactory

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
    
    def destroyBall(self, emotion = None):
        if emotion is None:
            self.destroyActor(self.getBall().actorID)
    
    def restartBall(self, num = 0):
        pos = Vec2d(ECOM.Screen.halfW, ECOM.Screen.halfH)
        x = random.choice((-1, 1))
        y = random.choice((-1, 1))
        direction = Vec2d(x, y)
        
        self.balls[num].getComponent("PhysicsComponent").setPosition(pos) 
        self.balls[num].getComponent("TransformComponent").direction = direction
    
    def cleanUp(self):
        super().cleanUp()
        
        self.players.clear()
        self.enemies.clear()
        self.balls.clear()