import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import *
from direct.task import Task
    
from direct.gui.OnscreenImage import OnscreenImage
from pandac.PandaModules import TransparencyAttrib
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *

import sys, math, os, random
import world, entity, projectile

from pandac.PandaModules import Filename

class PlayerTank(entity.entity): #use to create player tank
    def __init__(self):
        #NOTE!!!: I couldn't get the models to load conveniently (I believe panda needs an absolute path
        #So in your panda config file (located in Panda3d-1.5.3/etc paste the line where the sumotanks file is
        #for me I had to paste: model-path    C:\Documents and Settings\therrj\Desktop\sumotanks\art\tank
        #Put this where the other model-path lines are
        #If there is a more convenient way to do this feel free
        self.isMoving = False

        self.cannon = Actor("cannongreen.egg")
        self.cannon.setScale(.75)
        self.cannon.reparentTo(render)
        self.turret = Actor("turretgreen.egg")
        self.turret.setScale(.75)
        self.turret.reparentTo(render)

        self.base = Actor("basegreen.egg", {"moveforwards":"forwards.egg","movebackwards":"backwards.egg", "turnleft":"left.egg","turnright":"right.egg"})
        self.base.setScale(.75)        
        self.base.reparentTo(render)
        
        self.moveforwardscontrol=self.base.getAnimControl("moveforwards") #Set animation control for moveforwards
        self.movebackwardsscontrol=self.base.getAnimControl("movebackwards") #Set animation control for moveforwards
        self.turnleftcontrol=self.base.getAnimControl("turnleft") #Set animation control for moveforwards
        self.turnrightcontrol=self.base.getAnimControl("turnright") #Set animation control for moveforwards
                
        self.headlight = Spotlight("headLight")
        self.headlightNP = render.attachNewNode(self.headlight)
        self.headlightstatus = 0
       
        self.xycameradistance = 15    
        self.zcameradistance = 15
        self.cannonmove = 5

        self.keyMap = {"left":0, "right":0, "forward":0, "back":0, "headlight":0, "fire":0}
    
        self.prevtimeforTurret = 0
        self.prevtimeforBase = 0

        self.crosshair = Actor("panda-model")
        #self.crosshair.reparentTo(render)
        self.crosshair.setScale(.000000001)
        self.crosshair.setH(180)

        self.crosshair2d = OnscreenImage(image = "cannoncrosshair.png", pos=(0,0,0),scale=0.1)
        self.crosshair2d.setTransparency(TransparencyAttrib.MAlpha)

        
        self.currentweapon = 1 #1 for cannon 2 for machine gun
        self.currentweaponimage = OnscreenImage(image = "cannonimage.png", pos=(-.99,0,.87),scale=.3)
        self.currentweaponimage.setTransparency(TransparencyAttrib.MAlpha)

        self.damage = 1
        self.crosshair3d = [] #Crosshair in 3d space (needs to be converted to 2d for drawing crosshair)

        self.prevtimeforPlayer = 0

        self.nodePath = self.addCollisionBoundaries()

        self.projectiles = list()
        self.fireCount = 60
        self.fired = False

        entity.entity.__init__(self, 5)
        
    def addCollisionBoundaries(self):
        self.cHandler = CollisionHandlerEvent()
        self.cHandler.setInPattern("hit-%in")
        cSphere = CollisionSphere(0, 0, 0, 3)
        cNode = CollisionNode("Player")
        cNode.addSolid(cSphere)
        cNP = self.base.attachNewNode(cNode)
        #cNP.show()
   
        base.cTrav.addCollider(cNP, self.cHandler)
        
        self.accept("hit-Enemy", self.hitEnemy)
        
        return cNP
        
    def hitEnemy(self, entry):
        print "Player hit enemy"

    def setkeyMap(self, keyMap):
        self.keyMap = keyMap

    def setTexture(self,key):
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
    
    def setcurrentWeapon(self, weapon, image):
        self.currentweaponimage.destroy()
        self.currentweapon = weapon
        self.currentweaponimage = OnscreenImage(image = image, pos=(-.99,0,.87),scale=.3)
        self.currentweaponimage.setTransparency(TransparencyAttrib.MAlpha)
        
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
        
        dist = .1
        angle = deg2Rad(self.turret.getH())
        dx = dist * math.sin(angle) #Calculate change in x direction
        dy = dist * -math.cos(angle)#Calculate change in y direction
        self.headlightNP.setPosHpr(self.base.getX()+dx,self.base.getY()+dy,self.base.getZ(),self.base.getH()+180,self.base.getP(),0)
 

        return Task.cont

    def getCoordinates(self):
        position = self.turret.getPos()
        return([self.turret.getX(),self.turret.getY(),self.turret.getZ()])

    

    def movePlayer(self,task):
        """Code to move the base of the players tank"""
        delta = task.time - self.prevtimeforPlayer
        self.update()
        self.base.setPos(self.base.getX() + self.vel.xcomp(), self.base.getY() + self.vel.ycomp(), 0)
        if self.keyMap["forward"]:
            angle = self.base.getH()
            self.move.magnitude = 1.2
            self.move.angle = deg2Rad(angle-90)
        elif self.keyMap["back"]:
            angle = self.base.getH()
            self.move.magnitude = -1.2
            self.move.angle = deg2Rad(angle-90)
        if self.keyMap["left"]:
            self.base.setH(self.base.getH() + delta*100) #fiddle with this number to determine how fast it moves)
        elif self.keyMap["right"]:
            self.base.setH(self.base.getH() - delta*100) #fiddle with this number to determine how fast it moves)
        if not self.keyMap["forward"] and not self.keyMap["back"]:
           self.move.magnitude = 0
        #Code to determine animations:
        if self.keyMap["forward"]:
            if self.isMoving == False:
                self.moveforwardscontrol.setPlayRate(10)#set play rate for moveforwards animation
                self.base.loop("moveforwards")
                self.isMoving = True
        elif self.keyMap["back"]:
            if self.isMoving == False:
                self.movebackwardsscontrol.setPlayRate(10)#set play rate for movebackwards animation
                self.base.loop("movebackwards")
                self.isMoving = True
        elif self.keyMap["left"]:
            if self.isMoving == False:
                self.turnleftcontrol.setPlayRate(10)#set play rate for turnleft animation
                self.base.loop("turnleft")
                self.isMoving = True
        elif self.keyMap["right"]:
            if self.isMoving == False:
                self.turnrightcontrol.setPlayRate(10)#set play rate for turnright animation
                self.base.loop("turnright")
                self.isMoving = True
        else:
            if self.isMoving:
                self.base.stop()
                self.isMoving = False

        if self.isMoving:
            self.soundqueue.loop('engine')#, [self.base.getX()], [self.base.getY()], [self.base.getZ()])
        else:
               self.isMoving = False

        if self.isMoving:
            self.soundqueue.loop('engine')
        else:
            self.soundqueue.unloop('engine')

        self.moveplayerTurret()    
        self.prevtimeforPlayer = task.time
        return Task.cont              

    def fire(self, task):
        delta = task.time - self.prevtimeforPlayer
        if self.fired:
            self.fireCount -= 1
            if self.fireCount == 0:
                self.fireCount = 60
                self.fired = False
        if self.keyMap["fire"] and not self.fired:
            print "IT FIRED!"
            print self.cannon.getP()
            shot = projectile.projectile(.1, self.vel.xcomp(), self.vel.ycomp(), deg2Rad(self.base.getH()-90), deg2Rad(self.cannon.getP()))
            forces = entity.force(3-3*math.cos(self.cannon.getP()), deg2Rad(self.cannon.getH()-90))
            shot.vel = shot.vel.add(forces)
            shot.model.setPos(self.cannon.getX(), self.cannon.getY(), self.cannon.getZ())
            self.projectiles.append(shot)
            self.fired = True
        for i in range(len(self.projectiles)):
            self.projectiles[i].zv -= .3
            self.projectiles[i].model.setPos(self.projectiles[i].model.getX() + self.projectiles[i].vel.xcomp(), self.projectiles[i].model.getY() + self.projectiles[i].vel.ycomp(), self.projectiles[i].model.getZ() + self.projectiles[i].zv)
        self.prevtimeforPlayer = task.time
        return Task.cont

        
    def moveplayerTurret(self):
        #Set Position on top of base:
        baseposition = self.base.getPos()
        self.turret.setPos(self.base.getX(),self.base.getY(),self.base.getZ())
        
        if base.mouseWatcherNode.hasMouse():        
            x=base.mouseWatcherNode.getMouseX() #get mouse coordinates
            y=base.mouseWatcherNode.getMouseY() 
            move = [x,y] #Where mouse moved to 
            factor = 10
            base.win.movePointer(0, 400, 300) #Move cursor to center of screen
            deltaHeading = self.cannon.getH() + move[0] * -100 #Calculate change in heading
            deltaPitch = self.cannon.getP() + move[1] * -100   #Calculate change in pitch

            if deltaPitch < -20:
                deltaPitch = -20
            if deltaPitch > -1:
                deltaPitch = -1           

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
    
        dist = 20
        angle = deg2Rad(self.cannon.getH())
        dx = dist * math.sin(angle) #Calculate change in x direction
        dy = dist * -math.cos(angle)#Calculate change in y direction    
    
        dist = 15
        angle = deg2Rad(self.cannon.getP())
        dz = dist*math.tan(angle)   #Calculate change in pitch
    
        pitch = self.cannon.getP()  #Set pitch of camera (limits it so player can only look so high and so low)
        if self.cannon.getP() > 8.6:
            pitch = 8.6
        if self.cannon.getP() < -4.6:
            pitch = -4.6
        pitch +=5
        camera.setPosHpr(xposition-dx,yposition-dy,self.base.getZ()+5,self.cannon.getH()+180,-pitch,0) #Set camera position, heading, pitch and roll
        
        #Set Crosshair position - If you are moving rediculously fast this gets out of alignment...I don't know why
        
        xvalues = (xposition+dx-xposition)  #Distance formula
        yvalues = (yposition+dy-yposition)
        xsquared = math.pow(xvalues,2)
        ysquared = math.pow(yvalues,2)
        distance = math.sqrt(xsquared+ysquared) 
        pitch = self.cannon.getP()*-1
        pitch = deg2Rad(pitch)
        dz = (math.tan(pitch)) * (distance)
        
        self.crosshair.setPosHpr(xposition+dx,yposition+dy,dz,self.turret.getH(),0,0)
        # Convert the point into the camera's coordinate space 
        p3d = base.camera.getRelativePoint(self.crosshair, Point3(self.crosshair.getX(),self.crosshair.getY(),self.crosshair.getZ()))
        # Ask the lens to project the 3-d point to 2-d. 
        p2d = Point2()
                
        if base.camLens.project(p3d, p2d):
            self.crosshair2d.destroy()
            if self.currentweapon == 1:
                self.crosshair2d=OnscreenImage(image = "cannoncrosshair.png", pos=(p2d[0],0,p2d[1]),scale=0.1)
                self.crosshair2d.setTransparency(TransparencyAttrib.MAlpha)        
            elif self.currentweapon == 2:
                self.crosshair2d=OnscreenImage(image = "machineguncrosshair.png", pos=(p2d[0],0,p2d[1]),scale=0.1)
                self.crosshair2d.setTransparency(TransparencyAttrib.MAlpha)

    







