import sys, math

from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject

class projectile(DirectObject):
    def __init__(self, mass, posCannon, lenCannon, pitch, head):
        self.model = loader.loadModel("../art/tank/bullet.egg")
        self.model.setScale(1)
        self.model.reparentTo(render)
        
        self.mass = mass
        
        proj = lenCannon * math.sin(pitch)
        tipx = proj * math.cos(head)
        tipy = proj * math.sin(head)
        tipz = lenCannon * math.cos(pitch)

        compx = (tipx + posCannon[0])
        compy = (tipy + posCannon[1])
        compz = (tipz + posCannon[2])

        dirx = (compx / lenCannon)
        diry = (compy / lenCannon)
        dirz = (compz / lenCannon)
        
        muzzvel = .1 #Change to change speed

        self.velx = (dirx * muzzvel)
        self.vely = (diry * muzzvel)
        self.velz = (dirz * muzzvel)

    def grav(self):
        self.velz -= .1 #Change to change affect of gravity
        
