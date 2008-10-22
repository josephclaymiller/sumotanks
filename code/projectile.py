import sys, math, world

from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject

class projectile(DirectObject):
    def __init__(self, mass, world, lenCannon, pitch, head, ptype=None):
        if ptype == 1:
            self.model = loader.loadModel("../art/tank/bullet.egg")
            self.model.setScale(1)
        else:
            self.model = loader.loadModel("../art/tank/bullet.egg")
            self.model.setScale(.4)
        self.model.reparentTo(render)
        
        self.world = world
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
            muzzvel = 10 #Change to change speed

        self.velx = (dirx * muzzvel)
        self.vely = (diry * muzzvel)
        self.velz = (dirz * muzzvel)

        self.ptype = ptype
        self.nodePath = self.addCollisionBoundaries()
        
    def addCollisionBoundaries(self):
        self.cHandler = CollisionHandlerEvent()
        self.cHandler.setInPattern("hit-%in")
        cSphere = CollisionSphere(0, 0, 0, 3)
        cNode = CollisionNode("Bullet")
        cNode.addSolid(cSphere)
        cNP = self.model.attachNewNode(cNode)
        #cNP.show()
        
        base.cTrav.addCollider(cNP, self.cHandler)
        
        self.accept("hit-Player", self.hitPlayer)
        self.accept("hit-Enemy", self.hitEnemy)
        
        return cNP

    def grav(self):
        self.velz -= .05 #Change to change affect of gravity
    
    def hitPlayer(self, entry):
        self.world.addDamage(1, 1)
    
    def hitEnemy(self, entry):
        self.world.addDamage(1, 0)
        
