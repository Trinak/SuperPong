'''
Created on Nov 2, 2014

@author: Arrington
'''

import random

from pyHopeEngine import engineCommon as ECOM
from pyHopeEngine import Event_ApplyImpulse, Vec2d
from superPong.actors.ballAI.ballState.ballState import BallState

class BallCrazy(BallState): #Goal: None, move randomly
    def __init__(self, ball):
        super().__init__(ball)
        transformComp = self.ball.getComponent('TransformComponent')
        pos = transformComp.pos
        rotation = transformComp.rotation
        
        file = 'Images\PongBallCrazy.png'
        renderComp = self.ball.getComponent('RenderComponent')
        renderComp.spriteFile = file
        renderComp.sceneNode.addSpriteImage(file, pos, rotation)
    
    def update(self):
        rand = random.randint(0, 3)
        if rand == 0:
            event = Event_ApplyImpulse(self.ball.actorID, Vec2d(0, 1), 25)
            ECOM.eventManager.queueEvent(event)
        elif rand == 1:
            event = Event_ApplyImpulse(self.ball.actorID, Vec2d(0, -1), 25)
            ECOM.eventManager.queueEvent(event)
        elif rand == 2:
            event = Event_ApplyImpulse(self.ball.actorID, Vec2d(1, 0), 25)
            ECOM.eventManager.queueEvent(event)
        elif rand == 3:
            event = Event_ApplyImpulse(self.ball.actorID, Vec2d(-1, 0), 25)
            ECOM.eventManager.queueEvent(event)