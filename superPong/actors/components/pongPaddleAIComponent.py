'''
Created on Oct 30, 2014

@author: Arrington
'''

from pyHopeEngine import engineCommon as ECOM
from pyHopeEngine.actors.components.aiComponent import AIComponent
from pyHopeEngine import Event_ChangeVelocity
from superPong.humanView.pongController import VELOCITY
from superPong.actors.paddleAI.paddleGiveItemProcess import PaddleGiveItemProcess

class PongPaddleAIComponent(AIComponent):
    def __init__(self):
        super().__init__()
        self.giveItemProcess = None
        self.posAdjust = 50 
    
    def init(self, element):
        self.giveItemProcess = PaddleGiveItemProcess()
        ECOM.engine.baseLogic.processManager.addProcess(self.giveItemProcess)
    
    def postInit(self):
        pass
    
    def update(self):
        pos = self.owner.getComponent("TransformComponent").pos
        balls = ECOM.engine.baseLogic.actorManager.getBalls()
        closestBall = balls[0]
        for ball in balls:
            tempBallTransform = ball.getComponent("TransformComponent")
            closestBallTransform = closestBall.getComponent("TransformComponent")
            if tempBallTransform.velocityNormal.x > 0 and tempBallTransform.pos.x > closestBallTransform.pos.x:
                closestBall = ball
            
        ballPos = closestBall.getComponent("TransformComponent").pos
        
        if pos.y > (ballPos.y + self.posAdjust):
            event = Event_ChangeVelocity(self.owner.actorID, (0, -VELOCITY))
            ECOM.eventManager.queueEvent(event)
        
        if pos.y < (ballPos.y - self.posAdjust):
            event = Event_ChangeVelocity(self.owner.actorID, (0, VELOCITY))
            ECOM.eventManager.queueEvent(event)
    
    def cleanUp(self):
        pass
