'''
Created on Jan 13, 2015

@author: Devon
'''

from pyHopeEngine import engineCommon as ECOM
from superPong.actors.ballAI.ballState import ballAngry, ballBored, ballCrazy, ballExcited, ballHappy, ballSad
from superPong.events.pongEvents import Event_AddBall, Event_DestroyExtraBall
from superPong.actors.ballAI.pongBallBrain import Moods


MIN_EMO_CHANGE = 5
MAX_EMO_CHANGE = MIN_EMO_CHANGE * 3
ENHANCE_MAX_EMO = MIN_EMO_CHANGE * 4
ENHANCE_MIN_EMO = MIN_EMO_CHANGE * 2
REDUCED_EMO = round(MIN_EMO_CHANGE / 2)

class BaseItem:
    name = None
    
    def __init__(self):
        pass
    
    def updateEmotions(self, emotions):
        raise NotImplementedError(self.name + " didn't implement updateEmotions")

    def comboUpdateEmotions(self, emotions, itemName):
        raise NotImplementedError(self.name + " didn't implement comboUpdateEmotions")
    
    def setScore(self, score):
        return max(min(score, 100), 1)


class Chocolate(BaseItem):
    name = "Chocolate"
    
    def __init__(self):
        pass
    
    def updateEmotions(self, emotions):
        emotions[Moods.Happy] = self.setScore(emotions[Moods.Happy] + MAX_EMO_CHANGE)
        emotions[Moods.Excited] = self.setScore(emotions[Moods.Excited] + MIN_EMO_CHANGE)
        emotions[Moods.Sad] = self.setScore(emotions[Moods.Sad] - MIN_EMO_CHANGE)
        
    def comboUpdateEmotions(self, emotions, itemName):
        if itemName == Chocolate.name:
            emotions[Moods.Happy] = self.setScore(emotions[Moods.Happy] + ENHANCE_MAX_EMO)
            emotions[Moods.Excited] = self.setScore(emotions[Moods.Excited] + ENHANCE_MIN_EMO)
            emotions[Moods.Sad] = self.setScore(emotions[Moods.Sad] - ENHANCE_MIN_EMO)
        elif itemName == WinningTicket.name:
            emotions[Moods.Happy] = self.setScore(emotions[Moods.Happy] + ENHANCE_MAX_EMO)
            emotions[Moods.Excited] = self.setScore(emotions[Moods.Excited] + ENHANCE_MIN_EMO)
            emotions[Moods.Sad] = self.setScore(emotions[Moods.Sad] - ENHANCE_MIN_EMO)
            event = Event_DestroyExtraBall(ballAngry.BallAngry)
            ECOM.eventManager.queueEvent(event)
            event = Event_DestroyExtraBall(ballSad.BallSad)
            ECOM.eventManager.queueEvent(event)
            event = Event_DestroyExtraBall(ballBored.BallBored)
            ECOM.eventManager.queueEvent(event)
        elif itemName == PsychoPill.name:
            event = Event_AddBall(ballHappy.BallHappy)
            ECOM.eventManager.queueEvent(event)

class MeanNote(BaseItem):
    name = "MeanNote"
    
    def __init__(self):
        pass

    def updateEmotions(self, emotions):
        emotions[Moods.Angry] = self.setScore(emotions[Moods.Angry] + MAX_EMO_CHANGE)
        emotions[Moods.Sad] = self.setScore(emotions[Moods.Sad] + MIN_EMO_CHANGE)
        emotions[Moods.Happy] = self.setScore(emotions[Moods.Happy] - MIN_EMO_CHANGE)

    def comboUpdateEmotions(self, emotions, itemName):
        if itemName == MeanNote.name:
            emotions[Moods.Angry] = self.setScore(emotions[Moods.Angry] + ENHANCE_MAX_EMO)
            emotions[Moods.Sad] = self.setScore(emotions[Moods.Sad] + ENHANCE_MIN_EMO)
            emotions[Moods.Happy] = self.setScore(emotions[Moods.Happy] - ENHANCE_MIN_EMO) 
        elif itemName == Chocolate.name:
            emotions[Moods.Angry] = self.setScore(emotions[Moods.Angry] + ENHANCE_MIN_EMO)
            emotions[Moods.Sad] = self.setScore(emotions[Moods.Sad] + REDUCED_EMO)
            emotions[Moods.Happy] = self.setScore(emotions[Moods.Happy] - REDUCED_EMO)
            event = Event_DestroyExtraBall(ballCrazy.BallCrazy)
            ECOM.eventManager.queueEvent(event)
        elif itemName == SadPicture.name:
            emotions[Moods.Angry] = self.setScore(emotions[Moods.Angry] + ENHANCE_MAX_EMO)
            emotions[Moods.Sad] = self.setScore(emotions[Moods.Sad] + ENHANCE_MIN_EMO)
            emotions[Moods.Happy] = self.setScore(emotions[Moods.Happy] - ENHANCE_MIN_EMO)
            event = Event_DestroyExtraBall(ballHappy.BallHappy)
            ECOM.eventManager.queueEvent(event)
            event = Event_DestroyExtraBall(ballExcited.BallExcited)
            ECOM.eventManager.queueEvent(event)
        elif itemName == WinningTicket.name:
            emotions[Moods.Bored] = self.setScore(emotions[Moods.Bored] + ENHANCE_MIN_EMO)
            event = Event_DestroyExtraBall(ballCrazy.BallCrazy)
            ECOM.eventManager.queueEvent(event)
        elif itemName == PsychoPill.name:
            event = Event_AddBall(ballAngry.BallAngry)
            ECOM.eventManager.queueEvent(event)


