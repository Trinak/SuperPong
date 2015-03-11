'''
Created on Dec 23, 2014

@author: Arrington
'''

import random

from pyHopeEngine import Process
from pyHopeEngine import engineCommon as ECOM
from superPong.actors.ballAI.ballState import *
from superPong.actors.items.items import *
from superPong.events.pongEvents import Event_GiveBallItem, Event_BallGoal

class PaddleGiveItemProcess(Process):
    def __init__(self):
        super().__init__()
        self.interval = (10 * 1000) + random.randint(0, 4) #10 to 14 seconds
        self.time = 0
        self.myScore = 0
        self.enemyScore = 0
        self.enemyGaveItem = False
        self.enemyItemGiven = None
        ECOM.eventManager.addListener(self.adjustScore, Event_BallGoal.eventType)
        ECOM.eventManager.addListener(self.itemGiven, Event_GiveBallItem.eventType) 
    
    def update(self, elapsedTime):
        self.time += elapsedTime
        
        if self.time > self.interval:
            self.time = 0
            self.interval = (10 + random.randint(0, 6)) * 1000
            isWinning = self.myScore > self.enemyScore
            event = None
            
            if self.enemyGaveItem: 
                if self.enemyItemGiven.name == Chocolate.name:
                    if isWinning:
                        event = Event_GiveBallItem(HistoryBook(), False)
                    else:
                        event = Event_GiveBallItem(MeanNote(), False)
                elif self.enemyItemGiven.name == MeanNote.name:
                    if isWinning:
                        event = Event_GiveBallItem(HistoryBook(), False)
                    else:
                        event = Event_GiveBallItem(PsychoPill(), False)
                elif self.enemyItemGiven.name == SadPicture.name:
                    if isWinning:
                        event = Event_GiveBallItem(PsychoPill(), False)
                    else:
                        if ECOM.actorManager.extraBallExists(ballBored.BallBored):
                            event = Event_GiveBallItem(WinningTicket(), False)
                        else:
                            event = Event_GiveBallItem(MeanNote(), False)
                elif self.enemyItemGiven.name == HistoryBook.name:
                    if isWinning:
                        if ECOM.actorManager.extraBallExists(ballAngry.BallAngry):
                            event = Event_GiveBallItem(WinningTicket(), False)
                        else:
                            event = Event_GiveBallItem(PsychoPill(), False)
                    else:
                        event = Event_GiveBallItem(SadPicture(), False)
                elif self.enemyItemGiven.name == WinningTicket.name:
                    if isWinning:
                        if ECOM.actorManager.extraBallExists(ballAngry.BallAngry):
                            event = Event_GiveBallItem(HistoryBook(), False)
                        else:
                            event = Event_GiveBallItem(MeanNote(), False)
                    else:
                        if ECOM.actorManager.extraBallExists(ballBored.BallBored):
                            event = Event_GiveBallItem(SadPicture(), False)
                        else:
                            event = Event_GiveBallItem(PsychoPill(), False)
                elif self.enemyItemGiven.name == PsychoPill.name:
                    if isWinning:
                        event = Event_GiveBallItem(HistoryBook(), False)
                    else:
                        event = Event_GiveBallItem(MeanNote(), False)
            else:
                if isWinning:
                    event = Event_GiveBallItem(HistoryBook(), False)
                else:
                    event = Event_GiveBallItem(MeanNote(), False)
            
            if event is not None:
                ECOM.eventManager.queueEvent(event)
                self.enemyGaveItem = False
                self.enemyItemGiven = None
        
    def adjustScore(self, event):
        self.myScore = event.rightScore
        self.enemyScore = event.leftScore
    
    def itemGiven(self, event):
        if event.isPlayerOne:
            self.enemyGaveItem = True
            self.enemyItemGiven = event.item
            