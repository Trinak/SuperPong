'''
Created on Feb 18, 2015

@author: Arrington
'''

from pyHopeEngine import Process

class DisableGiveItemProcess(Process):
    def __init__(self, UI, disablePlayer = True):
        super().__init__()
        self.interval = 10 * 1000 #10 seconds
        self.time = 0
        self.UI = UI
        self.disablePlayer = disablePlayer
        if self.disablePlayer:
            self.UI.disabledImagesPlayer = True
        else:
            self.UI.disabledImagesEnemy = True
            
        self.UI.widget.remove_row(0)
        self.UI.createTopUI()
    
    def update(self, elapsedTime):
        self.time += elapsedTime
        
        if self.time > self.interval:
            if self.disablePlayer:
                self.UI.disabledImagesPlayer = False
                self.UI.playerItemGiven = None
            else:
                self.UI.disabledImagesEnemy = False
                self.UI.opponentItemGiven = None
                
            self.UI.widget.remove_row(0)
            self.UI.createTopUI()
            self.succeed()
            