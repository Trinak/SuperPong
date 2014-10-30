'''
Created on Sep 17, 2013

@author: Devon
'''

import random

from pyHopeEngine import engineCommon as ECOM
from pyHopeEngine import Process
from pyHopeEngine import Event_ApplyImpulse
from pyHopeEngine import Vec2d
from superPong.events.pongEvents import Event_BallCollide, Event_BallGoal

class BallProcess(Process):
    def __init__(self, comp):
        super().__init__()
        self.interval = 7 * 1000 # 7 seconds
        self.time = 0
        self.stateMachine = comp
        
    def update(self, time):
        self.time += time
        
        if self.time > self.interval:
            self.time = 0
            self.stateMachine.chooseState()


class BallBrain(object):
    def __init__(self):
        self.ball = None
    
    
    def init(self, ball):
        self.ball = ball
    
    
    def think(self):
        pass


class SimpleBallBrain(BallBrain):
    def __init__(self):
        super().__init__()
        self.hitLeft = 0
        self.hitRight = 0
        self.name = "SimpleBallBrain"
        ECOM.eventManager.addListener(self.checkCollide, Event_BallCollide.eventType)
    
    def think(self):
        hits = self.hitLeft + self.hitRight
        if hits < 1:
            return BallHappy
        else:
            rand = random.randint(0, 6)
            if rand == 0:
                return BallHappy
            elif rand == 1:
                return BallCrazy
            elif rand == 2:
                return BallSad
            elif rand == 3:
                return BallExcited
            elif rand == 4:
                return BallAngry
            elif rand == 5:
                return BallBored
        
        return BallHappy
            
       
    def checkCollide(self, event):
        actor1 = ECOM.actorManager.getActor(event.actorID1)
        actor2 = ECOM.actorManager.getActor(event.actorID2)
        
        if actor1.actorID == self.ball.actorID:
            paddle = actor2
        elif actor2.actorID == self.ball.actorID:
            paddle = actor1
        else:
            return
        
        if paddle.type == 'PaddleOne':
            self.hitLeft += 1
        elif paddle.type == 'PaddleTwo':
            self.hitRight += 1


class BallHappy(BallState):
    def __init__(self, ball):
        super().__init__(ball)


class BallExcited(BallState): #Goal: Feels great, stays on top half of screen
    def __init__(self, ball):
        super().__init__(ball)
        transformComp = self.ball.getComponent('TransformComponent')
        pos = transformComp.pos
        rotation = transformComp.rotation
        
        file = 'Images\PongBallExcited.png'
        renderComp = self.ball.getComponent('RenderComponent')
        renderComp.spriteFile = file
        renderComp.sceneNode.addSpriteImage(file, pos, rotation)
        
        self.belowHalf = False;
        if pos.y > ECOM.Screen.halfH:
            self.belowHalf = True;
        
    def update(self):
        transformComp = self.ball.getComponent('TransformComponent')
        pos = transformComp.pos
        
        if not self.belowHalf:
            physicsComp = self.ball.getComponent("PhysicsComponent")
            velocity = physicsComp.physics.getVelocity(self.ball.actorID)
            
            if pos.y > ECOM.Screen.halfH:
                velocity.y = -velocity.y
        else:
            if pos.y < ECOM.Screen.halfH:
                self.belowHalf = False;


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
            

class BallCrazy(BallState): #Goal: None, move randomly
    def __init__(self, ball):
        super().__init__(ball)
        transformComp = self.ball.getComponent('TransformComponent')
        pos = transformComp.pos
        rotation = transformComp.rotation
        
        file = 'Images\PongBallCrazy.png'
        renderComp = self.ball.getComponent('RenderComponent')
        renderComp.spriteFile = file
        renderComp.sceneNode.addSpriteImage(file, pos, rotation)
    
    def update(self):
        rand = random.randint(0, 3)
        if rand == 0:
            event = Event_ApplyImpulse(self.ball.actorID, Vec2d(0, 1), 25)
            ECOM.eventManager.queueEvent(event)
        elif rand == 1:
            event = Event_ApplyImpulse(self.ball.actorID, Vec2d(0, -1), 25)
            ECOM.eventManager.queueEvent(event)
        elif rand == 2:
            event = Event_ApplyImpulse(self.ball.actorID, Vec2d(1, 0), 25)
            ECOM.eventManager.queueEvent(event)
        elif rand == 3:
            event = Event_ApplyImpulse(self.ball.actorID, Vec2d(-1, 0), 25)
            ECOM.eventManager.queueEvent(event)


class BallAngry(BallState): #Goal: Angry at being hit. Supports whoever has hit it less. 
    def __init__(self, ball):
        super().__init__(ball)
        transformComp = self.ball.getComponent('TransformComponent')
        pos = transformComp.pos
        rotation = transformComp.rotation
        self.leftScore = ECOM.engine.baseLogic.leftScore
        self.rightScore = ECOM.engine.baseLogic.rightScore
        self.MAX_VELOCITY = 500
        self.MIN_VELOCITY = 150
        
        file = 'Images\PongBallAngry.png'
        renderComp = self.ball.getComponent('RenderComponent')
        renderComp.spriteFile = file
        renderComp.sceneNode.addSpriteImage(file, pos, rotation)
        
        ECOM.eventManager.addListener(self.handleGoal, Event_BallGoal.eventType)
    
    def update(self):
        physicsComp = self.ball.getComponent("PhysicsComponent")
        velocityMod = physicsComp.velocityMod
        velocity = physicsComp.physics.getVelocity(self.ball.actorID)
        
        #ball will favor left side           
        if self.leftScore < self.rightScore:
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
                
        #ball will favor right side
        elif self.rightScore < self.leftScore:
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
            
            
class BallBored(BallState): #Goal: Bored with game. Supports whoever is winning. 
    def __init__(self, ball):
        super().__init__(ball)
        transformComp = self.ball.getComponent('TransformComponent')
        pos = transformComp.pos
        rotation = transformComp.rotation
        self.leftScore = ECOM.engine.baseLogic.leftScore
        self.rightScore = ECOM.engine.baseLogic.rightScore
        self.MAX_VELOCITY = 500
        self.MIN_VELOCITY = 150
        
        file = 'Images\PongBallBored.png'
        renderComp = self.ball.getComponent('RenderComponent')
        renderComp.spriteFile = file
        renderComp.sceneNode.addSpriteImage(file, pos, rotation)
        
        ECOM.eventManager.addListener(self.handleGoal, Event_BallGoal.eventType)
    
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