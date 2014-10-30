'''
Created on Jun 4, 2013

@author: Devon
'''

import os
import sys

from pyHopeEngine import PyHopeEngineApp
from superPong.main.pongLogic import PongLogic
from superPong.main.pongGameStates import MainMenuState
from superPong.humanView.pongView import MainMenuView

class PongApp(PyHopeEngineApp):
    def __init__(self):
        super().__init__()
        self.caption = "Super Pong"
        
        if hasattr(sys, "frozen"):
            path = os.path.dirname(sys.executable)
        else:
            path = os.path.normpath(os.path.dirname(__file__) + "\..\..")
            
        self.resourceManager.setDataDir(path, "Assets")
        
        
    def createLogicAndView(self):
        self.baseLogic = PongLogic()
        view = MainMenuView()
        self.baseLogic.addView(view)
        state = MainMenuState()
        self.baseLogic.changeState(state)
        

if __name__ == '__main__':
    pongApp = PongApp()
    pongApp.run()