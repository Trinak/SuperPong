'''
Created on Sep 17, 2013

@author: Devon
'''

import random
from enum import IntEnum

from pyHopeEngine import engineCommon as ECOM
from superPong.actors.ballAI.ballState import *
from superPong.actors.ballAI.ballProcesses.ballHandleItemProcess import BallHandleItemProcess
from superPong.events.pongEvents import Event_BallCollide, Event_GiveBallItem

class Moods(IntEnum):
    Happy = 0
    Angry = 1
    Sad = 2
    Bored = 3
    Excited = 4
    Crazy = 5


class BallBrain(object):
    def __init__(self):
        self.ball = None
    
    def init(self, ball):
        self.ball = ball
        initState = ballHappy.BallHappy
        return initState(ball)
    
    def think(self):
        pass


class SimpleBallBrain(BallBrain):
    def __init__(self):
        super().__init__()
        self.emotionalScores = [75, 25, 25, 10, 50, 10]; # 0 = Happy, 1 = Angry, 2 = Sad, 3 = Bored, 4 = Excited, 5 = Crazy
        self.emotionalStates = [ballHappy.BallHappy, ballAngry.BallAngry, ballSad.BallSad, ballBored.BallBored, ballExcited.BallExcited, ballCrazy.BallCrazy];
        self.hitLeft = 0
        self.hitRight = 0
        self.name = "SimpleBallBrain"
        self.handleItemProcess = None
        ECOM.eventManager.addListener(self.checkCollide, Event_BallCollide.eventType)
        ECOM.eventManager.addListener(self.handleItem, Event_GiveBallItem.eventType)
    
    def think(self):
        rand = random.randint(0, sum(self.emotionalScores))
        
        for i in range(len(self.emotionalScores)):
            if rand < self.emotionalScores[i]:
                return self.emotionalStates[i]
            
            rand -= self.emotionalScores[i]
            
        return None
       
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
        if self.handleItemProcess is None:
            self.handleItemProcess = BallHandleItemProcess(event.item, self)
            ECOM.engine.baseLogic.processManager.addProcess(self.handleItemProcess)
        else:
            self.handleItemProcess.addItem(event.item)
        
        