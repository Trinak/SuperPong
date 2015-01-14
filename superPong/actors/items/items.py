'''
Created on Jan 13, 2015

@author: Devon
'''

from superPong.actors.ballAI.pongBallBrain import Moods

class BaseItem:
    def __init__(self):
        pass
    
    def updateEmotions(self, emotions):
        raise NotImplementedError("Item didn't implement updateEmotions")
    
    def setScore(self, score):
        return max(min(score, 100), 1)


class Chocolate(BaseItem):
    def __init__(self):
        pass
    
    def updateEmotions(self, emotions):
        emotions[Moods.Happy] = self.setScore(emotions[Moods.Happy] + 30)
        emotions[Moods.Excited] = self.setScore(emotions[Moods.Excited] + 10)
        emotions[Moods.Sad] = self.setScore(emotions[Moods.Sad] - 10)
        
        return emotions


class MeanNote(BaseItem):
    def __init__(self):
        pass

    def updateEmotions(self, emotions):
        emotions[Moods.Angry] = self.setScore(emotions[Moods.Angry] + 30)
        emotions[Moods.Sad] = self.setScore(emotions[Moods.Sad] + 10)
        emotions[Moods.Happy] = self.setScore(emotions[Moods.Happy] - 10)

        return emotions


class SadPicture(BaseItem):
    def __init__(self):
        pass

    def updateEmotions(self, emotions):
        emotions[Moods.Sad] = self.setScore(emotions[Moods.Sad] + 30)
        emotions[Moods.Angry] = self.setScore(emotions[Moods.Angry] + 10)
        emotions[Moods.Happy] = self.setScore(emotions[Moods.Happy] - 10)

        return emotions


class HistoryBook(BaseItem):
    def __init__(self):
        pass
    
    def updateEmotions(self, emotions):
        emotions[Moods.Bored] = self.setScore(emotions[Moods.Bored] + 30)
        emotions[Moods.Sad] = self.setScore(emotions[Moods.Sad] - 10)
        emotions[Moods.Excited] = self.setScore(emotions[Moods.Excited] - 10)

        return emotions


class WinningTicket(BaseItem):
    def __init__(self):
        pass
    
    def updateEmotions(self, emotions):
        emotions[Moods.Excited] = self.setScore(emotions[Moods.Excited] + 30)
        emotions[Moods.Happy] = self.setScore(emotions[Moods.Happy] + 10)
        emotions[Moods.Bored] = self.setScore(emotions[Moods.Bored] - 10)

        return emotions


class PsychoPill(BaseItem):
    def __init__(self):
        pass

    def updateEmotions(self, emotions):
        emotions[Moods.Crazy] = self.setScore(emotions[Moods.Crazy] + 30)
        
        return emotions