import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject

import direct.directbase.DirectStart
from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import *
from direct.task import Task
import sys, math
import random
import world

class Tank(DirectObject): #put tank code in here
    def __init__(self):
        self.prevtime = 0
        self.xycameradistance = 15    
        self.zcameradistance = 15

    def moveTurret(self, task): #right now it uses the panda as the turret...
        """move the turret, and the camera with it"""
        delta = task.time - self.prevtime 
        if base.mouseWatcherNode.hasMouse():        
            x=base.mouseWatcherNode.getMouseX() #get mouse coordinates
            y=base.mouseWatcherNode.getMouseY() 
            move = [x,y] #Where mouse moved to 
            factor = 10
            base.win.movePointer(0, 400, 300) #Move cursor to center of screen
            deltaHeading = self.turret.getH() + move[0] * -100 #Calculate change in heading
            deltaPitch = self.turret.getP() + move[1] * -100   #Calculate change in pitch

            if deltaPitch < -30:
                deltaPitch = -30
            if deltaPitch > 0:
                deltaPitch = 0           

            self.turret.setH(deltaHeading) #Animate change in heading
            self.turret.setP(deltaPitch)   #Animate change in pitch - this would be for the actual gun, if we were going to give it the ability to move up and down
    
        position = self.turret.getPos()
        xposition = self.turret.getX() #Used to get current coordinates of the turret
        yposition = self.turret.getY()
        zposition = self.turret.getZ()
    
        dist = self.xycameradistance #Distance the camera will be behind the turret
        angle = deg2Rad(self.turret.getH())
        dx = dist * math.sin(angle) #Calculate change in x direction
        dy = dist * -math.cos(angle)#Calculate change in y direction
    
        dist = self.zcameradistance
        angle = deg2Rad(self.turret.getP())
        dz = dist*math.tan(angle)   #Calculate change in pitch
    
        pitch = self.turret.getP()  #Set pitch of camera (limits it so player can only look so high and so low
        if self.turret.getP() > 8.6:
            pitch = 8.6
        if self.turret.getP() < -7:
            pitch = -7
    
        camera.setPosHpr(xposition-dx,yposition-dy,2,self.turret.getH()+180,-pitch,0) #Set camera position, heading, pitch and roll
        
        position = self.turret.getPos()
       
        self.prevtime = task.time
        
        return Task.cont #Continue updating this task
        #return Task.done to remove task from the task manager (we want this to run continuously)   

#    def moveenemyTurret(self,task): #used so enemy turret is aimed at the player
#        position = self.enemyturret.getPos()
#        xposition = self.enemyturret.getX() #Used to get current coordinates of the turret
#        yposition = self.enemyturret.getY()
#        zposition = self.enemyturret.getZ()

#        playerposition
#        #print position
#        #playerposition = PlayerTank.getCoordinates()
#        playerxposition = 1000#PlayerTank.turret.getX()
#        playeryposition = 100#PlayerTank.turret.getY()
#        #playerzposition = 0#PlayerTank.turret.getZ()
#        heading = math.atan((playeryposition-yposition)/(playerxposition-xposition))
#        #inverse tan y2-y1/x2-x1
#        heading = -rad2Deg(heading)
#        #print playerposition
#        #print self.playercoordinates
#        #print heading
        
#        #atan2f(ax-bx, ay-by)
#        self.enemyturret.setHpr(heading,0,0)
#        return Task.cont        


class PlayerTank(Tank): #use to create player tank
    def __init__(self):
        Tank.__init__(self)
        self.turret = Actor("panda-model", {"walk":"panda-walk4"})
        self.turret.reparentTo(render)
        self.turret.setScale(.005)
        self.turret.setH(180)

    def getCoordinates(self):
        position = self.turret.getPos()
        return([self.turret.getX(),self.turret.getY(),self.turret.getZ()])


class EnemyTank(Tank):  #use to create computer tank
    def __init__(self):
        Tank.__init__(self)
        self.enemyturret = Actor("panda-model", {"walk":"panda-walk4"})
        self.enemyturret.reparentTo(render)
        self.enemyturret.setScale(.005)
        self.enemyturret.setH(180)
        self.enemyturret.setPos(7,7,0)
        self.playerPos = [0,0,0]

    def setplayerPos(self,playerPosition):
        self.playerPos = playerPosition

        #so aimComputerTurret(self,task,playerPos)
    def moveenemyTurret(self,task): #used so enemy turret is aimed at the player
        position = self.enemyturret.getPos()
        xposition = self.enemyturret.getX() #Used to get current coordinates of the turret
        yposition = self.enemyturret.getY()
        zposition = self.enemyturret.getZ()
        #print self.playerPos
        #print self.playerPos[0]
        #playerposition
        #print position
        #playerposition = PlayerTank.getCoordinates()
        #playerxposition = 1000#PlayerTank.turret.getX()
        #playeryposition = 100#PlayerTank.turret.getY()
        #playerzposition = 0#PlayerTank.turret.getZ()
        #heading = rad2Deg(math.atan((self.playerPos[1]-yposition)/(self.playerPos[0]-xposition)))
        dx = self.playerPos[0]-xposition
        dy = self.playerPos[1]-yposition
        heading = rad2Deg(math.atan2(dy, dx))
        #inverse tan y2-y1/x2-x1
        
        #if(self.playerPos[1]-yposition > 0): 
        #    heading = 360-heading
        #else:
        #    heading = 360+heading



        #heading*=-1
        #heading = -rad2Deg(heading)
        #print playerposition
        #print self.playercoordinates
        #print heading
        heading = heading+90
        #atan2f(ax-bx, ay-by)
        self.enemyturret.setHpr(heading,0,0)
        return Task.cont        
