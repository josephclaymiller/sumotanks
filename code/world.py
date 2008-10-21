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
        
        self.keyMap = {"left":0, "right":0, "forward":0, "back":0, "enter":0}  

        #Make mouse invisible
        props = WindowProperties()
        props.setCursorHidden(True) 
        base.win.requestProperties(props)      

        #Sets up glow mapping based on alpha channel
        self.filters = CommonFilters(base.win, base.cam)
        filterok = self.filters.setBloom(blend=(0,0,0,1), desat= 0.0, intensity=10.0, size="small")
        self.soundqueue = soundqueue.SoundQueue()
        self.soundqueue.loop('menumusic')

        self.accept("escape", sys.exit)
        self.hud = OnscreenImage(image = "hud.png", pos=(0,0,.85),scale = (1.35,0,.157))
        self.treadglow = OnscreenImage(image = "../art/tank/treadglow.png", pos=(0,0,0))
        self.tankglow = OnscreenImage(image = "../art/tank/newtankglow.png", pos=(0,0,0))
        #self.turretglow = OnscreenImage(image = "../art/tank/turretglow.png", pos=(0,0,0))
        self.wheelglow = OnscreenImage(image = "../art/tank/wheelglow.png", pos=(0,0,0))
        self.cannonglow = OnscreenImage(image = "../art/tank/cannonglow.png", pos=(0,0,0))
        self.mgglow = OnscreenImage(image = "../art/tank/gunglow.png", pos=(0,0,0))
        #self.pressenter = OnscreenText(text = "Press Enter To Continue...", pos = (0,0))
        self.player = playertank.PlayerTank()
        self.computer = enemytank.EnemyTank()
        self.playerhealth = OnscreenText(text = str(self.player.damage-1), pos = (-.5,.8), fg = (255, 255, 255, 1), mayChange = True, scale = 0.2)
        self.enemyhealth = OnscreenText(text = str(self.player.damage-1), pos = (.5,.8), fg = (255, 255, 255, 1), mayChange = True, scale = 0.2) 
        self.spashscreen = OnscreenImage(image = "summotankstitlescreen.png", pos=(0,0,0),scale = (1.35,1,1))
        
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
        self.accept("mouse1", self.setKey, ["mouse1", 1])
        self.accept("mouse2", self.setKey, ["mouse2", 1])
       
    def splashScreen(self,task): #Put title tasks in here
        if self.keyMap["enter"]:
            #self.pressenter.destroy()
            self.spashscreen.destroy()
            self.treadglow.destroy()
            self.tankglow.destroy()
            #self.turretglow.destroy()
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
        

    def updateHud(self,task):
        self.player.damage +=1
        self.playerhealth.setText(str(self.player.damage-1))
        self.enemyhealth.setText(str(self.computer.damage-1))   
        return Task.cont

                
    def setWeapon(self, key):
        if key == 1: #Switch image to cannon
            self.player.setcurrentWeapon(1,"cannonimage.png")
        if key == 2: #Switch image to machinegun
            self.player.setcurrentWeapon(2,"machinegunimage.png")   

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
        self.environment = loader.loadModel("../art/arena/arena1.egg")
        self.environment.reparentTo(render)
        self.environment.setScale(4)
#        self.environment.setPos(-8,42,0)
