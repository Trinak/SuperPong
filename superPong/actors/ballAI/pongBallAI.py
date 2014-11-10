'''
Created on Sep 17, 2013

@author: Devon
'''

import random

from pyHopeEngine import engineCommon as ECOM
from superPong.actors.ballAI.ballState import *
from superPong.events.pongEvents import Event_BallCollide, Event_GiveBallItem

class BallBrain(object):
    def __init__(self):
        self.ball = None
    
    
    def init(self, ball):
        self.ball = ball
    
    
    def think(self):
        pass


class SimpleBallBrain(BallBrain):
    def __init__(self):
        super().__init__()
        self.hitLeft = 0
        self.hitRight = 0
        self.name = "SimpleBallBrain"
        ECOM.eventManager.addListener(self.checkCollide, Event_BallCollide.eventType)
        ECOM.eventManager.addListener(self.adjustEmotionalStats, Event_GiveBallItem.eventType)
    
    def think(self):
        hits = self.hitLeft + self.hitRight
        if hits < 1:
            return ballHappy.BallHappy
        else:
            rand = random.randint(0, 6)
            if rand == 0:
                return ballHappy.BallHappy
            elif rand == 1:
                return ballCrazy.BallCrazy
            elif rand == 2:
                return ballSad.BallSad
            elif rand == 3:
                return ballExcited.BallExcited
            elif rand == 4:
                return ballAngry.BallAngry
            elif rand == 5:
                return ballBored.BallBored
        
        return ballHappy.BallHappy
            
       
    def checkCollide(self, event):
        actor1 = ECOM.actorManager.getActor(event.actorID1)
        actor2 = ECOM.actorManager.getActor(event.actorID2)
        
        if actor1.actorID == self.ball.actorID:
            paddle = actor2
        elif actor2.actorID == self.ball.actorID:
            paddle = actor1
        else:
            return
        
        if paddle.type == 'PaddleOne':
            self.hitLeft += 1
        elif paddle.type == 'PaddleTwo':
            self.hitRight += 1
    
    
    def adjustEmotionalStats(self, event):
        if event.item == "Chocolate":
            pass
        elif event.item == "PsychoticPill":
            pass
        elif event.item == "AntiDepressant":
            pass