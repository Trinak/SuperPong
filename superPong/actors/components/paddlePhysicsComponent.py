'''
Created on Oct 30, 2014

@author: Arrington
'''

from pyHopeEngine.actors.components.physicsComponent import PhysicsComponent

class PaddlePhysicsComponent(PhysicsComponent):
    def __init__(self):
        super().__init__()
        self.grooveJoint = {}
        
    def init(self, element):
        super().init(element)
    
    def setProperties(self, element):
        super().setProperties(element)
        
        element = element.find("GrooveJoint")
        self.grooveJoint['groove_a'] = self.findProperty(element, "GrooveA", (0, 0))
        self.grooveJoint['groove_b'] = self.findProperty(element, "GrooveB", (0, 0))
        self.grooveJoint['anchr2'] = self.findProperty(element, "Anchr2", (0, 0))
    
    def postInit(self):
        super().postInit()
        
        self.physics.addConstraint("GrooveJoint", None, self.owner.actorID, **self.grooveJoint)