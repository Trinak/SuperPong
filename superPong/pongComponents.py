'''
Created on Jul 23, 2013

@author: Devon
'''

from pyHopeEngine import engineCommon as ECOM
from pyHopeEngine import Process
from pyHopeEngine.actors.components.physicsComponent import PhysicsComponent
from pyHopeEngine.actors.components.aiComponent import AIComponent
from pyHopeEngine import Event_Accelerate
from superPong.pongController import ACCELERATION
from superPong.pongBallAI import SimpleBallBrain, BallProcess

class PaddlePhysicsComponent(PhysicsComponent):
    def __init__(self):
        super().__init__()
        self.grooveJoint = {}
        
    def init(self, element):
        super().init(element)
    
    def setProperties(self, element):
        super().setProperties(element)
        
        element = element.find("GrooveJoint")
        self.grooveJoint['groove_a'] = self.findProperty(element, "GrooveA", (0, 0))
        self.grooveJoint['groove_b'] = self.findProperty(element, "GrooveB", (0, 0))
        self.grooveJoint['anchr2'] = self.findProperty(element, "Anchr2", (0, 0))
    
    def postInit(self):
        super().postInit()
        
        self.physics.addConstraint("GrooveJoint", None, self.owner.actorID, **self.grooveJoint)
        
    
class PongPaddleAIComponent(AIComponent):
    def __init__(self):
        super().__init__()
    
    def init(self, element):
        pass
    
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


class BallAIProcess(Process):
    def __init__(self, comp):
        super().__init__()
        self.interval = 2 * 1000 # 3 seconds
        self.time = 0
        self.aiComponent = comp
        
    def update(self, time):
        self.time += time
        
        if self.time > self.interval:
            self.time = 0
            self.aiComponent.updateProcess()
            

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
    
    