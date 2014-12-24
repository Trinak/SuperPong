'''
Created on Dec 23, 2014

@author: Arrington
'''

from pyHopeEngine import Process
from pyHopeEngine import engineCommon as ECOM
from superPong.events.pongEvents import Event_GiveBallItem

class PaddleGiveItemProcess(Process):
    def __init__(self):
        super().__init__()
    
    def update(self, elapsedTime):
        pass