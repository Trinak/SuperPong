'''
Created on Dec 23, 2014

@author: Arrington
'''

from pyHopeEngine import Process
from pyHopeEngine import engineCommon as ECOM
from superPong.actors.ballAI.ballState import *
from superPong.actors.items.items import *
from superPong.events.pongEvents import Event_GiveBallItem, Event_BallGoal
from superPong.actors.ballAI.ballState.ballBored import BallBored

class PaddleGiveItemProcess(Process):
    def __init__(self):
        super().__init__()
        self.interval = 10 * 1000 #10 seconds
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
            isWinning = self.myScore > self.enemyScore
            event = None
            
            if self.enemyGaveItem: 
                if self.enemyItemGiven.name == Chocolate.name:
                    if isWinning:
                        event = Event_GiveBallItem(HistoryBook())
                    else:
                        event = Event_GiveBallItem(MeanNote())
                elif self.enemyItemGiven.name == MeanNote.name:
                    if isWinning:
                        event = Event_GiveBallItem(HistoryBook())
                    else:
                        event = Event_GiveBallItem(PsychoPill())
                elif self.enemyItemGiven.name == SadPicture.name:
                    if isWinning:
                        event = Event_GiveBallItem(PsychoPill())
                    else:
                        if ECOM.actorManager.extraBallExists(ballBored.BallBored):
                            event = Event_GiveBallItem(WinningTicket())
                        else:
                            event = Event_GiveBallItem(MeanNote())
                elif self.enemyItemGiven.name == HistoryBook.name:
                    if isWinning:
                        if ECOM.actorManager.extraBallExists(ballAngry.BallAngry):
                            event = Event_GiveBallItem(WinningTicket())
                        else:
                            event = Event_GiveBallItem(PsychoPill())
                    else:
                        event = Event_GiveBallItem(SadPicture())
                elif self.enemyItemGiven.name == WinningTicket.name:
                    if isWinning:
                        if ECOM.actorManager.extraBallExists(ballAngry.BallAngry):
                            event = Event_GiveBallItem(HistoryBook())
                        else:
                            event = Event_GiveBallItem(MeanNote())
                    else:
                        if ECOM.actorManager.extraBallExists(ballBored.BallBored):
                            event = Event_GiveBallItem(SadPicture())
                        else:
                            event = Event_GiveBallItem(PsychoPill())
                elif self.enemyItemGiven.name == PsychoPill.name:
                    if isWinning:
                        event = Event_GiveBallItem(HistoryBook())
                    else:
                        event = Event_GiveBallItem(MeanNote())
            else:
                if isWinning:
                    event = Event_GiveBallItem(HistoryBook())
                else:
                    event = Event_GiveBallItem(MeanNote())
            
            if event is not None:
                ECOM.eventManager.queueEvent(event)
        
    def adjustScore(self, event):
        self.myScore = event.rightScore
        self.enemyScore = event.leftScore
    
    def itemGiven(self, event):
        if event.isPlayerOne:
            self.enemyGaveItem = True
            self.enemyItemGiven = event.item
            