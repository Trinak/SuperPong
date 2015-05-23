'''
Created on Sep 17, 2013

@author: Devon
'''

import random
from enum import IntEnum

from pyHopeEngine import engineCommon as ECOM
from superPong.actors.ballAI.ballState import ballAngry, ballBored, ballCrazy, ballExcited, ballHappy, ballSad
from superPong.actors.ballAI.ballProcesses.ballHandleItemProcess import BallHandleItemProcess
from superPong.events.pongEvents import Event_BallCollide, Event_GiveBallItem, Event_RequestCurrentScore

class Moods(IntEnum):
    Happy = 0
    Angry = 1
    Sad = 2
    Bored = 3
    Excited = 4
    Crazy = 5


class BasicBallBrain(object):
    def __init__(self):
        self.ball = None
        self.name = "BasicBallBrain"
    
    def init(self, ball):
        self.ball = ball
        initState = ballHappy.BallHappy
        return initState(ball)
    
    def think(self):
        return None
    
    def cleanUp(self):
        self.ball = None


class MainBallBrain(BasicBallBrain):
    def __init__(self):
        super().__init__()
        self.name = "MainBallBrain"
        self.emotionalScores = [75, 25, 25, 10, 50, 10]; # 0 = Happy, 1 = Angry, 2 = Sad, 3 = Bored, 4 = Excited, 5 = Crazy
        self.emotionalStates = [ballHappy.BallHappy, ballAngry.BallAngry, ballSad.BallSad, ballBored.BallBored, ballExcited.BallExcited, ballCrazy.BallCrazy];
        self.handleItemProcess = None
        ECOM.eventManager.addListener(self.handleItem, Event_GiveBallItem.eventType)
    
    def think(self):
        rand = random.randint(0, sum(self.emotionalScores))
        
        for i in range(len(self.emotionalScores)):
            if rand < self.emotionalScores[i]:
                return self.emotionalStates[i]
            
            rand -= self.emotionalScores[i]
            
        return None
       
    
    def handleItem(self, event):
        if self.handleItemProcess is None:
            self.handleItemProcess = BallHandleItemProcess(event.item, self)
            ECOM.engine.baseLogic.processManager.addProcess(self.handleItemProcess)
        else:
            self.handleItemProcess.addItem(event.item)
        
    def cleanUp(self):
        super().cleanUp()
        ECOM.eventManager.removeListener(self.handleItem, Event_GiveBallItem.eventType)
        