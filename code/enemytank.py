import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import *
from direct.task import Task
import sys, math
import random
import world, entity, projectile
     
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

        self.moveforwardscontrol=self.base.getAnimControl("moveforwards") #Set animation control for moveforwards
        self.movebackwardsscontrol=self.base.getAnimControl("movebackwards") #Set animation control for moveforwards
        self.turnleftcontrol=self.base.getAnimControl("turnleft") #Set animation control for moveforwards
        self.turnrightcontrol=self.base.getAnimControl("turnright") #Set animation control for moveforwards
        
        entity.entity.__init__(self, 5)
        self.base.setName("enemy")
        self.base.setPos(15,15,0)
        self.playerPos = [0,0,0]
        self.loweraimingoffset = -1
        self.upperaimingoffset = 1

        self.keyMap = {"left":0, "right":0, "forward":0, "back":0, "fire":1}
        self.forwardsflag = False

        self.damage = 1

        self.prevtimeforPlayer = 0
        self.prevtimeforPlayerShooting = 0
        self.isMoving = 0

        self.haschangedtexture = False

        self.oldvel = entity.force(0,0)
        
        self.world = world
        self.nodePath = self.addCollisionBoundaries()

        self.charge = 0

        self.currentweapon = 1

        self.projectiles = list()
        self.fireCountCannon = 60
        self.fireCountMG = 10
        self.firedCannon = False
        self.firedMG = False

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
        
        self.accept("hit-Player", self.enemyHitPlayer)
        
        return cNP

    def enemyHitPlayer(self, entry):
        if entry.getFromNode().getName() == "Bullet" or entry.getFromNode().getName() == "Cannon":
            return
        XDiff = -(self.vel.xcomp()-self.world.player.oldvel.xcomp())
        YDiff = -(self.vel.ycomp()-self.world.player.oldvel.ycomp())
        speed = self.vel.magnitude
        if self.vel.magnitude >= 0:
            speed += .3
        else:
            speed -= .3
        if XDiff > 0:
            if YDiff > 0:
                Angle = math.degrees(math.atan(YDiff/XDiff))
                XSpeed = -speed*math.cos(math.radians(Angle))
                YSpeed = -speed*math.sin(math.radians(Angle))
            elif YDiff < 0:
                Angle = math.degrees(math.atan(YDiff/XDiff))
                XSpeed = -speed*math.cos(math.radians(Angle))
                YSpeed = -speed*math.sin(math.radians(Angle))
        elif XDiff < 0:
            if YDiff > 0:
                Angle = 180 + math.degrees(math.atan(YDiff/XDiff))
                XSpeed = -speed*math.cos(math.radians(Angle))
                YSpeed = -speed*math.sin(math.radians(Angle))
            elif YDiff < 0:
                Angle = -180 + math.degrees(math.atan(YDiff/XDiff))
                XSpeed = -speed*math.cos(math.radians(Angle))
                YSpeed = -speed*math.sin(math.radians(Angle))
        elif XDiff == 0:
            if YDiff > 0:
                Angle = -90
            else:
                Angle = 90
            XSpeed = -speed*math.cos(math.radians(Angle))
            YSpeed = -speed*math.sin(math.radians(Angle))
        elif YDiff == 0:
            if XDiff < 0:
                Angle = 0
            else:
                Angle = 180
            XSpeed = -speed*math.cos(math.radians(Angle))
            YSpeed = -speed*math.sin(math.radians(Angle))
        if self.damage < 5:
            damfact = 5
        damfact = self.damage
        self.oldvel = self.vel
        self.vel.magnitude = -damfact*0.3*math.sqrt((math.pow(XSpeed,2) + math.pow(YSpeed,2)))
        #print "X: ", XSpeed, " Y: ", YSpeed
        if self.vel.magnitude < -4:
            self.vel.magnitude = -4
        self.damage += 1
        # uncomment the next line for debug infos
        #print entry
        
    def setplayerPos(self,playerPosition):
        self.playerPos = playerPosition

    def decide(self):
        hdist = math.sqrt((self.base.getX() - self.playerPos[0]) ** 2 + (self.base.getY() - self.playerPos[1]) ** 2)
        
        if hdist > 15 or hdist < 7:
            self.currentweapon = 2
        else:
            self.currentweapon = 1

        if self.charge:
            if math.sqrt((self.base.getX()) ** 2 + (self.base.getY()) ** 2) + 4 > math.sqrt((self.playerPos[0]) ** 2 + (self.playerPos[1]) ** 2):
                self.charge = False
                return [self.playerPos[0] / 2, self.playerPos[1] / 2]
            else:
                return [self.playerPos[0], self.playerPos[1]]
        if math.sqrt((self.base.getX() - self.playerPos[0] / 2) ** 2 + (self.base.getY() - self.playerPos[1] / 2) ** 2) < 5:
            self.charge = True
            return [self.playerPos[0], self.playerPos[1]]

        return [self.playerPos[0] / 2, self.playerPos[1] / 2]




    def moveEnemy(self,task):
        """Move enemy base and then the turret"""

        #Put code to move base here:
        goalpoint = self.decide()

        goalheading = ((rad2Deg(math.atan2((self.base.getY() - goalpoint[1]), (self.base.getX() - goalpoint[0]))) + 180))
        absolutebase = (self.base.getH() + 270) % 360
        while absolutebase < 0:
            absolutebase += 360
        theta = goalheading - absolutebase

        if theta > 180:
            theta -= 360
        if theta < -180:
            theta += 360

        if theta < 90 and theta > -90:
            self.forwardsflag = True
            if theta > 1 and theta < 179 or theta < -1 and theta > -179:
                if theta < 0:
                    self.keyMap["right"] = True
                    self.keyMap["left"] = False
                else:
                    self.keyMap["left"] = True
                    self.keyMap["right"] = False
            else:
                self.keyMap["right"] = False
                self.keyMap["left"] = False

        else:
            self.forwardsflag = False
            if theta > 1 and theta < 179 or theta < -1 and theta > -179:
                if theta < 0:
                    self.keyMap["right"] = False
                    self.keyMap["left"] = True
                else:
                    self.keyMap["left"] = False
                    self.keyMap["right"] = True
            else:
                self.keyMap["right"] = False
                self.keyMap["left"] = False


        hdistance = math.sqrt((self.base.getX() - goalpoint[0]) ** 2 + (self.base.getY() - goalpoint[1]) ** 2)

        if hdistance > 3 and not (theta > 45 and theta < 135 or theta < -45 and theta > -135):
            self.keyMap["back"] = not self.forwardsflag
            self.keyMap["forward"] = self.forwardsflag
            pass
            
        else:
            self.keyMap["back"] = False
            self.keyMap["forward"] = False

        #actual movement code
        delta = task.time - self.prevtimeforPlayer
        self.update()
        self.base.setPos(self.base.getX() + self.vel.xcomp(), self.base.getY() + self.vel.ycomp(), 0)
        self.oldvel = self.vel
        if self.haschangedtexture == True:
            self.haschangedtexture = False
            self.isMoving = False
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
                self.moveforwardscontrol.setPlayRate(4)#set play rate for moveforwards animation
                self.base.loop("moveforwards")
                self.isMoving = True
        elif self.keyMap["back"]:
            if self.isMoving == False:
                self.movebackwardsscontrol.setPlayRate(4)#set play rate for movebackwards animation
                self.base.loop("movebackwards")
                self.isMoving = True
        elif self.keyMap["left"]:
            if self.isMoving == False:
                self.turnleftcontrol.setPlayRate(4)#set play rate for turnleft animation
                self.base.loop("turnleft")
                self.isMoving = True
        elif self.keyMap["right"]:
            if self.isMoving == False:
                self.turnrightcontrol.setPlayRate(4)#set play rate for turnright animation
                self.base.loop("turnright")
                self.isMoving = True
        else:
            if self.isMoving:
                self.base.stop()
                self.isMoving = False

        if self.isMoving:
            self.soundqueue.loop('enemyengine')#, [self.base.getX()], [self.base.getY()], [self.base.getZ()])
        else:
               self.isMoving = False

        if self.isMoving:
            self.soundqueue.loop('enemyengine')
        else:
            self.soundqueue.unloop('enemyengine')



        self.moveenemyTurret() #Move enemy turret (to keep the code separate, but still update both in the same frame
        self.prevtimeforPlayer = task.time
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
        
        headingoffset = (random.random() - .5) * (10 + self.world.player.vel.magnitude * 2) #random offset for heading
        pitchoffset = (random.random() - .5) * (10 + self.world.player.vel.magnitude * 2)   #random offset for pitch
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

    def fire(self, task):
        delta = task.time - self.prevtimeforPlayerShooting
        #print "Turret Pos: ", self.turret.getPos()
        if self.firedCannon:
            self.fireCountCannon -= 1
            if self.fireCountCannon == 0:
                self.fireCountCannon = 60
                self.firedCannon = False
        if self.firedMG:
            self.fireCountMG -= 1
            if self.fireCountMG == 0:
                self.fireCountMG = random.randint(8,14)
                self.firedMG = False
        if self.keyMap["fire"] and ((not self.firedCannon and self.currentweapon == 1) or (not self.firedMG and self.currentweapon == 2)):
            lenCannon = 1
            if self.currentweapon == 1:
                shot = projectile.projectile(.1, self, lenCannon, deg2Rad(self.cannon.getP()+90), deg2Rad(self.cannon.getH()-90), 1 )
                self.soundqueue.enqueue('cannon', self.base.getX(), self.base.getY(), self.base.getZ())
            else:
                shot = projectile.projectile(.1, self, lenCannon, deg2Rad(self.cannon.getP()+90), deg2Rad(self.cannon.getH()-90), 2 )
                self.soundqueue.enqueue('bang', self.base.getX(), self.base.getY(), self.base.getZ())
            shot.velx += self.vel.xcomp()
            shot.vely += self.vel.ycomp()

            proj = lenCannon * math.sin(self.cannon.getP()+90)
            tipx = proj * math.cos(self.cannon.getH()-90)
            tipy = proj * math.sin(self.cannon.getH()-90)
            tipz = lenCannon * math.cos(self.cannon.getP()+90)
            shot.model.setPos((self.base.getX()), (self.base.getY()), (self.base.getZ()-1))
            shot.model.setH(self.cannon.getH())
            #print "Shot model: ", shot.model.getPos()
            #print "Cannon model: ", self.cannon.getPos()
            self.projectiles.append(shot)
            if self.currentweapon == 1:
                self.firedCannon = True
            else:
                self.firedMG = True
        for i in range(len(self.projectiles)):
            if i < len(self.projectiles):
                if self.projectiles[i].model.getZ() < -20 or self.projectiles[i].model.getZ() > 150 or math.sqrt((self.projectiles[i].model.getX()) ** 2 + (self.projectiles[i].model.getY()) ** 2) > 200:
                    self.projectiles[i].model.removeNode()
                    del self.projectiles[i]
                    i -= 1
                else:                
                    self.projectiles[i].model.setPos(self.projectiles[i].model.getX() + self.projectiles[i].velx, self.projectiles[i].model.getY() + self.projectiles[i].vely, self.projectiles[i].model.getZ() + self.projectiles[i].velz)
                    self.projectiles[i].grav()
        self.prevtimeforPlayerShooting = task.time
        return Task.cont

        

	def shootatPlayer(self):
		pass;
