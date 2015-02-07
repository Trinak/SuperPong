'''
Created on Nov 2, 2014

@author: Arrington
'''

from pyHopeEngine import Process

class BallChooseStateProcess(Process):
    def __init__(self, comp):
        super().__init__()
        self.interval = 7 * 1000 # 7 seconds
        self.time = 0
        self.AIComponent = comp
        
    def update(self, time):
        self.time += time
        
        if self.time > self.interval:
            self.time = 0
            self.AIComponent.chooseState()
    
    def onSuccess(self):
        self.AIComponent = None