'''
Created on Jul 17, 2013

@author: Devon
'''

import pygame

from pyHopeEngine import engineCommon as ECOM
from pyHopeEngine import KeyboardHandler
from pyHopeEngine import Event_Accelerate, Event_Decelerate
from superPong.events.pongEvents import Event_GiveBallItem
from superPong.actors.items.items import *

ACCELERATION = 100

class PaddleController(KeyboardHandler):
    def __init__(self):
        super().__init__()
        self.paddleNode = None
        self.keyMoveUp = None
        self.keyMoveDown = None
        self.giveChocolate = None
        self.givePsychoticPill = None
        self.giveHistoryBook = None
        self.giveMeanNote = None
        self.giveSadPicture = None
        self.giveWinningTicket = None
    
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
        
        if key == self.giveChocolate:
            event = Event_GiveBallItem(Chocolate())
            ECOM.eventManager.queueEvent(event)
        
        if key == self.givePsychoticPill:
            event = Event_GiveBallItem(PsychoPill())
            ECOM.eventManager.queueEvent(event)

        if key == self.giveHistoryBook:
            event = Event_GiveBallItem(HistoryBook())
            ECOM.eventManager.queueEvent(event)

        if key == self.giveMeanNote:
            event = Event_GiveBallItem(MeanNote())
            ECOM.eventManager.queueEvent(event)

        if key == self.giveSadPicture:
            event = Event_GiveBallItem(SadPicture())
            ECOM.eventManager.queueEvent(event)
            
        if key == self.giveWinningTicket:
            event = Event_GiveBallItem(WinningTicket())
            ECOM.eventManager.queueEvent(event)




class PaddleOneController(PaddleController):
    def __init__(self):
        super().__init__()
        self.keyMoveUp = pygame.K_w
        self.keyMoveDown = pygame.K_s
        self.giveChocolate = pygame.K_c
        self.givePsychoticPill = pygame.K_p
        self.giveAntiDepressant = pygame.K_a
        self.giveHistoryBook = pygame.K_h
        self.giveMeanNote = pygame.K_m
        self.giveSadPicture = pygame.K_k
        self.giveWinningTicket = pygame.K_t
        
        
class PaddleTwoController(PaddleController):
    def __init__(self):
        super().__init__()
        self.keyMoveUp = pygame.K_UP
        self.keyMoveDown = pygame.K_DOWN
        