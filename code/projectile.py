import sys, math

from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject

class projectile(DirectObject):
    def __init__(self, mass, lenCannon, pitch, head, ptype=None):
        if ptype == 1:
            self.model = loader.loadModel("../art/tank/bullet.egg")
            self.model.setScale(1)
        else:
            self.model = loader.loadModel("../art/tank/bullet.egg")
            self.model.setScale(.4)
        self.model.reparentTo(render)
        
        self.mass = mass
        
        proj = lenCannon * math.sin(pitch)
        tipx = proj * math.cos(head)
        tipy = proj * math.sin(head)
        tipz = lenCannon * math.cos(pitch)

        compx = (tipx - 0)
        compy = (tipy - 0)
        compz = (tipz - 0)

        dirx = (compx / lenCannon)
        diry = (compy / lenCannon)
        dirz = (compz / lenCannon)
        if ptype == 1: 
            muzzvel = 2 #Change to change speed
        else:
            muzzvel = 6 #Change to change speed

        self.velx = (dirx * muzzvel)
        self.vely = (diry * muzzvel)
        self.velz = (dirz * muzzvel)

    def grav(self):
        self.velz -= .05 #Change to change affect of gravity
        
