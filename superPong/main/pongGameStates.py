'''
Created on Jul 16, 2013

@author: Devon
'''

from pyHopeEngine import engineCommon as ECOM
from pyHopeEngine import BaseState
from pyHopeEngine import Event_ButtonPressed, Event_IPValid, Event_SetRemoteActor
from superPong.humanView import pongView
from superPong.events.pongEvents import Event_StartGame

Screen = ECOM.Screen

class MainMenuState(BaseState):
    def __init__(self):
        ECOM.eventManager.addListener(self.buttonPressed, Event_ButtonPressed.eventType)
        ECOM.eventManager.addListener(self.isValidServerIP, Event_IPValid.eventType)
        self.isNetworkGame = False
        self.netType = None
        self.connected = False
        self.nextState = False
    
    def init(self, logic):
        if not logic.gameViewList:
            view = pongView.MainMenuView(ECOM.engine.renderer)
            logic.addView(view)
    
    
    def cleanUp(self, logic):
        logic.gameViewList.pop()
    
    
    def update(self, logic):
        if self.nextState:
            if self.isNetworkGame:
                state = PongChooseSidesState(self.netType)
                logic.changeState(state)
            else:
                state = PongSetupState(2)
                logic.changeState(state)
    
    
    def buttonPressed(self, event):
        if event.value == "OnePlayer":
            self.nextState = True
        elif event.value == "CreateGame":
            self.nextState = True
            self.isNetworkGame = True
            self.netType = "server"
            ECOM.engine.setupServer()
        elif event.value == "JoinGame":
            ECOM.engine.setupClient()


    def isValidServerIP(self, event):
        if event.isValid:
            if ECOM.engine.networkManager.connect():
                self.nextState = True
                self.isNetworkGame = True
                self.netType = "client"


class PongChooseSidesState(BaseState):
    def __init__(self, netType):
        self.numPlayers = 2
        self.netType = netType
        self.ready = False
        
        ECOM.eventManager.addListener(self.startGame, Event_StartGame.eventType)
        
    
    def init(self, logic):
        if self.netType == "client":
            logic.setProxy()
        
        logic.createNetworkEventForwarder()
        view = pongView.PongChooseSidesView()
        if self.netType == "server":
            view.playerID = 1
            logic.players = 1
        logic.addView(view)

    
    def update(self, logic):
        if self.ready:
            state = PongSetupState(self.numPlayers, True, self.playerPaddles)
            logic.changeState(state)
        
    
    def startGame(self, event):
        self.playerPaddles = event.playerPaddles
        self.ready = True
    
    
    def cleanUp(self, logic):
        logic.gameViewList.pop()


class PongSetupState(BaseState):
    def __init__(self, players, isNetworkGame = False, playerPaddles = None):
        self.numPlayers = players
        self.isNetworkGame = isNetworkGame
        self.ready = False
        if playerPaddles is not None:
            self.playerOne = playerPaddles.index(1) + 1
            self.playerTwo = playerPaddles.index(2) + 1
            
    
    def init(self, logic):
        resources = []
        resources.append("Actors\AI\PongBall.xml")              #0
        resources.append("Actors\Players\PaddleOnePlayer.xml")  #1
        resources.append("Actors\Players\PaddleTwoPlayer.xml")  #2
        resources.append("Actors\Walls\TopWall.xml")            #3
        resources.append("Actors\Walls\RightWall.xml")          #4
        resources.append("Actors\Walls\BottomWall.xml")         #5 
        resources.append("Actors\Walls\LeftWall.xml")           #6
        resources.append("Actors\AI\PaddleOneAI.xml")           #7
        resources.append("Actors\AI\PaddleTwoAI.xml")           #8
        
        humanView = pongView.PongHumanView(ECOM.engine.renderer)
        logic.addView(humanView)
        
        if not logic.proxy:
            logic.createActor(resources[0], "Ball")
            
            for i in range(3, 7):
                logic.createActor(resources[i])
        
        if self.isNetworkGame:
            self.initNetworkGame(logic, resources)
        else:
            self.initGame(logic, resources)
            
        self.ready = True
    
    
    def initNetworkGame(self, logic, resources):
        if logic.proxy:
            return
        
        logic.createActor(resources[self.playerOne], "Player")
        playerTwo = logic.createActor(resources[self.playerTwo], "Enemy")

        event = Event_SetRemoteActor(playerTwo.actorID)
        ECOM.eventManager.queueEvent(event)
        
    
    def initGame(self, logic, resources):
        logic.createActor(resources[1], "Player")
        logic.createActor(resources[8], "Enemy")

    
    def update(self, logic):
        if self.ready:
            state = PongRunningState(self.numPlayers)
            logic.changeState(state)
    
    
    def cleanUp(self, logic):
        pass
    

class PongRunningState(BaseState):
    def __init__(self, players):
        self.numPlayers = players
    
    
    def init(self, logic):
        pass
        
    
    def update(self, logic):
        if logic.leftScore > 4 or logic.rightScore > 4:
            state = MainMenuState()
            logic.changeState(state)
    
    
    def cleanUp(self, logic):
        for view in logic.gameViewList:
            view.cleanUp()
        logic.gameViewList.clear()
        logic.actorManager.cleanUp()
        logic.leftScore = 0
        logic.rightScore = 0



        
        
        