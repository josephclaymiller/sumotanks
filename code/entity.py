#entity - a physics controlled object in the game world

import sys

from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject


class entity(DirectObject):
    def __init__( self, x, y, z, mass ):
        self.x = x
        self.y = y
        self.z = z
        self.mass = mass*.006

    def addForce(self, x, y, z):
        self.x += x
        self.y += y
        self.z += z

    def getSpeed(self):
        return (self.x/(self.mass+0.0), self.y/(self.mass+0.0), self.z/(self.mass+0.0))