class SadPicture(BaseItem):
    name = "SadPicture"
    
    def __init__(self):
        pass

    def updateEmotions(self, emotions):
        emotions[Moods.Sad] = self.setScore(emotions[Moods.Sad] + MAX_EMO_CHANGE)
        emotions[Moods.Angry] = self.setScore(emotions[Moods.Angry] + MIN_EMO_CHANGE)
        emotions[Moods.Happy] = self.setScore(emotions[Moods.Happy] - MIN_EMO_CHANGE)

    def comboUpdateEmotions(self, emotions, itemName):
        if itemName == SadPicture.name:
            emotions[Moods.Sad] = self.setScore(emotions[Moods.Sad] + ENHANCE_MAX_EMO)
            emotions[Moods.Angry] = self.setScore(emotions[Moods.Angry] + ENHANCE_MIN_EMO)
            emotions[Moods.Happy] = self.setScore(emotions[Moods.Happy] - ENHANCE_MIN_EMO)  
        elif itemName == Chocolate.name:
            emotions[Moods.Sad] = self.setScore(emotions[Moods.Sad] + ENHANCE_MIN_EMO)
            emotions[Moods.Angry] = self.setScore(emotions[Moods.Angry] + REDUCED_EMO)
            emotions[Moods.Happy] = self.setScore(emotions[Moods.Happy] - REDUCED_EMO)
            event = Event_DestroyExtraBall(ballCrazy.BallCrazy)
            ECOM.eventManager.queueEvent(event)
        elif itemName == MeanNote.name:
            emotions[Moods.Sad] = self.setScore(emotions[Moods.Sad] + ENHANCE_MAX_EMO)
            emotions[Moods.Angry] = self.setScore(emotions[Moods.Angry] + ENHANCE_MIN_EMO)
            emotions[Moods.Happy] = self.setScore(emotions[Moods.Happy] - ENHANCE_MIN_EMO)
        elif itemName == HistoryBook.name:
            emotions[Moods.Angry] = self.setScore(emotions[Moods.Angry] + ENHANCE_MIN_EMO)
            event = Event_DestroyExtraBall(ballHappy.BallHappy)
            ECOM.eventManager.queueEvent(event)
            event = Event_DestroyExtraBall(ballExcited.BallExcited)
            ECOM.eventManager.queueEvent(event)
        elif itemName == WinningTicket.name:
            event = Event_DestroyExtraBall(ballBored.BallBored)
            ECOM.eventManager.queueEvent(event)
        elif itemName == PsychoPill.name:
            event = Event_AddBall(ballSad.BallSad)
            ECOM.eventManager.queueEvent(event)


