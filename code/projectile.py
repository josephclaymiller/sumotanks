import sys, math

from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject

class projectile(DirectObject):
    def __init__(self, mass, lenCannon, pitch, head):
        self.model = loader.loadModel("../art/tank/bullet.egg")
        self.model.setScale(1)
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
        
        muzzvel = 4 #Change to change speed

        self.velx = (dirx * muzzvel)
        self.vely = (diry * muzzvel)
        self.velz = (dirz * muzzvel)
        print "XV: ", self.velx, " YV: ", self.vely, " ZV: ", self.velz

    def grav(self):
        self.velz -= 1 #Change to change affect of gravity
        
