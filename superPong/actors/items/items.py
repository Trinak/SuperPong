'''
Created on Jan 13, 2015

@author: Devon
'''

from pyHopeEngine import engineCommon as ECOM
from superPong.actors.ballAI.ballState import *
from superPong.events.pongEvents import Event_AddBall
from superPong.actors.ballAI.pongBallBrain import Moods


MIN_EMO_CHANGE = 5
MAX_EMO_CHANGE = MIN_EMO_CHANGE * 3
ENHANCE_MAX_EMO = MIN_EMO_CHANGE * 4
ENHANCE_MIN_EMO = MIN_EMO_CHANGE * 2
REDUCED_EMO = MIN_EMO_CHANGE / 2

class BaseItem:
    def __init__(self):
        self.name = None
    
    def updateEmotions(self, emotions):
        raise NotImplementedError(self.name + " didn't implement updateEmotions")

    def comboUpdateEmotions(self, emotions, itemName):
        raise NotImplementedError(self.name + " didn't implement comboUpdateEmotions")
    
    def setScore(self, score):
        return max(min(score, 100), 1)


class Chocolate(BaseItem):
    def __init__(self):
        self.name = "Chocolate"
    
    def updateEmotions(self, emotions):
        emotions[Moods.Happy] = self.setScore(emotions[Moods.Happy] + MAX_EMO_CHANGE)
        emotions[Moods.Excited] = self.setScore(emotions[Moods.Excited] + MIN_EMO_CHANGE)
        emotions[Moods.Sad] = self.setScore(emotions[Moods.Sad] - MIN_EMO_CHANGE)
        event = Event_AddBall(ballHappy.BallHappy)
        ECOM.eventManager.queueEvent(event)
        
    def comboUpdateEmotions(self, emotions, itemName):
        if itemName == WinningTicket.name:
            emotions[Moods.Happy] = self.setScore(emotions[Moods.Happy] + ENHANCE_MAX_EMO)
            emotions[Moods.Excited] = self.setScore(emotions[Moods.Excited] + ENHANCE_MIN_EMO)
            emotions[Moods.Sad] = self.setScore(emotions[Moods.Sad] - ENHANCE_MIN_EMO)
        elif itemName == PsychoPill.name:
            event = Event_AddBall(ballHappy.BallHappy)
            ECOM.eventManager.queueEvent(event)

class MeanNote(BaseItem):
    def __init__(self):
        self.name = "MeanNote"

    def updateEmotions(self, emotions):
        emotions[Moods.Angry] = self.setScore(emotions[Moods.Angry] + MAX_EMO_CHANGE)
        emotions[Moods.Sad] = self.setScore(emotions[Moods.Sad] + MIN_EMO_CHANGE)
        emotions[Moods.Happy] = self.setScore(emotions[Moods.Happy] - MIN_EMO_CHANGE)

    def comboUpdateEmotions(self, emotions, itemName):
        if itemName == Chocolate.name:
            emotions[Moods.Angry] = self.setScore(emotions[Moods.Angry] + ENHANCE_MIN_EMO)
            emotions[Moods.Sad] = self.setScore(emotions[Moods.Sad] + REDUCED_EMO)
            emotions[Moods.Happy] = self.setScore(emotions[Moods.Happy] - REDUCED_EMO)
        elif itemName == SadPicture.name:
            emotions[Moods.Angry] = self.setScore(emotions[Moods.Angry] + ENHANCE_MAX_EMO)
            emotions[Moods.Sad] = self.setScore(emotions[Moods.Sad] + ENHANCE_MIN_EMO)
            emotions[Moods.Happy] = self.setScore(emotions[Moods.Happy] - ENHANCE_MIN_EMO)
        elif itemName == WinningTicket.name:
            emotions[Moods.Bored] = self.setScore(emotions[Moods.Bored] + ENHANCE_MIN_EMO)


class SadPicture(BaseItem):
    def __init__(self):
        self.name = "SadPicture"

    def updateEmotions(self, emotions):
        emotions[Moods.Sad] = self.setScore(emotions[Moods.Sad] + MAX_EMO_CHANGE)
        emotions[Moods.Angry] = self.setScore(emotions[Moods.Angry] + MIN_EMO_CHANGE)
        emotions[Moods.Happy] = self.setScore(emotions[Moods.Happy] - MIN_EMO_CHANGE)

    def comboUpdateEmotions(self, emotions, itemName):
        if itemName == Chocolate.name:
            emotions[Moods.Sad] = self.setScore(emotions[Moods.Sad] + ENHANCE_MIN_EMO)
            emotions[Moods.Angry] = self.setScore(emotions[Moods.Angry] + REDUCED_EMO)
            emotions[Moods.Happy] = self.setScore(emotions[Moods.Happy] - REDUCED_EMO)
        elif itemName == MeanNote.name:
            emotions[Moods.Sad] = self.setScore(emotions[Moods.Sad] + ENHANCE_MAX_EMO)
            emotions[Moods.Angry] = self.setScore(emotions[Moods.Angry] + ENHANCE_MIN_EMO)
            emotions[Moods.Happy] = self.setScore(emotions[Moods.Happy] - ENHANCE_MIN_EMO)
        elif itemName == HistoryBook.name:
            emotions[Moods.Angry] = self.setScore(emotions[Moods.Angry] + ENHANCE_MIN_EMO)


class HistoryBook(BaseItem):
    def __init__(self):
        self.name = "HistoryBook"
    
    def updateEmotions(self, emotions):
        emotions[Moods.Bored] = self.setScore(emotions[Moods.Bored] + MAX_EMO_CHANGE)
        emotions[Moods.Sad] = self.setScore(emotions[Moods.Sad] - MIN_EMO_CHANGE)
        emotions[Moods.Excited] = self.setScore(emotions[Moods.Excited] - MIN_EMO_CHANGE)
        
    def comboUpdateEmotions(self, emotions, itemName):
        if itemName == Chocolate.name or itemName == WinningTicket.name:
            emotions[Moods.Bored] = self.setScore(emotions[Moods.Bored] + ENHANCE_MIN_EMO)
            emotions[Moods.Sad] = self.setScore(emotions[Moods.Sad] - REDUCED_EMO)
            emotions[Moods.Excited] = self.setScore(emotions[Moods.Excited] - REDUCED_EMO)
    

class WinningTicket(BaseItem):
    def __init__(self):
        self.name = "WinningTicket"
    
    def updateEmotions(self, emotions):
        emotions[Moods.Excited] = self.setScore(emotions[Moods.Excited] + MAX_EMO_CHANGE)
        emotions[Moods.Happy] = self.setScore(emotions[Moods.Happy] + MIN_EMO_CHANGE)
        emotions[Moods.Bored] = self.setScore(emotions[Moods.Bored] - MIN_EMO_CHANGE)

    def comboUpdateEmotions(self, emotions, itemName):
        if itemName == Chocolate.name:
            emotions[Moods.Excited] = self.setScore(emotions[Moods.Excited] + ENHANCE_MAX_EMO)
            emotions[Moods.Happy] = self.setScore(emotions[Moods.Happy] + ENHANCE_MIN_EMO)
            emotions[Moods.Bored] = self.setScore(emotions[Moods.Bored] - ENHANCE_MIN_EMO)
    

class PsychoPill(BaseItem):
    def __init__(self):
        self.name = "PsychoPill"

    def updateEmotions(self, emotions):
        emotions[Moods.Crazy] = self.setScore(emotions[Moods.Crazy] + MAX_EMO_CHANGE)
        
    def comboUpdateEmotions(self, emotions, itemName):
        pass