'''
Created on Sep 17, 2013

@author: Devon
'''

import random
import math

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
        self.emotionalWeights = [15, 17, 17, 17, 17, 17]; # 0 = Happy, 1 = Angry, 2 = Sad, 3 = Bored, 4 = Excited, 5 = Crazy
        self.emotions = [ballHappy.BallHappy, ballAngry.BallAngry, ballSad.BallSad, ballBored.BallBored, ballExcited.BallExcited, ballCrazy.BallCrazy];
        self.hitLeft = 0
        self.hitRight = 0
        self.name = "SimpleBallBrain"
        ECOM.eventManager.addListener(self.checkCollide, Event_BallCollide.eventType)
        ECOM.eventManager.addListener(self.handleItem, Event_GiveBallItem.eventType)
    
    def think(self):
        choices = []
        
        for i in range(6):
            choices += [self.emotions[i]] * self.emotionalWeights[i]
        
        return random.choice(choices)
            
       
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
    
    
    def handleItem(self, event):
        if event.item == "Chocolate" and self.emotionalWeights[0] < 100:
            self.emotionalWeights[0] = self.adjustEmotionalStats(self.emotionalWeights[0])
        elif event.item == "Psychopill" and self.emotionalWeights[5] < 100:
            self.emotionalWeights[5] = self.adjustEmotionalStats(self.emotionalWeights[5])
        elif event.item == "AntiDepressant" and self.emotionalWeights[0] < 100:
            self.emotionalWeights[0] = self.adjustEmotionalStats(self.emotionalWeights[0])
        elif event.item == "HistoryBook":
            pass
        elif event.item == "MeanNote":
            pass
        elif event.item == "SadPicture":
            pass
        elif event.item =="WinningTicket":
            pass


    def adjustEmotionalStats(self, weight):
        currentWeight = weight
        weight = min(weight + 30, 100)
        adjust = int((weight - currentWeight) / 6)
        
        for i in range(6):
            self.emotionalWeights[i] -= adjust
        
        return weight
        
        
        