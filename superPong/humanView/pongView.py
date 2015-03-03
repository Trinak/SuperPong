'''
Created on Jun 17, 2013

@author: Devon
'''

from pyHopeEngine import engineCommon as ECOM
from pyHopeEngine import HumanView
from pyHopeEngine import Event_SetControlledActor, Event_ButtonPressed
from superPong.humanView.pongUI import PongMainMenuUI, PongChooseSidesUI, PongUI
from superPong.humanView.pongController import PaddleOneController, PaddleTwoController
from superPong.events.pongEvents import Event_BallGoal, Event_BallCollide

Screen = ECOM.Screen

class MainMenuView(HumanView):
    def __init__(self, renderer):
        super().__init__(renderer)
        self.type = "MainMenuView"
        self.setBackground("Images\TitleScreen.png")
        
        rectUI = (0, 0, Screen.windowWidth, Screen.windowHeight)
        vpad = 5
        self.UI = PongMainMenuUI(rectUI, vpadding = vpad)
        self.addScreenElement(self.UI)
        self.audio.addSound("Sounds/button.wav", "button")
        ECOM.eventManager.addListener(self.buttonPressed, Event_ButtonPressed.eventType)
    
    def onPygameEvent(self, event):
        self.UI.onPygameEvent(event)


    def buttonPressed(self, event):
        self.audio.playSound("button")


class PongChooseSidesView(HumanView):
    def __init__(self):
        super().__init__(None)
        self.type = "PongChooseSidesView"
        rectUI = (0, 0, Screen.windowWidth, Screen.windowHeight)
        self.UI = PongChooseSidesUI(rectUI, valign = -1)
        self.UI.owner = self
        self.addScreenElement(self.UI)
        self.playerID = None
    
    
    def onPygameEvent(self, event):
        self.UI.onPygameEvent(event)
        

class PongHumanView(HumanView):
    def __init__(self, renderer):
        super().__init__(renderer)
        self.type = "PongHumanView"
        rectUI = (0, 0, Screen.windowWidth, 30)
        self.UI = PongUI(rectUI)
        self.addScreenElement(self.scene) 
        self.addScreenElement(self.UI)
        
        self.audio.addSound("Sounds/goal.wav", "goal")
        self.audio.addSound("Sounds/ballCollide.ogg", "collide")
        
        eventManager = ECOM.eventManager
        eventManager.addListener(self.updateScore, Event_BallGoal.eventType)
        eventManager.addListener(self.ballCollide, Event_BallCollide.eventType)
        eventManager.addListener(self.setActor, Event_SetControlledActor.eventType)
    
    def onPygameEvent(self, event):
        handled = super().onPygameEvent(event)
        if not handled:
            self.UI.onPygameEvent(event)    
    
    def setControlledActor(self, actorID):
        super().setControlledActor(actorID)
        self.paddleController = PaddleOneController()
        self.paddleController.setControlledActor(self.controlledActor)
        self.keyboardHandler = self.paddleController
    
    
    def setActor(self, event):
        self.setControlledActor(event.actorID)
        
       
    def updateScore(self, event):
        self.UI.updateScore(event.leftScore, event.rightScore)
        self.audio.playSound("goal")
    
    
    def ballCollide(self, event):
        self.audio.playSound("collide") 