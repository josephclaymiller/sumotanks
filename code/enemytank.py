import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import *
from direct.task import Task
import entity
import sys, math
import random
import world
     
class EnemyTank(entity.entity):  #use to create computer tank
    def __init__(self, world):
        self.cannon = Actor("cannongreen.egg")
        self.cannon.setScale(.75)
        self.cannon.reparentTo(render)
        self.turret = Actor("turretgreen.egg")
        self.turret.setScale(.75)
        self.turret.reparentTo(render)
        
        self.base = Actor("basegreen.egg", {"moveforwards":"forwards.egg","movebackwards":"backwards.egg", "turnleft":"left.egg","turnright":"right.egg"})
        self.base.setScale(.75)        
        self.base.reparentTo(render)
        
        entity.entity.__init__(self, 5)
        self.base.setName("enemy")
        self.base.setPos(7,7,0)
        self.playerPos = [0,0,0]
        self.loweraimingoffset = -1
        self.upperaimingoffset = 1

        self.damage = 1
        
        self.world = world
        self.nodePath = self.addCollisionBoundaries()

    def setenemyTexture(self,key):
        basepos = self.base.getPos()
        basehpr = self.base.getHpr()
        turrethpr = self.turret.getHpr()
        cannonhpr = self.cannon.getHpr()
        self.base.delete()
        self.turret.delete()
        self.cannon.delete()
        if key == 4: #Blue 
            self.base = Actor("baseblue.egg", {"moveforwards":"forwards.egg","movebackwards":"backwards.egg", "turnleft":"left.egg","turnright":"right.egg"})
            self.turret = Actor("turretblue.egg")
            self.cannon = Actor("cannonblue.egg")
        if key == 5: #Purple 
            self.base = Actor("basepurple.egg", {"moveforwards":"forwards.egg","movebackwards":"backwards.egg", "turnleft":"left.egg","turnright":"right.egg"})
            self.turret = Actor("turretpurple.egg")
            self.cannon = Actor("cannonpurple.egg")
        if key == 6: #Green
            self.base = Actor("basegreen.egg", {"moveforwards":"forwards.egg","movebackwards":"backwards.egg", "turnleft":"left.egg","turnright":"right.egg"})
            self.turret = Actor("turretgreen.egg")
            self.cannon = Actor("cannongreen.egg")
        if key == 7: #Yellow
            self.base = Actor("baseyellow.egg", {"moveforwards":"forwards.egg","movebackwards":"backwards.egg", "turnleft":"left.egg","turnright":"right.egg"})
            self.turret = Actor("turretyellow.egg")
            self.cannon = Actor("cannonyellow.egg")
        if key == 8: #Red
            self.base = Actor("basered.egg", {"moveforwards":"forwards.egg","movebackwards":"backwards.egg", "turnleft":"left.egg","turnright":"right.egg"})
            self.turret = Actor("turretred.egg")
            self.cannon = Actor("cannonred.egg")
        self.base.setScale(.75)        
        self.base.reparentTo(render)
        self.base.setPosHpr(basepos,basehpr)
        self.turret.setScale(.75)
        self.turret.reparentTo(render)
        self.turret.setHpr(turrethpr)
        self.cannon.setScale(.75)
        self.cannon.reparentTo(render)
        self.cannon.setHpr(cannonhpr)
        self.nodePath = self.addCollisionBoundaries()
        
    def addCollisionBoundaries(self):
        self.cHandler = CollisionHandlerEvent()
        self.cHandler.setInPattern("hit-%in")
        cSphere = CollisionSphere(0, 0, 0, 3)
        cNode = CollisionNode("Enemy")
        cNode.addSolid(cSphere)
        cNP = self.base.attachNewNode(cNode)
        #cNP.show()
        
        base.cTrav.addCollider(cNP, self.cHandler)
        
        self.accept("hit-Player", self.world.enemyHitPlayer)
        
        return cNP
    
    def setplayerPos(self,playerPosition):
        self.playerPos = playerPosition

    def moveEnemy(self,task):
        """Move enemy base and then the turret"""
        self.update()
        self.base.setPos(self.base.getX() + self.vel.xcomp(), self.base.getY() + self.vel.ycomp(), 0)

        #Put code to move base here:
        self.base.setH(self.base.getH()+1)

        self.moveenemyTurret() #Move enemy turret (to keep the code separate, but still update both in the same frame
        return Task.cont
        
    def moveenemyTurret(self): #used so enemy turret is aimed at the player
        xposition = self.turret.getX() #Used to get current coordinates of the turret
        yposition = self.turret.getY()
        zposition = self.turret.getZ()
        dx = self.playerPos[0]-xposition
        dy = self.playerPos[1]-yposition
        heading = rad2Deg(math.atan2(dy, dx))
        heading = heading+90

        dz = self.playerPos[2]-zposition #distance in height

        xvalues = (self.playerPos[0]-xposition)  #Distance formula
        yvalues = (self.playerPos[1]-yposition)
        xsquared = math.pow(xvalues,2)
        ysquared = math.pow(yvalues,2)
        distance = math.sqrt(xsquared+ysquared)
       
        pitch = rad2Deg(math.atan2(dz,distance)) 
        pitch *=-1
        if pitch < -20: #Limit how high up and down the turret can aim
            pitch = -20
        if pitch > 0:
            pitch = 0
        
        headingoffset = random.randrange(self.loweraimingoffset,self.upperaimingoffset) #random offset for heading
        pitchoffset = random.randrange(self.loweraimingoffset,self.upperaimingoffset)   #random offset for pitch
        modifiedheading = heading+headingoffset
        modifiedpitch = pitch+pitchoffset

        #self.cannon.setPos(self.base.getX(),self.base.getY(),self.base.getZ())
        self.cannon.setHpr(modifiedheading,modifiedpitch,0)
        self.turret.setHpr(modifiedheading-headingoffset,0,0)
        self.turret.setPos(self.base.getX(),self.base.getY(),self.base.getZ())

        dist = self.cannon.getP()*-1 #When the cannon pitches upwards it moves backwards a bit...this fixes it...but I have no idea why it works
        angle = deg2Rad(self.cannon.getH())
        dx = dist * math.sin(angle) #Calculate change in x direction
        dy = dist * -math.cos(angle)#Calculate change in y direction   
        dx = dx/40
        dy = dy/40
        self.cannon.setPos(self.base.getX()+dx,self.base.getY()+dy,self.base.getZ())
        

	def shootatPlayer(self):
		pass;
