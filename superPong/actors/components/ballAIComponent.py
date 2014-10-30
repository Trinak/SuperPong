'''
Created on Oct 30, 2014

@author: Arrington
'''

from pyHopeEngine import engineCommon as ECOM
from pyHopeEngine.actors.components.aiComponent import AIComponent
from superPong.actors.ballAI.ballAIProcess import BallAIProcess
from superPong.actors.pongBallAI import SimpleBallBrain, BallProcess

class BallAIComponent(AIComponent):
    def __init__(self):
        super().__init__()
        self.currentState = None
        self.brain = None
    
    def init(self, element):
        brainElement = element.find("Brain")
        self.setBrain(brainElement.text)
        ballProcess = BallProcess(self)
        aiProcess = BallAIProcess(self)
        ECOM.engine.baseLogic.processManager.addProcess(ballProcess)
        #ECOM.engine.baseLogic.processManager.addProcess(aiProcess)
        
    def postInit(self):
        self.brain.init(self.owner)
    
    def setBrain(self, name):
        if name == "SimpleBallBrain":
            self.brain = SimpleBallBrain()
    
    def setState(self, state):
        self.currentState = state(self.owner)
        self.currentState.init()
    
    def chooseState(self):
        if self.brain is not None:
            state = self.brain.think()
            
            self.setState(state)
    
    def update(self):
        if self.currentState is not None:
            self.currentState.update()
    
    def updateProcess(self):
        if self.currentState is not None:
            self.currentState.update()
    
    def cleanUp(self):
        pass