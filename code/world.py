import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
import playertank, enemytank
from pandac.PandaModules import *
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import *
from direct.task import Task
from direct.filter.CommonFilters import CommonFilters
import sys, math
import soundqueue
from direct.gui.OnscreenImage import OnscreenImage
from pandac.PandaModules import TransparencyAttrib
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *

class World(DirectObject):
    def __init__(self):
        #pass
        base.cTrav = CollisionTraverser('traverser')
        self.tankGroundHandler = CollisionHandlerQueue()
        self.floorHandler = CollisionHandlerFloor()

        self.worldvalue = 1 #If there is one...
        self.keyMap = {"left":0, "right":0, "forward":0, "back":0, "enter":0, "fire":0}  

        #Make mouse invisible
        props = WindowProperties()
        props.setCursorHidden(True) 
        base.win.requestProperties(props)      

        #Sets up glow mapping based on alpha channel
        self.filters = CommonFilters(base.win, base.cam)
        filterok = self.filters.setBloom(blend=(0,0,0,1), desat= 0.0, intensity=2.2, size="small")
        self.soundqueue = soundqueue.SoundQueue()
        self.soundqueue.loop('menumusic')

        self.accept("escape", sys.exit)
        self.hud = OnscreenImage(image = "hud.png", pos=(0,0,.85),scale = (1.35,0,.157))
        self.hudweapon = OnscreenImage(image = "currentWeaponCannon.png", pos = (-.95,0,.75),scale=(.23,1,.05))
        self.hudweapon.setTransparency(TransparencyAttrib.MAlpha)
        self.playerhudhealth = OnscreenImage(image = "playerDamage.png", pos=(-.4,0,.75), scale=(.15,0,.05))
        self.playerhudhealth.setTransparency(TransparencyAttrib.MAlpha)
        self.enemyhudhealth = OnscreenImage(image = "enemyDamage.png", pos=(.4,0,.75), scale=(.15,0,.05))
        self.enemyhudhealth.setTransparency(TransparencyAttrib.MAlpha)
        self.treadglow = OnscreenImage(image = "../art/tank/treadglow.png", pos=(0,0,0))
        self.tankglow = OnscreenImage(image = "../art/tank/newtankglow.png", pos=(0,0,0))
        self.turretglow = OnscreenImage(image = "../art/tank/turretglow.png", pos=(0,0,0))
        self.wheelglow = OnscreenImage(image = "../art/tank/wheelglow.png", pos=(0,0,0))
        self.cannonglow = OnscreenImage(image = "../art/tank/cannonglow.png", pos=(0,0,0))
        self.mgglow = OnscreenImage(image = "../art/tank/gunglow.png", pos=(0,0,0))
        #self.pressenter = OnscreenText(text = "Press Enter To Continue...", pos = (0,0))
        self.player = playertank.PlayerTank(self)
        self.computer = enemytank.EnemyTank(self)
        self.playerhealth = OnscreenText(text = str(self.player.damage-1), pos = (-.4,.85), fg = (0, 211, 0, 1), mayChange = True, scale = 0.17)
        self.enemyhealth = OnscreenText(text = str(self.player.damage-1), pos = (.4,.85), fg = (0, 150, 0, 1), mayChange = True, scale = 0.17) 
        self.spashscreen = OnscreenImage(image = "startscreen.png", pos=(0,0,0),scale = (1.35,1,1))
        
        self.gameover = False
