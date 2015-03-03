'''
Created on Jul 3, 2013

@author: Devon
'''

from pyHopeEngine import engineCommon as ECOM
from pyHopeEngine import BaseUI
from pyHopeEngine import Event_ButtonPressed
from superPong.humanView import pongWidgets
from superPong.actors.items.items import *
from superPong.humanView.disableGiveItemProcess import DisableGiveItemProcess
from superPong.events.pongEvents import Event_PaddleClicked, Event_AssignPaddle, Event_RequestStartGame, Event_GiveBallItem


from pgu import gui
from faulthandler import disable


Screen = ECOM.Screen

class PongMainMenuUI(BaseUI):
    def __init__(self, area, **params):
        super().__init__(**params)
        
        self.widget.addButton("One Player", self.onePlayerButton)
        self.widget.tr()
        
        #self.widget.addButton("Create Game", self.createLANButton)
        #self.widget.tr()
        
        #self.widget.addButton("Join Game", self.joinGameButton)
        #self.widget.tr()
        
        self.widget.addButton("Instructions", self.instructionButton)
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

    def instructionButton(self):
        dialog = pongWidgets.InstructionsDialog("Instructions")
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
        text = "Choose Sides"
        rect = (0, 0, 140, 100)
        self.widget.addText(text, rect, color = 'green')
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
                text = str(player)
                self.widget.addText(text, rect, color = "green")
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
        self.disabledImagesPlayer = False
        self.disabledImagesEnemy = False        
        self.playerItemGiven = None
        self.opponentItemGiven = None
        self.leftScore = 0
        self.rightScore = 0
        self.scoreRect = (0, 0, 175, 30)
        self.createTopUI()
        self.init(area = area)

        ECOM.eventManager.addListener(self.handleItemGiven, Event_GiveBallItem.eventType)
    
    def createTopUI(self):
        leftText = "Left Score: " + str(self.leftScore)
        rightText = "Right Score: " + str(self.rightScore)

        if self.disabledImagesPlayer:
            self.createItemImages(True, True)
        else:
            self.createItemButtons()
        
        self.widget.addSpacer(10, 10)
        self.widget.addText(leftText, self.scoreRect, color = "green")
        self.widget.addText(rightText, self.scoreRect, 'right', color = "green")
        self.widget.addSpacer(10, 10)

        self.createItemImages(self.disabledImagesEnemy, False)
        self.widget.tr();
        
    def createItemButtons(self):
        self.widget.addButton("Images\Chocolate.png", self.giveChocolate, True)
        self.widget.addSpacer(10, 10)
        self.widget.addButton("Images\HistoryBook.png", self.giveHistoryBook, True)
        self.widget.addSpacer(10, 10)
        self.widget.addButton("Images\MeanNote.png", self.giveMeanNote, True)
        self.widget.addSpacer(10, 10)
        self.widget.addButton("Images\PsychoPill.png", self.givePsychoPill, True)
        self.widget.addSpacer(10, 10)
        self.widget.addButton("Images\SadPicture.png", self.giveSadPicture, True)
        self.widget.addSpacer(10, 10)
        self.widget.addButton("Images\WinningTicket.png", self.giveWinningTicket, True)
        
    def createItemImages(self, isDisabled, isPlayerOne):
        endText = ".png"
        
        if isDisabled:
            endText = "Disabled.png"
        
        if isPlayerOne:
            itemName = self.playerItemGiven
        else:
            itemName = self.opponentItemGiven

        if itemName == "Chocolate":
            self.widget.addImage("Images\ChocolateChosen.png")
        else:
            self.widget.addImage("Images\Chocolate" + endText)
            
        self.widget.addSpacer(30, 10)
        if itemName == "HistoryBook":
            self.widget.addImage("Images\HistoryBookChosen.png")
        else:
            self.widget.addImage("Images\HistoryBook" + endText)
        
        self.widget.addSpacer(30, 10)
        if itemName == "MeanNote":
            self.widget.addImage("Images\MeanNoteChosen.png")
        else:
            self.widget.addImage("Images\MeanNote" + endText)
        
        self.widget.addSpacer(30, 10)
        if itemName == "PsychoPill":
            self.widget.addImage("Images\PsychoPillChosen.png")
        else:
            self.widget.addImage("Images\PsychoPill" + endText)
        
        self.widget.addSpacer(30, 10)
        if itemName == "SadPicture":
            self.widget.addImage("Images\SadPictureChosen.png")
        else:
            self.widget.addImage("Images\SadPicture" + endText)
        self.widget.addSpacer(30, 10)
        if itemName == "WinningTicket":
            self.widget.addImage("Images\WinningTicketChosen.png")
        else:
            self.widget.addImage("Images\WinningTicket" + endText)
    
    def updateScore(self, left, right):
        self.leftScore = left
        self.rightScore = right
        self.widget.remove_row(0)
        self.createTopUI()
    
    def handleItemGiven(self, event):
        if event.isPlayerOne:
            self.playerItemGiven = event.item.name
            self.disabledImagesPlayer = True
            process = DisableGiveItemProcess(self, True)
        else:
            self.opponentItemGiven = event.item.name
            self.disabledImagesEnemy = True
            process = DisableGiveItemProcess(self, False)
        
        ECOM.engine.baseLogic.processManager.addProcess(process)
    
    def giveChocolate(self):
        event = Event_GiveBallItem(Chocolate())
        ECOM.eventManager.queueEvent(event)
    
    def giveHistoryBook(self):
        event = Event_GiveBallItem(HistoryBook())
        ECOM.eventManager.queueEvent(event)
    
    def giveMeanNote(self):
        event = Event_GiveBallItem(MeanNote())
        ECOM.eventManager.queueEvent(event)
    
    def givePsychoPill(self):
        event = Event_GiveBallItem(PsychoPill())
        ECOM.eventManager.queueEvent(event)
    
    def giveSadPicture(self):
        event = Event_GiveBallItem(SadPicture())
        ECOM.eventManager.queueEvent(event)
        
    def giveWinningTicket(self):
        event = Event_GiveBallItem(WinningTicket())
        ECOM.eventManager.queueEvent(event)