'''
Created on Oct 30, 2014

@author: Arrington
'''

from pyHopeEngine import engineCommon as ECOM
from pyHopeEngine.actors.components.aiComponent import AIComponent
from superPong.actors.ballAI.ballProcesses.ballChooseStateProcess import BallChooseStateProcess
from superPong.actors.ballAI.pongBallBrain import MainBallBrain, BasicBallBrain

class BallAIComponent(AIComponent):
    def __init__(self):
        super().__init__()
        self.currentState = None
        self.brain = None
        self.chooseStateProcess = None
    
    def init(self, element):
        brainElement = element.find("Brain")
        self.setBrain(brainElement.text)
        self.chooseStateProcess = BallChooseStateProcess(self)
        ECOM.engine.baseLogic.processManager.addProcess(self.chooseStateProcess)
        
    def postInit(self):
        self.currentState = self.brain.init(self.owner)
        self.currentState.init()
    
    def setBrain(self, name):
        if name == "MainBallBrain":
            self.brain = MainBallBrain()
        elif name == "BasicBallBrain":
            self.brain = BasicBallBrain()
    
    def setState(self, state):
        self.currentState.cleanUp()
        self.currentState = state(self.owner)
        self.currentState.init()
    
    def chooseState(self):
        if self.brain is not None:
            state = self.brain.think()
            
            if state is not None:
                self.setState(state)
    
    def update(self):
        if self.currentState is not None:
            self.currentState.update()
    
    def cleanUp(self):
        super().cleanUp()
        self.brain.cleanUp()
        self.brain = None
        self.currentState.cleanUp()
        self.currentState = None
        self.chooseStateProcess.succeed()
        self.chooseStateProcess = None