#        self.player.soundqueue.loop('idle')
#        self.player.soundqueue.loop('enemyengineidle')
        
        taskMgr.add(self.splashScreen,"spashscreenTask",uponDeath=self.startGame)
        
        self.accept("w", self.setKey, ["forward", 1])
        self.accept("s", self.setKey, ["back", 1])
        self.accept("a", self.setKey, ["left", 1])
        self.accept("d", self.setKey, ["right", 1])
        self.accept("w-up", self.setKey, ["forward", 0])
        self.accept("s-up", self.setKey, ["back", 0])
        self.accept("a-up", self.setKey, ["left", 0])
        self.accept("d-up", self.setKey, ["right", 0])
        self.accept("enter", self.setKey, ["enter", 1])
        self.accept("mouse1", self.setKey, ["fire", 1])
        self.accept("mouse1-up", self.setKey, ["fire", 0])
        self.accept("h", self.player.toggleHeadlights)
        self.accept("1", self.setWeapon,[1])
        self.accept("2", self.setWeapon,[2])
        self.accept("4", self.player.setTexture,[4])
        self.accept("5", self.player.setTexture,[5])
        self.accept("6", self.player.setTexture,[6])
        self.accept("7", self.player.setTexture,[7])
        self.accept("8", self.player.setTexture,[8])
        self.accept("y", self.computer.setenemyTexture,[4])
        self.accept("u", self.computer.setenemyTexture,[5])
        self.accept("i", self.computer.setenemyTexture,[6])
        self.accept("o", self.computer.setenemyTexture,[7])
        self.accept("p", self.computer.setenemyTexture,[8])
       
    def splashScreen(self,task): #Put title tasks in here
        if self.keyMap["enter"]:
            #self.pressenter.destroy()
            self.spashscreen.destroy()
            self.treadglow.destroy()
            self.tankglow.destroy()
            self.turretglow.destroy()
            self.wheelglow.destroy()
            self.cannonglow.destroy()
            self.mgglow.destroy()
            return Task.done
        else:
            pass
        return Task.cont
        
    def startGame(self,task): #Put game tasks in here
        self.soundqueue.unloop('menumusic')
        self.setupLights()
        self.loadModels()
        self.player.soundqueue = self.soundqueue
        self.soundqueue.loop('music')
        self.player.soundqueue.loop('idle')
        self.player.soundqueue.loop('enemyengineidle')
        taskMgr.add(self.player.movePlayer, "moveplayerTask")
        taskMgr.add(self.player.fire, "fireTask")
        taskMgr.add(self.getplayerPos, "getplayerpositionTask")
        #taskMgr.add(self.computer.moveenemyTurret, "moveenemyturretTask")
        taskMgr.add(self.computer.moveEnemy, "moveenemyTask")
        taskMgr.add(self.player.setHeadlights, "setheadlightTask")
        taskMgr.add(self.soundqueue.playqueue, "playsoundsTask")
        taskMgr.add(self.updateHud, "updatehudTask")
        taskMgr.add(self.updateCollision, "updatecollisionTask")
        taskMgr.add(self.gamestatus, "gamestatusTask")

    def gamestatus(self,task):
        #Check if player is outside arena
        xvalues = (self.player.base.getX())  #Distance formula
        yvalues = (self.player.base.getY())
        xsquared = math.pow(xvalues,2)
        ysquared = math.pow(yvalues,2)
        distance = math.sqrt(xsquared+ysquared)
        if distance>=121:
            self.gameover = True
            self.gameoverscreen = OnscreenImage(image = "../art/HUD/losescreen.png", scale = (1.34,1,1))
        
        #Check if computer is outside arena
        xvalues = (self.computer.base.getX())  #Distance formula
        yvalues = (self.computer.base.getY())
        xsquared = math.pow(xvalues,2)
        ysquared = math.pow(yvalues,2)
        distance = math.sqrt(xsquared+ysquared)
        if distance>=121:
            self.gameover = True
            self.gameoverscreen = OnscreenImage(image = "../art/HUD/winscreen.png", scale = (1.34,1,1))

        if self.gameover == True:
            taskMgr.remove("moveplayerTask")
            taskMgr.remove("fireTask")
            taskMgr.remove("getplayerpositionTask")
            taskMgr.remove("moveenemytask")
            taskMgr.remove("setheadlightTask")
            taskMgr.remove("playsoundsTask")
            taskMgr.remove("updatehudTask")
            taskMgr.remove("updatecollisionTask")
            taskMgr.remove("gamestatusTask")
            self.soundqueue.unloop('idle')
            self.soundqueue.unloop('enemyengineidle')
            self.soundqueue.unloop('engine')
    
        return Task.cont

    def updateCollision(self, task):
        base.cTrav.traverse(render)
        for i in range(self.tankGroundHandler.getNumEntries()):
            entry = self.tankGroundHandler.getEntry(i)
            if entry.getFromNode().getName() == "Player":
                tankZ = entry.getSurfacePoint(render).getZ()
                if tankZ is not self.player.base.getZ():
                    self.player.base.setPos(self.player.base.getX(), self.player.base.getY(), tankZ)
                    
            if entry.getFromNode().getName() == "Enemy":
                tankZ = entry.getSurfacePoint(render).getZ()
                if tankZ is not self.enemy.base.getZ():
                    self.enemy.base.setPos(self.enemy.base.getX(), self.enemy.base.getY(), tankZ)
        return Task.cont
        
    def updateHud(self,task):        
        self.playerhealth.setText(str(self.player.damage-1))
        self.enemyhealth.setText(str(self.computer.damage-1))   
        return Task.cont

                
    def setWeapon(self, key):
        if key == 1: #Switch image to cannon
            self.player.setcurrentWeapon(1,"cannonimage.png")
            self.hudweapon.setImage("currentWeaponCannon.png")
            self.hudweapon.setTransparency(TransparencyAttrib.MAlpha)
        if key == 2: #Switch image to machinegun
            self.player.setcurrentWeapon(2,"machinegunimage.png")   
            self.hudweapon.setImage("PlayerWeaponMachineGun.png")
            self.hudweapon.setTransparency(TransparencyAttrib.MAlpha)

    def setKey(self, key, value):
        self.keyMap[key] = value
        self.player.setkeyMap(self.keyMap)
        

    def getplayerPos(self,task):
        self.player.turret.getPos()
        playerPos = [self.player.turret.getX(),self.player.turret.getY(),self.player.turret.getZ()]
        self.computer.setplayerPos(playerPos)
        self.soundqueue.setplayerPos(playerPos, self.player.turret.getH(), [self.computer.turret.getX(),self.computer.turret.getY(),self.computer.turret.getZ()])
        return Task.cont

    def setupLights(self):
        """Loads initial lighting"""
        dirLight = DirectionalLight("dirLight")
        dirLight.setColor(Vec4(0.6, 0.6, 0.6, 1.0)) #alpha is largely irrelevent
        dirLightNP = render.attachNewNode(dirLight) #creates a NodePath and attaches it
        dirLightNP.setHpr(0, -26, 0)
        render.setLight(dirLightNP) #clearLight() turns it off

        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor(Vec4(0.25, 0.25, 0.25, 1))
        ambientLightNP = render.attachNewNode(ambientLight)
        render.setLight(ambientLightNP)

    def loadModels(self):
        """Loads models/actors into the world"""

        #load environment
        self.environment = loader.loadModel("../art/arena/arena.egg")
        self.environment.reparentTo(render)
        self.environment.setScale(4)
        
        self.floorHandler.addCollider(self.player.base.attachNewNode(CollisionNode('col')), self.player.base)
        base.cTrav.addCollider(self.player.nodePath, self.tankGroundHandler)
        base.cTrav.showCollisions(render) #just to visualize the collisions
#        self.environment.setPos(-8,42,0)


    def playerHitEnemy(self, entry):
        print "Player hit enemy"
        # uncomment the next line for debug infos
        #print entry

    def enemyHitPlayer(self, entry):
        print "Enemy hit player"
        # uncomment the next line for debug infos
        #print entry
        