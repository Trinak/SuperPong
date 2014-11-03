'''
Created on Jul 27, 2013

@author: Devon
'''

from pyHopeEngine import ActorFactory
from superPong.actors.components import *

class PongActorFactory(ActorFactory):
    def __init__(self):
        super().__init__()
        
        self.componentDict["PaddlePhysicsComponent"] = paddlePhysicsComponent.PaddlePhysicsComponent
        self.componentDict["PongPaddleAIComponent"] = pongPaddleAIComponent.PongPaddleAIComponent
        self.componentDict["BallAIComponent"] = ballAIComponent.BallAIComponent
        