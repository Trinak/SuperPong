'''
Created on Jul 17, 2013

@author: Devon
'''

import pygame

from pyHopeEngine import engineCommon as ECOM
from pyHopeEngine import KeyboardHandler
from pyHopeEngine import Event_Accelerate, Event_Decelerate

ACCELERATION = 100

class PaddleController(KeyboardHandler):
    def __init__(self):
        super().__init__()
        self.paddleNode = None
        self.keyMoveUp = None
        self.keyMoveDown = None
    
    
    def setControlledActor(self, paddleNode):
        self.paddleNode = paddleNode
    
    
    def onKeyDown(self, key):
        super().onKeyDown(key)
        
        if self.keys[self.keyMoveUp]:
            event = Event_Accelerate(self.paddleNode.actorID, -ACCELERATION)
            ECOM.eventManager.queueEvent(event)
        
        if self.keys[self.keyMoveDown]:
            event = Event_Accelerate(self.paddleNode.actorID, ACCELERATION)
            ECOM.eventManager.queueEvent(event)
    
    
    def onKeyUp(self, key):
        super().onKeyUp(key)
        
        if key == self.keyMoveUp or key == self.keyMoveDown:
            event = Event_Decelerate(self.paddleNode.actorID, 0)
            ECOM.eventManager.queueEvent(event)


class PaddleOneController(PaddleController):
    def __init__(self):
        super().__init__()
        self.keyMoveUp = pygame.K_w
        self.keyMoveDown = pygame.K_s
        
        
class PaddleTwoController(PaddleController):
    def __init__(self):
        super().__init__()
        self.keyMoveUp = pygame.K_UP
        self.keyMoveDown = pygame.K_DOWN
        