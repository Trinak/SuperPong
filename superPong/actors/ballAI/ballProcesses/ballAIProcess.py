'''
Created on Oct 30, 2014

@author: Arrington
'''

from pyHopeEngine import Process

class BallAIProcess(Process):
    def __init__(self, comp):
        super().__init__()
        self.interval = 2 * 1000 # 2 seconds
        self.time = 0
        self.aiComponent = comp
        
    def update(self, elapsedTime):
        self.time += elapsedTime
        
        if self.time > self.interval:
            self.time = 0
            self.aiComponent.updateProcess()
            
