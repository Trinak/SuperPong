'''
Created on Jul 27, 2013

@author: Devon
'''

from pyHopeEngine import ActorFactory
from superPong.actors.pongComponents import PaddlePhysicsComponent, PongPaddleAIComponent, BallAIComponent

class PongActorFactory(ActorFactory):
    def __init__(self):
        super().__init__()
        
        self.componentDict["PaddlePhysicsComponent"] = PaddlePhysicsComponent
        self.componentDict["PongPaddleAIComponent"] = PongPaddleAIComponent
        self.componentDict["BallAIComponent"] = BallAIComponent
        