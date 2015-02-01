'''
Created on Jul 31, 2013

@author: Devon
'''

from pyHopeEngine import BaseEvent

class Event_BallGoal(BaseEvent):
    eventType = "BallGoal"
    
    def __init__(self, leftScore, rightScore):
        self.leftScore = leftScore
        self.rightScore  = rightScore


class Event_BallCollide(BaseEvent):
    eventType = "BallCollide"
    
    def __init__(self, actorID1, actorID2):
        self.actorID1 = actorID1
        self.actorID2 = actorID2


class Event_RequestCurrentScore(BaseEvent):
    eventType = "RequestCurrentScore"
    
    def __init__(self, requestor):
        self.requestor = requestor
        

class Event_PaddleClicked(BaseEvent):
    eventType = "PaddleClicked"
    
    def __init__(self, paddleNum, playerNum):
        self.paddleNum = paddleNum
        self.playerNum = playerNum
        

class Event_AssignPaddle(BaseEvent):
    eventType = "AssignPaddle"
    
    def __init__(self, paddleNum, playerNum):
        self.paddleNum = paddleNum
        self.playerNum = playerNum


class Event_AssignPlayerID(BaseEvent):
    eventType = "AssignPlayerID"
    
    def __init__(self, playerID):
        self.playerID = playerID


class Event_RequestStartGame(BaseEvent):
    eventType = "RequestStartGame"
    
    def __init__(self):
        pass


class Event_StartGame(BaseEvent):
    eventType = "StartGame"
    
    def __init__(self, playerPaddles):
        self.playerPaddles = playerPaddles


class Event_GiveBallItem(BaseEvent):
    eventType = "GiveBallItem"
    
    def __init__(self, item):
        self.item = item


class Event_AddBall(BaseEvent):
    eventType = "AddBall"
    
    def __init__(self, emotion):
        self.emotion = emotion


class Event_DestroyExtraBall(BaseEvent):
    eventType = "DestroyExtraBall"
    
    def __init__(self, emotion):
        self.emotion = emotion
