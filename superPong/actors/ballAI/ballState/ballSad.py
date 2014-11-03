'''
Created on Nov 2, 2014

@author: Arrington
'''

from pyHopeEngine import engineCommon as ECOM
from superPong.actors.ballAI.ballState.ballState import BallState

class BallSad(BallState): #Goal: Feels down, stays on bottom half of screen
    def __init__(self, ball):
        super().__init__(ball)
        transformComp = self.ball.getComponent('TransformComponent')
        pos = transformComp.pos
        rotation = transformComp.rotation
        
        file = 'Images\PongBallSad.png'
        renderComp = self.ball.getComponent('RenderComponent')
        renderComp.spriteFile = file
        renderComp.sceneNode.addSpriteImage(file, pos, rotation)
        
        self.aboveHalf = False;
        if pos.y < ECOM.Screen.halfH:
            self.aboveHalf = True;
        
    def update(self):
        transformComp = self.ball.getComponent('TransformComponent')
        pos = transformComp.pos
        
        if not self.aboveHalf:
            physicsComp = self.ball.getComponent("PhysicsComponent")
            velocity = physicsComp.physics.getVelocity(self.ball.actorID)
            
            if pos.y < ECOM.Screen.halfH:
                velocity.y = -velocity.y
        else:
            if pos.y > ECOM.Screen.halfH:
                self.aboveHalf = False;