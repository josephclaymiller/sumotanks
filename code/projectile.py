import sys, math, world, random

from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject

class projectile(DirectObject):
    def __init__(self, mass, shooter, lenCannon, pitch, head, ptype=None):
        if ptype == 1:
            self.model = loader.loadModel("../art/tank/bullet.egg")
            self.model.setScale(1)
        else:
            self.model = loader.loadModel("../art/tank/bullet.egg")
            self.model.setScale(.4)
        self.model.reparentTo(render)
        
        self.shooter = shooter
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
            muzzvel = 7 #Change to change speed
        else:
            muzzvel = 10 #Change to change speed

        self.velx = (dirx * muzzvel)
        self.vely = (diry * muzzvel)
        self.velz = (dirz * muzzvel)

        self.ptype = ptype
        self.nodePath = self.addCollisionBoundaries()

        self.hasHit = False
        
    def addCollisionBoundaries(self):
        self.cHandler = CollisionHandlerEvent()
        self.cHandler.setInPattern("hit-%in")
        cSphere = CollisionSphere(0, 0, 0, 3)
        if self.ptype == 1:
            cNode = CollisionNode("Cannon")
        else:
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
        if self.hasHit:
            return
        self.hasHit = True
        if self.ptype == 1:
            self.shooter.world.addDamage(100, 1)
            self.shooter.world.soundqueue.enqueue('boom', self.shooter.world.player.base.getX(),self.shooter.world.player.base.getY(),self.shooter.world.player.base.getZ())
            if self.shooter.world.player.vel.magnitude >= 0:
                self.shooter.world.player.vel.magnitude -= .01*self.shooter.world.computer.damage
                if self.shooter.world.player.vel.magnitude < -7:
                    self.shooter.world.player.vel.magnitude = -7 
            else:
                self.shooter.world.player.vel.magnitude += .01*self.shooter.world.computer.damage
                if self.shooter.world.player.vel.magnitude > 7:
                    self.shooter.world.player.vel.magnitude = 7 
        else:
            self.shooter.world.addDamage(1, 1)
            self.shooter.world.soundqueue.enqueue('hit' + str(random.randint(1, 3)), self.shooter.world.player.base.getX(),self.shooter.world.player.base.getY(),self.shooter.world.player.base.getZ())
        base.cTrav.removeCollider(self.nodePath)
        for i in range(len(self.shooter.projectiles)):
            if self.shooter.projectiles[i] == self:
                self.shooter.projectiles[i].model.removeNode()
                del self.shooter.projectiles[i]
                break
        
    def hitEnemy(self, entry):
        if self.hasHit:
            return
        self.hasHit = True
        if self.ptype == 1:
            self.shooter.world.addDamage(100, 0)
            self.shooter.world.soundqueue.enqueue('boom', self.shooter.world.computer.base.getX(),self.shooter.world.computer.base.getY(),self.shooter.world.computer.base.getZ())
            if self.shooter.world.computer.vel.magnitude >= 0:
                self.shooter.world.computer.vel.magnitude -= .02*self.shooter.world.player.damage
                if self.shooter.world.computer.vel.magnitude < -7:
                    self.shooter.world.computer.vel.magnitude = -7 
            else:
                self.shooter.world.computer.vel.magnitude += .02*self.shooter.world.player.damage
                if self.shooter.world.computer.vel.magnitude > 7:
                    self.shooter.world.computer.vel.magnitude = 7 
        else:
            self.shooter.world.addDamage(1, 0)
            self.shooter.world.soundqueue.enqueue('hit' + str(random.randint(1, 3)), self.shooter.world.computer.base.getX(),self.shooter.world.computer.base.getY(),self.shooter.world.computer.base.getZ())
        base.cTrav.removeCollider(self.nodePath)
        for i in range(len(self.shooter.projectiles)):
            if self.shooter.projectiles[i] == self:
                self.shooter.projectiles[i].model.removeNode()
                del self.shooter.projectiles[i]     
                break
