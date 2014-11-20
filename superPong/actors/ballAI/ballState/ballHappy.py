'''
Created on Nov 2, 2014

@author: Arrington
'''

from superPong.actors.ballAI.ballState.ballState import BallState

class BallHappy(BallState):
    def __init__(self, ball):
        super().__init__(ball)
        transformComp = self.ball.getComponent('TransformComponent')
        pos = transformComp.pos
        rotation = transformComp.rotation
        
        file = 'Images\PongBallHappy.png'
        renderComp = self.ball.getComponent('RenderComponent')
        renderComp.spriteFile = file
        renderComp.sceneNode.addSpriteImage(file, pos, rotation)