class HistoryBook(BaseItem):
    name = "HistoryBook"
    
    def __init__(self):
        pass
    
    def updateEmotions(self, emotions):
        emotions[Moods.Bored] = self.setScore(emotions[Moods.Bored] + MAX_EMO_CHANGE)
        emotions[Moods.Sad] = self.setScore(emotions[Moods.Sad] - MIN_EMO_CHANGE)
        emotions[Moods.Excited] = self.setScore(emotions[Moods.Excited] - MIN_EMO_CHANGE)
        
    def comboUpdateEmotions(self, emotions, itemName):
        if itemName == HistoryBook.name:
            emotions[Moods.Bored] = self.setScore(emotions[Moods.Bored] + ENHANCE_MAX_EMO)
            emotions[Moods.Sad] = self.setScore(emotions[Moods.Sad] - ENHANCE_MIN_EMO)
            emotions[Moods.Excited] = self.setScore(emotions[Moods.Excited] - ENHANCE_MIN_EMO)
            event = Event_DestroyExtraBall(ballAngry.BallAngry)
            ECOM.eventManager.queueEvent(event)
            event = Event_DestroyExtraBall(ballSad.BallSad)
            ECOM.eventManager.queueEvent(event)
        elif itemName == Chocolate.name or itemName == WinningTicket.name:
            emotions[Moods.Bored] = self.setScore(emotions[Moods.Bored] + ENHANCE_MIN_EMO)
            emotions[Moods.Sad] = self.setScore(emotions[Moods.Sad] - REDUCED_EMO)
            emotions[Moods.Excited] = self.setScore(emotions[Moods.Excited] - REDUCED_EMO)
            event = Event_DestroyExtraBall(ballCrazy.BallCrazy)
            ECOM.eventManager.queueEvent(event)
        elif itemName == PsychoPill.name:
            event = Event_AddBall(ballBored.BallBored)
            ECOM.eventManager.queueEvent(event)
    

class WinningTicket(BaseItem):
    name = "WinningTicket"
    
    def __init__(self):
        pass
    
    def updateEmotions(self, emotions):
        emotions[Moods.Excited] = self.setScore(emotions[Moods.Excited] + MAX_EMO_CHANGE)
        emotions[Moods.Happy] = self.setScore(emotions[Moods.Happy] + MIN_EMO_CHANGE)
        emotions[Moods.Bored] = self.setScore(emotions[Moods.Bored] - MIN_EMO_CHANGE)

    def comboUpdateEmotions(self, emotions, itemName):
        if itemName == WinningTicket.name:
            emotions[Moods.Excited] = self.setScore(emotions[Moods.Excited] + ENHANCE_MAX_EMO)
            emotions[Moods.Happy] = self.setScore(emotions[Moods.Happy] + ENHANCE_MIN_EMO)
            emotions[Moods.Bored] = self.setScore(emotions[Moods.Bored] - ENHANCE_MIN_EMO)
        elif itemName == Chocolate.name:
            emotions[Moods.Excited] = self.setScore(emotions[Moods.Excited] + ENHANCE_MAX_EMO)
            emotions[Moods.Happy] = self.setScore(emotions[Moods.Happy] + ENHANCE_MIN_EMO)
            emotions[Moods.Bored] = self.setScore(emotions[Moods.Bored] - ENHANCE_MIN_EMO)
        elif itemName == PsychoPill.name:
            event = Event_AddBall(ballExcited.BallExcited)
            ECOM.eventManager.queueEvent(event)
    

class PsychoPill(BaseItem):
    name = "PsychoPill"
    isFirstPill = True
    
    def __init__(self):
        pass

    def updateEmotions(self, emotions):
        emotions[Moods.Crazy] = self.setScore(emotions[Moods.Crazy] + MAX_EMO_CHANGE)
        
    def comboUpdateEmotions(self, emotions, itemName):
        if itemName == PsychoPill.name and PsychoPill.isFirstPill:
            emotions[Moods.Crazy] = self.setScore(emotions[Moods.Crazy] + ENHANCE_MAX_EMO)
            event = Event_AddBall(ballHappy.BallHappy)
            ECOM.eventManager.queueEvent(event)
            event = Event_AddBall(ballAngry.BallAngry)
            ECOM.eventManager.queueEvent(event)
            event = Event_AddBall(ballSad.BallSad)
            ECOM.eventManager.queueEvent(event)
            event = Event_AddBall(ballBored.BallBored)
            ECOM.eventManager.queueEvent(event)
            event = Event_AddBall(ballExcited.BallExcited)
            ECOM.eventManager.queueEvent(event)
            event = Event_AddBall(ballCrazy.BallCrazy)
            ECOM.eventManager.queueEvent(event)
            
            PsychoPill.isFirstPill = False
        elif not PsychoPill.isFirstPill:
            emotions[Moods.Crazy] = self.setScore(emotions[Moods.Crazy] + ENHANCE_MAX_EMO)
            PsychoPill.isFirstPill = True
        
        
            