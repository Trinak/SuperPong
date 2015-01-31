'''
Created on Jan 19, 2015

@author: Arrington
'''

from pyHopeEngine import Process

class BallHandleItemProcess(Process):
    def __init__(self, item, ballBrain):
        super().__init__()
        self.interval = 2 * 1000 # 2 seconds
        self.time = 0
        self.itemOne = item
        self.itemTwo = None
        self.ballBrain = ballBrain
        
    def update(self, elapsedTime):
        self.time += elapsedTime
        
        if self.time > self.interval:
            if self.itemTwo is None:
                self.itemOne.updateEmotions(self.ballBrain.emotionalScores)
            else:
                self.itemOne.comboUpdateEmotions(self.ballBrain.emotionalScores, self.itemTwo.name)
                self.itemTwo.comboUpdateEmotions(self.ballBrain.emotionalScores, self.itemOne.name)
    
            self.succeed()
            
    def addItem(self, item):
        self.itemTwo = item
    
    def onSuccess(self):
        self.ballBrain.handleItemProcess = None