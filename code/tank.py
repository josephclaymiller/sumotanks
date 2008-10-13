import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import *
from direct.task import Task
import sys, math
import random
import world

class PlayerTank(DirectObject): #use to create player tank
    def __init__(self):
        self.turret = Actor("panda-model", {"walk":"panda-walk4"})
        self.turret.reparentTo(render)
        self.turret.setScale(.005)
        self.turret.setH(180)
        
        self.base = Actor("panda-model")
        self.base.reparentTo(render)
        self.base.setScale(.005)
        self.base.setH(180) 

        self.xycameradistance = 15    
        self.zcameradistance = 15

        self.keyMap = {"left":0, "right":0, "forward":0, "back":0}
    
        self.prevtimeforTurret = 0
        self.prevtimeforBase = 0


    def setkeyMap(self, keyMap):
        self.keyMap = keyMap
        #print self.keyMap

    def moveplayerBase(self,task):
        delta = task.time - self.prevtimeforBase
        if self.keyMap["forward"]:
            dist = 0.1
            angle = deg2Rad(self.base.getH())
            dx = dist * math.sin(angle)
            dy = dist * -math.cos(angle)
            self.base.setPos(self.base.getX() + dx, self.base.getY() + dy, 0) 
        if self.keyMap["left"]:
            self.base.setH(self.base.getH() + delta*100) #fiddle with this number to determine how fast it moves)
        if self.keyMap["right"]:
            self.base.setH(self.base.getH() - delta*100) #fiddle with this number to determine how fast it moves)
        if self.keyMap["back"]:
            dist = 0.1
            angle = deg2Rad(self.base.getH())
            dx = dist * math.sin(angle)
            dy = dist * -math.cos(angle)
            self.base.setPos(self.base.getX() - dx, self.base.getY() - dy, 0)
        
        self.prevtimeforBase = task.time        
        return Task.cont

    def getCoordinates(self):
        position = self.turret.getPos()
        return([self.turret.getX(),self.turret.getY(),self.turret.getZ()])


    def moveplayerTurret(self, task): #right now it uses the panda as the turret...
        """move the turret, and the camera with it"""
        delta = task.time - self.prevtimeforTurret

        #Set Position on top of base:
        baseposition = self.base.getPos()
        self.turret.setPos(self.base.getX(),self.base.getY(),2)


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
       
        self.prevtimeforTurret = task.time
        
        return Task.cont #Continue updating this task
       
class EnemyTank(DirectObject):  #use to create computer tank
    def __init__(self):
        
        self.enemyturret = Actor("panda-model", {"walk":"panda-walk4"})
        self.enemyturret.reparentTo(render)
        self.enemyturret.setScale(.005)
        self.enemyturret.setH(180)
        self.enemyturret.setPos(7,7,0)
        self.playerPos = [0,0,0]

    def setplayerPos(self,playerPosition):
        self.playerPos = playerPosition

    def moveenemyTurret(self,task): #used so enemy turret is aimed at the player
        position = self.enemyturret.getPos()
        xposition = self.enemyturret.getX() #Used to get current coordinates of the turret
        yposition = self.enemyturret.getY()
        zposition = self.enemyturret.getZ()
        dx = self.playerPos[0]-xposition
        dy = self.playerPos[1]-yposition
        heading = rad2Deg(math.atan2(dy, dx))
        heading = heading+90
        self.enemyturret.setHpr(heading,0,0)
        return Task.cont        
