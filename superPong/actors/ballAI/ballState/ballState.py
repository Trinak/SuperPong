'''
Created on Oct 30, 2014

@author: Arrington
'''

class BallState(object):
    def __init__(self, ball):
        self.ball = ball
        self.MAX_VELOCITY = 500
        self.MIN_VELOCITY = 150
        self.AVG_VELOCITY = (self.MAX_VELOCITY + self.MIN_VELOCITY) / 2
    
    def init(self):
        pass
    
    def update(self):
        pass
    
    def cleanUp(self):
        physicsComp = self.ball.getComponent("PhysicsComponent")
        if physicsComp is not None and physicsComp.physics is not None:
            physicsComp.changeVelocityMod(self.AVG_VELOCITY)