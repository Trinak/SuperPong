'''
Created on Jul 3, 2013

@author: Devon
'''

from pyHopeEngine import engineCommon as ECOM
from pyHopeEngine import BaseUI
from pyHopeEngine import Event_ButtonPressed
from superPong.events.pongEvents import Event_PaddleClicked, Event_AssignPaddle, Event_RequestStartGame
from superPong.humanView import pongWidgets

from pgu import gui


Screen = ECOM.Screen

class PongMainMenuUI(BaseUI):
    def __init__(self, area, **params):
        super().__init__(**params)
        
        self.widget.addButton("One Player", self.onePlayerButton)
        self.widget.tr()
        
        self.widget.addButton("Create Game", self.createLANButton)
        self.widget.tr()
        
        self.widget.addButton("Join Game", self.joinGameButton)
        self.widget.tr()
        
        self.widget.addButton("Options", self.optionsButton)
        
        self.init(area = area)
    
    def onePlayerButton(self):
        event = Event_ButtonPressed("OnePlayer")
        ECOM.eventManager.queueEvent(event)

    def createLANButton(self):
        event = Event_ButtonPressed("CreateGame")
        ECOM.eventManager.queueEvent(event)
    
    def joinGameButton(self):
        dialog = pongWidgets.JoinGameDialog("Join Game")
        event = Event_ButtonPressed("JoinGame")
        ECOM.eventManager.queueEvent(event)
        dialog.open()

    def optionsButton(self):
        dialog = pongWidgets.OptionsDialog("Options")
        dialog.open()


class PongChooseSidesUI(BaseUI):
    def __init__(self, area, **params):
        super().__init__(**params)
        self.playerAssigned = [None, None]
        self.isFadeImage =[True, True]
        self.fadeImages = ["Images\PaddleOneFade.png",
                           "Images\PaddleTwoFade.png"]
        
        self.normImages = ["Images\PaddleOne.png",
                           "Images\PaddleTwo.png"]
        
        self.createUI()
        self.init(area = area)
        
        ECOM.eventManager.addListener(self.redrawPaddles, Event_AssignPaddle.eventType)
    
    def createUI(self):
        text = '{defaultFont; {green; Choose Sides}}'
        rect = (0, 0, 140, 100)
        self.widget.addText(text, rect)
        self.widget.tr()
        
        self.widget.addSpacer(50, 50)
        self.widget.tr()
        
        for i in range(0, len(self.isFadeImage)):
            if self.isFadeImage[i]:
                widget = self.widget.addImage(self.fadeImages[i])
                self.widget.connectEvent(widget, gui.CLICK, self.paddleClicked, i)
            else:
                widget = self.widget.addImage(self.normImages[i])
                self.widget.connectEvent(widget, gui.CLICK, self.paddleClicked, i)
        
        self.widget.tr()
        rect = (0,0, 50,50)
        for player in self.playerAssigned:
            if player is not None:
                text = "{defaultFont; {green; " + str(player) + "}}"
                self.widget.addText(text, rect)
            else:
                self.widget.addSpacer(50, 50)
        
        self.widget.tr()
        self.widget.addSpacer(100, 100)
        self.widget.tr()
        self.widget.addButton("Start Game", self.startGame)
    
    def clearPaddles(self):
        self.widget.clear()
    
    def paddleClicked(self, num):
        event = Event_PaddleClicked(num, self.owner.playerID)
        ECOM.eventManager.queueEvent(event)
    
    def redrawPaddles(self, event):
        self.clearPaddles()
        self.isFadeImage[event.paddleNum] = not self.isFadeImage[event.paddleNum]
        if self.playerAssigned[event.paddleNum] is None:
            self.playerAssigned[event.paddleNum] = event.playerNum
        else:
            self.playerAssigned[event.paddleNum] = None
        self.createUI()
        self.resize()
    
    def startGame(self):
        event = Event_RequestStartGame()
        ECOM.eventManager.queueEvent(event)
        
        
class PongUI(BaseUI):
    def __init__(self, area, **params):
        super().__init__(**params)
        self.textRect = (0, 0, 175, 30)
        self.createTopUI(0, 0)
        self.init(area = area)
    
    def createTopUI(self, leftScore, rightScore):
        leftText = '{defaultFont; {green; Left Score: ' + str(leftScore) + '}}' 
        rightText = '{defaultFont; {green; Right Score: ' + str(rightScore) + '}}'
        
        self.widget.addButton("Images\Chocolate.png", self.test, True)
        self.widget.addImage("Images\Antidepressant.png")
        self.widget.addImage("Images\HistoryBook.png")
        self.widget.addImage("Images\MeanNote.png")
        self.widget.addImage("Images\PsychoPill.png")
        self.widget.addImage("Images\SadPicture.png")
        self.widget.addImage("Images\WinningTicket.png")
        self.widget.addText(leftText, self.textRect)
        self.widget.addText(rightText, self.textRect, 'right')
        
    def updateScore(self, left, right):
        self.widget.remove_row(0)
        self.createTopUI(left, right)
    
    def test(self):
        pass
        
        