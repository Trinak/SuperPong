'''
Created on Dec 23, 2014

@author: Arrington
'''

from pyHopeEngine import Process
from pyHopeEngine import engineCommon as ECOM
from superPong.events.pongEvents import Event_GiveBallItem, Event_BallGoal

class PaddleGiveItemProcess(Process):
    def __init__(self):
        super().__init__()
        self.time = 0
        self.myScore = 0
        self.enemyScore = 0 
        ECOM.eventManager.addListener(self.adjustScore, Event_BallGoal.eventType) 
    
    def update(self, elapsedTime):
        pass
    #happy - favors no one
    #angry - favors loser
    #bored - favors winner
    #crazy - favors no one
    #excited - favors no one
    #sad - favors no one
    
    def adjustScore(self, event):
        self.myScore = event.rightScore
        self.enemyScore = event.leftScore