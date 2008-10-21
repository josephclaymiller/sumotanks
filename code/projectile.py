import entity

import sys, math

from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject

class projectile(entity.entity):
    def __init__(self, mass, xv, yv, angle, pitch):
        self.model = loader.loadModel("../art/arena/arena1.egg")
        self.model.setScale(.02)
        self.model.reparentTo(render)
        self.mass = mass
        self.acc = entity.force(0,0)
        self.vel = entity.force(math.sqrt(math.pow(xv,2) + math.pow(yv,2)), angle)
        self.zv = 3*math.cos(pitch)

        
        
