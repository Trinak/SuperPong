'''
Created on Sep 7, 2013

@author: Devon
'''

from pyHopeEngine import engineCommon as ECOM
from pyHopeEngine import BaseDialog, BaseTable
from pyHopeEngine import Event_IPInput

class JoinGameDialog(BaseDialog):
    def __init__(self, title, **params):
        main = BaseTable()
        
        main.addLabel("Host Address:")
        self.input = main.addInput(size = 15)
        main.addButton("Join", self.joinButton)
        
        super().__init__(title, main, **params)
    
    def joinButton(self):
        inputValue = self.input.value
        if len(inputValue) > 15 or len(inputValue) < 7:
            return
        else:
            event = Event_IPInput(inputValue)
            ECOM.eventManager.queueEvent(event)


class InstructionsDialog(BaseDialog):
    def __init__(self, title, **params):
        main = BaseTable()
        
        text = ("The goal of EmotiPong is the same as regular pong, get the ball past your opponents paddle. "
                "Unlike regular pong, you can give the ball items. The items will influence the balls emotional state "
                "which may be beneficial for you or your opponent. Be careful though, if you and your opponent give items "
                "at the same time they may interact unexpectedly.")
        text = "{smallFont; {green;" + text + " }}"
        rect = (0, 0, 800, 100)
        main.addText(text, rect, 'center')
        main.tr()
        
        text = "{largeFont; {green; The States}"
        rect = (0, 0, 800, 50)
        main.addText(text, rect, 'center')
        
        
        super().__init__(title, main, **params)


class OptionsDialog(BaseDialog):
    def __init__(self, title, **params):
        main = BaseTable()
        
        self.select = main.addSelect()
        main.addButton("Apply", self.applyButton)
        super().__init__(title, main, **params)
    
    def applyButton(self):
        pass
        
        
        
        