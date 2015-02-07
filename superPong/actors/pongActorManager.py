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
    
    def getBall(self, actorID = 0):
        for ball in self.balls:
            if ball.actorID == actorID:
                return ball
        
        return None
    
    def destroyBall(self, actorID = 0, emotion = None):
        if emotion is None:
            ball = self.getBall(actorID)
            self.balls.remove(ball)
            self.destroyActor(actorID)
            return True
        else:
            ballToDestroy = None
            
            for ball in self.balls[1:]:
                aiComponent = ball.getComponent("AIComponent")
                if type(aiComponent.currentState) is emotion:
                    ballToDestroy = ball
                    break
                 
            if ballToDestroy is not None:
                actorID = ballToDestroy.actorID
                self.balls.remove(ballToDestroy)
                self.destroyActor(actorID)
                return True
        
        return False
            
    def ballWasRemoved(self, actorID1, actorID2):
        ballID = None
        if actorID1 != 0 and actorID2 != 0:
            for ball in self.balls:
                if ball.actorID == actorID1:
                    ballID = actorID1
                    break;
                elif ball.actorID == actorID2:
                    ballID = actorID2
                    break;
                
            if ballID is not None:
                self.destroyBall(ballID)
                return True
        return False
        
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