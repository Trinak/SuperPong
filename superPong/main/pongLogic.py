'''
Created on May 9, 2013

@author: Devon
'''

from pyHopeEngine import engineCommon as ECOM
from pyHopeEngine import BaseLogic
from pyHopeEngine import Event_ClientConnected, Event_Accelerate, Event_Decelerate, Event_ApplyImpulse
from superPong.actors.pongActorManager import PongActorManager
from superPong.events.pongEvents import (Event_BallGoal, Event_BallCollide, Event_RequestCurrentScore, Event_PaddleClicked, Event_AssignPaddle, 
                                         Event_AssignPlayerID, Event_RequestStartGame, Event_StartGame, Event_AddBall, Event_DestroyExtraBall)

class PongLogic(BaseLogic):
    def __init__(self):
        super().__init__()
        self.physics.setDamping(0.7)
        
        self.actorManager = PongActorManager()
        self.leftScore = 0
        self.rightScore = 0
        self.players = 0
        self.spotsSelected = [None, None]
        self.setupCollisionHandlers()
        
        ECOM.eventManager.addListener(self.accelerate, Event_Accelerate.eventType)
        ECOM.eventManager.addListener(self.decelerate, Event_Decelerate.eventType)
        ECOM.eventManager.addListener(self.applyImpulse, Event_ApplyImpulse.eventType)
        ECOM.eventManager.addListener(self.paddleClicked, Event_PaddleClicked.eventType)
        ECOM.eventManager.addListener(self.clientConnected, Event_ClientConnected.eventType)
        ECOM.eventManager.addListener(self.assignPlayerID, Event_AssignPlayerID.eventType)
        ECOM.eventManager.addListener(self.requestStartGame, Event_RequestStartGame.eventType)
        ECOM.eventManager.addListener(self.addBall, Event_AddBall.eventType)
        ECOM.eventManager.addListener(self.destroyExtraBall, Event_DestroyExtraBall.eventType)
        ECOM.eventManager.addListener(self.scoresRequested, Event_RequestCurrentScore.eventType)
        
    def setupCollisionHandlers(self):
        def ballGoalLeft(space, arbiter):
            self.rightScore += 1
            actorID1 = self.physics.getActorID(arbiter.shapes[0])
            actorID2 = self.physics.getActorID(arbiter.shapes[1])
            self.handleGoal(actorID1, actorID2)
            return True
        
        def ballGoalRight(space, arbiter):
            self.leftScore += 1
            actorID1 = self.physics.getActorID(arbiter.shapes[0])
            actorID2 = self.physics.getActorID(arbiter.shapes[1])
            self.handleGoal(actorID1, actorID2)
            return True
        
        def ballCollide(space, arbiter):
            actorID1 = self.physics.getActorID(arbiter.shapes[0])
            actorID2 = self.physics.getActorID(arbiter.shapes[1])
            event = Event_BallCollide(actorID1, actorID2)
            ECOM.eventManager.queueEvent(event)
            return True
        
        self.physics.addCollisionHandler(3, 2, begin = ballGoalLeft)
        self.physics.addCollisionHandler(3, 1, begin = ballGoalRight)
        self.physics.addCollisionHandler(3, 0, begin = ballCollide)
    
    def createActor(self, resource, actorType = None, actorID = None):
        actor = super().createActor(resource, actorID = actorID)
        
        if actorType == "Player":
            self.actorManager.addPlayer(actor)
        elif actorType == "Enemy":
            self.actorManager.addEnemy(actor)
        elif actorType == "Ball":
            self.actorManager.addBall(actor)
        
        return actor
    
    def paddleClicked(self, event):
        if not self.proxy:
            if self.spotsSelected[event.paddleNum] is None and event.playerNum not in self.spotsSelected:
                self.spotsSelected[event.paddleNum] = event.playerNum
                event = Event_AssignPaddle(event.paddleNum, event.playerNum)
                ECOM.eventManager.queueEvent(event)
            elif self.spotsSelected[event.paddleNum] == event.playerNum:
                self.spotsSelected[event.paddleNum] = None
                event = Event_AssignPaddle(event.paddleNum, event.playerNum)
                ECOM.eventManager.queueEvent(event)  
        
    def createNetworkEventForwarder(self):
        super().createNetworkEventForwarder()
        
        eMan = ECOM.eventManager
        if not self.proxy:
            eMan.addListener(self.networkEventForwarder.forwardEvent, Event_BallGoal.eventType)
            eMan.addListener(self.networkEventForwarder.forwardEvent, Event_BallCollide.eventType)
            eMan.addListener(self.networkEventForwarder.forwardEvent, Event_AssignPlayerID.eventType)
            eMan.addListener(self.networkEventForwarder.forwardEvent, Event_AssignPaddle.eventType)
            eMan.addListener(self.networkEventForwarder.forwardEvent, Event_StartGame.eventType)
        else:
            eMan.addListener(self.networkEventForwarder.forwardEvent, Event_PaddleClicked.eventType)
    
    def addBall(self, event):
        ball = self.createActor("Actors\AI\PongBallAdd.xml", "Ball")
        ballAI = ball.getComponent("AIComponent")
        ballAI.setState(event.emotion)
    
    def destroyExtraBall(self, event):
        self.actorManager.destroyBall(emotion = event.emotion)
    
    def accelerate(self, event):
        actor = self.actorManager.getActor(event.actorID)
        physicsComp = actor.getComponent("PhysicsComponent")
        physicsComp.applyAcceleration(event.magnitude) 
    
    def decelerate(self, event):
        actor = self.actorManager.getActor(event.actorID)
        physicsComp = actor.getComponent("PhysicsComponent")
        physicsComp.removeAcceleration()
    
    def applyImpulse(self, event):
        actor = self.actorManager.getActor(event.actorID)
        physicsComp = actor.getComponent("PhysicsComponent")
        physicsComp.applyImpulse(event.direction, event.magnitude)
    
    def clientConnected(self, event):
        self.players += 1
        event = Event_AssignPlayerID(self.players)
        ECOM.eventManager.queueEvent(event)
     
    def assignPlayerID(self, event):
        if not self.proxy:
            return
        
        for view in self.gameViewList:
            if view.type == "PongChooseSidesView":
                view.playerID = event.playerID
    
    def requestStartGame(self, event):
        if not self.proxy:
            if None not in self.spotsSelected:
                event = Event_StartGame(self.spotsSelected)
                ECOM.eventManager.queueEvent(event)
    
    def handleGoal(self,actorID1, actorID2):
        event = Event_BallGoal(self.leftScore, self.rightScore)
        ECOM.eventManager.queueEvent(event)
        if not self.actorManager.ballWasRemoved(actorID1, actorID2):
            self.actorManager.restartBall()
    
    def scoresRequested(self, event):
        event.requestor.setScores(self.leftScore, self.rightScore)
    
    def restartGame(self):
        for view in self.gameViewList:
            view.cleanUp()
        self.gameViewList.clear()
        self.actorManager.cleanUp()
        self.physics.cleanUp()
        self.processManager.cleanUp()
        self.leftScore = 0
        self.rightScore = 0
            
        