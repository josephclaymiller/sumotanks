import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import *
from direct.task import Task
import sys, math
import random
import world
     
class EnemyTank(DirectObject):  #use to create computer tank
    def __init__(self):
        
        self.enemyturret = Actor("panda-model", {"walk":"panda-walk4"})
        self.enemyturret.reparentTo(render)
        self.enemyturret.setScale(.005)
        self.enemyturret.setH(180)

        self.enemybase = Actor("panda-model", {"walk":"panda-walk4"})
        self.enemybase.reparentTo(render)
        self.enemybase.setScale(.005)
        self.enemybase.setH(180)

        self.enemybase.setPos(7,7,0)
        self.playerPos = [0,0,0]
        self.loweraimingoffset = -1
        self.upperaimingoffset = 1

    def setplayerPos(self,playerPosition):
        self.playerPos = playerPosition

    def moveenemyTurret(self,task): #used so enemy turret is aimed at the player
        #position = self.enemyturret.getPos()
        xposition = self.enemyturret.getX() #Used to get current coordinates of the turret
        yposition = self.enemyturret.getY()
        zposition = self.enemyturret.getZ()
        dx = self.playerPos[0]-xposition
        dy = self.playerPos[1]-yposition
        heading = rad2Deg(math.atan2(dy, dx))
        heading = heading+90
        headingoffset = random.randrange(self.loweraimingoffset,self.upperaimingoffset) #random offset for heading
        pitchoffset = random.randrange(self.loweraimingoffset,self.upperaimingoffset)   #random offset for pitch
        modifiedheading = heading+headingoffset  
        self.enemyturret.setHpr(modifiedheading,pitchoffset,0)
        self.enemyturret.setPos(self.enemybase.getX(),self.enemybase.getY(),self.enemybase.getZ()+2)
        return Task.cont        
