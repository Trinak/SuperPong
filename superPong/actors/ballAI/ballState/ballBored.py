'''
Created on Nov 2, 2014

@author: Arrington
'''

from pyHopeEngine import engineCommon as ECOM
from superPong.actors.ballAI.ballState.ballState import BallState
from superPong.events.pongEvents import Event_BallGoal, Event_RequestCurrentScore

class BallBored(BallState): #Goal: Bored with game. Supports whoever is winning. 
    def __init__(self, ball):
        super().__init__(ball)
        transformComp = self.ball.getComponent('TransformComponent')
        pos = transformComp.pos
        rotation = transformComp.rotation
        self.leftScore = 0
        self.rightScore = 0
        self.MAX_VELOCITY = 500
        self.MIN_VELOCITY = 150
        event = Event_RequestCurrentScore(self)
        ECOM.eventManager.triggerEvent(event)
        
        file = 'Images\PongBallBored.png'
        renderComp = self.ball.getComponent('RenderComponent')
        renderComp.spriteFile = file
        renderComp.sceneNode.addSpriteImage(file, pos, rotation)
        
        ECOM.eventManager.addListener(self.handleGoal, Event_BallGoal.eventType)
    
    def setScores(self, leftScore, rightScore):
        self.leftScore = leftScore
        self.rightScore = rightScore
    
    def update(self):
        physicsComp = self.ball.getComponent("PhysicsComponent")
        velocityMod = physicsComp.velocityMod
        velocity = physicsComp.physics.getVelocity(self.ball.actorID)
        
        #ball will favor right side           
        if self.rightScore < self.leftScore:
            if velocity.x > 0: #ball going right
                velocityMod +=15
                if velocityMod > self.MAX_VELOCITY:
                    velocityMod = self.MAX_VELOCITY 
                physicsComp.changeVelocityMod(velocityMod)
            else:
                velocityMod -= 10
                if velocityMod < self.MIN_VELOCITY:
                    velocityMod = self.MIN_VELOCITY
                physicsComp.changeVelocityMod(velocityMod)
                
        #ball will favor left side
        elif self.leftScore < self.rightScore:
            if velocity.x < 0: #ball going left
                velocityMod += 15
                if velocityMod > self.MAX_VELOCITY:
                    velocityMod = self.MAX_VELOCITY
                physicsComp.changeVelocityMod(velocityMod)
            else:
                velocityMod -= 10
                if velocityMod < self.MIN_VELOCITY:
                    velocityMod = self.MIN_VELOCITY
                physicsComp.changeVelocityMod(velocityMod)
    
    def handleGoal(self, event):
        self.leftScore = event.leftScore
        self.rightScore = event.rightScore
        
        if self.leftScore == self.rightScore:
            physicsComp = self.ball.getComponent("PhysicsComponent")
            velocityMod = physicsComp.velocityMod
            if velocityMod < 300:
                velocityMod = 300
                physicsComp.changeVelocityMod(velocityMod)       
    
    def cleanUp(self):
        super().cleanUp()
        ECOM.eventManager.removeListener(self.handleGoal, Event_BallGoal.eventType) 