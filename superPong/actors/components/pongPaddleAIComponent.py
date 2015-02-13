'''
Created on Oct 30, 2014

@author: Arrington
'''

from pyHopeEngine import engineCommon as ECOM
from pyHopeEngine.actors.components.aiComponent import AIComponent
from pyHopeEngine import Event_Accelerate
from superPong.humanView.pongController import ACCELERATION
from superPong.actors.paddleAI.paddleGiveItemProcess import PaddleGiveItemProcess

class PongPaddleAIComponent(AIComponent):
    def __init__(self):
        super().__init__()
        self.giveItemProcess = None
    
    def init(self, element):
        self.giveItemProcess = PaddleGiveItemProcess()
        ECOM.engine.baseLogic.processManager.addProcess(self.giveItemProcess)
    
    def postInit(self):
        pass
    
    def update(self):
        pos = self.owner.getComponent("TransformComponent").pos
        ballPos = ECOM.engine.baseLogic.actorManager.getBall().getComponent("TransformComponent").pos
        
        if (pos.y) > ballPos.y:
            event = Event_Accelerate(self.owner.actorID, -ACCELERATION)
            ECOM.eventManager.queueEvent(event)
        
        if (pos.y) < ballPos.y:
            event = Event_Accelerate(self.owner.actorID, ACCELERATION)
            ECOM.eventManager.queueEvent(event)
    
    def cleanUp(self):
        pass
