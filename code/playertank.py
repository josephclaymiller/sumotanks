import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import *
from direct.task import Task
import sys, math
import random
import world

import sys,os
from pandac.PandaModules import Filename

class PlayerTank(DirectObject): #use to create player tank
    def __init__(self):
        #NOTE!!!: I couldn't get the models to load conveniently (I believe panda needs an absolute path
        #So in your panda config file (located in Panda3d-1.5.3/etc paste the line where the sumotanks file is
        #for me I had to paste: model-path    C:\Documents and Settings\therrj\Desktop\sumotanks\art\tank
        #Put this where the other model-path lines are
        #If there is a more convenient way to do this feel free


        self.cannon = Actor("cannon.egg")
        self.cannon.reparentTo(render)
        self.turret = Actor("turret.egg")
        self.turret.reparentTo(render)
#        self.turret = Actor("panda-model", {"walk":"panda-walk4"})
#        self.turret.reparentTo(render)
#        self.turret.setScale(.005)
#        self.turret.setH(180)

        #self.base = Actor("../art/tank/newtank")
        self.base = Actor("newtank.egg")
        
        self.base.reparentTo(render)
#        self.base.setScale(.005)
#        self.base.setH(180) 

        self.headlight = Spotlight("headLight")
        self.headlightNP = render.attachNewNode(self.headlight)
        self.headlightstatus = 0
       
        self.xycameradistance = 15    
        self.zcameradistance = 15
        self.cannonmove = 5

        self.keyMap = {"left":0, "right":0, "forward":0, "back":0, "headlight":0}
    
        self.prevtimeforTurret = 0
        self.prevtimeforBase = 0


    def setkeyMap(self, keyMap):
        self.keyMap = keyMap
        #print self.keyMap

    def toggleHeadlights(self):
        if self.headlightstatus == 1: #Headlight is on...turn it off
            print "Turn headlight off"
            render.clearLight(self.headlightNP)
            self.headlightstatus = 0
        elif self.headlightstatus == 0: #Headlight is off...turn it on
            print "Turn headlight on"
            render.setLight(self.headlightNP)
            self.headlightstatus = 1

    def setHeadlights(self,task):
        self.headlight.setColor(VBase4(1, 1, 1, 1))
        lens = PerspectiveLens()
        self.headlight.setLens(lens)
        #self.headlightNP = self.base.attachNewNode(self.headlight)
        #self.headlightNP.setH(self.base.getH()+360)
        
        dist = .1
        angle = deg2Rad(self.turret.getH())
        dx = dist * math.sin(angle) #Calculate change in x direction
        dy = dist * -math.cos(angle)#Calculate change in y direction
        self.headlightNP.setPosHpr(self.base.getX()+dx,self.base.getY()+dy,self.base.getZ(),self.base.getH()+180,self.base.getP(),0)
 

        return Task.cont
    
    def moveplayerBase(self,task):
        """Code to move the base of the players tank"""
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
        self.turret.setPos(self.base.getX(),self.base.getY(),self.base.getZ())
        #self.cannon.setPos(self.base.getX(),self.base.getY(),self.base.getZ())


        if base.mouseWatcherNode.hasMouse():        
            x=base.mouseWatcherNode.getMouseX() #get mouse coordinates
            y=base.mouseWatcherNode.getMouseY() 
            move = [x,y] #Where mouse moved to 
            factor = 10
            base.win.movePointer(0, 400, 300) #Move cursor to center of screen
            deltaHeading = self.cannon.getH() + move[0] * -100 #Calculate change in heading
            deltaPitch = self.cannon.getP() + move[1] * -100   #Calculate change in pitch

            if deltaPitch < -30:
                deltaPitch = -30
            if deltaPitch > 0:
                deltaPitch = 0           

            self.turret.setH(deltaHeading) #Animate change in heading
            self.cannon.setH(deltaHeading)
            #self.turret.setP(deltaPitch)   #Animate change in pitch - this would be for the actual gun, if we were going to give it the ability to move up and down
            self.cannon.setP(deltaPitch)   #Animate change in pitch - this would be for the actual gun, if we were going to give it the ability to move up and down
        
        
        dist = self.cannon.getP()*-1 #When the cannon pitches upwards it moves backwards a bit...this fixes it...but I have no idea why it works
        angle = deg2Rad(self.cannon.getH())
        dx = dist * math.sin(angle) #Calculate change in x direction
        dy = dist * -math.cos(angle)#Calculate change in y direction   
        dx = dx/40
        dy = dy/40
        self.cannon.setPos(self.base.getX()+dx,self.base.getY()+dy,self.base.getZ())


        position = self.cannon.getPos()
        xposition = self.cannon.getX() #Used to get current coordinates of the turret
        yposition = self.cannon.getY()
        zposition = self.cannon.getZ()
    
        #dist = self.xycameradistance #Distance the camera will be behind the turret
        dist = 20
        angle = deg2Rad(self.cannon.getH())
        dx = dist * math.sin(angle) #Calculate change in x direction
        dy = dist * -math.cos(angle)#Calculate change in y direction    

    
        #dist = self.zcameradistance
        dist = 15
        angle = deg2Rad(self.cannon.getP())
        dz = dist*math.tan(angle)   #Calculate change in pitch
    
        pitch = self.cannon.getP()  #Set pitch of camera (limits it so player can only look so high and so low
        if self.cannon.getP() > 8.6:
            pitch = 8.6
        if self.cannon.getP() < -8.6:
            pitch = -8.6
        #print pitch
        pitch +=8
        camera.setPosHpr(xposition-dx,yposition-dy,self.base.getZ()+6,self.cannon.getH()+180,-pitch,0) #Set camera position, heading, pitch and roll
        
        #position = self.turret.getPos()
       
        self.prevtimeforTurret = task.time
        
        return Task.cont #Continue updating this task
