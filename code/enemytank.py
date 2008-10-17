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
        

        self.enemycannon = Actor("cannon.egg")
        self.enemycannon.reparentTo(render)
        self.enemyturret = Actor("turret.egg")
        self.enemyturret.reparentTo(render)
        #self.enemyturret.setScale(.005)
        #self.enemyturret.setH(180)

        self.enemybase = Actor("base.egg")
        self.enemybase.reparentTo(render)
        #self.enemybase.setScale(.005)
        #self.enemybase.setH(180)

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

        #self.enemycannon.setPos(self.enemybase.getX(),self.enemybase.getY(),self.enemybase.getZ())
        self.enemycannon.setHpr(modifiedheading,modifiedpitch,0)
        self.enemyturret.setHpr(modifiedheading-headingoffset,0,0)
        self.enemyturret.setPos(self.enemybase.getX(),self.enemybase.getY(),self.enemybase.getZ())

        dist = self.enemycannon.getP()*-1 #When the cannon pitches upwards it moves backwards a bit...this fixes it...but I have no idea why it works
        angle = deg2Rad(self.enemycannon.getH())
        dx = dist * math.sin(angle) #Calculate change in x direction
        dy = dist * -math.cos(angle)#Calculate change in y direction   
        dx = dx/40
        dy = dy/40
        self.enemycannon.setPos(self.enemybase.getX()+dx,self.enemybase.getY()+dy,self.enemybase.getZ())
        return Task.cont        
