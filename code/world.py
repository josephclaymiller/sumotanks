import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
import playertank, enemytank
from pandac.PandaModules import *
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import *
from direct.task import Task
from direct.filter.CommonFilters import CommonFilters
import sys, math

class World(DirectObject):
    def __init__(self):
        #pass
        self.keyMap = {"left":0, "right":0, "forward":0, "back":0}        

        #Sets up glow mapping based on alpha channel
        self.filters = CommonFilters(base.win, base.cam)
        filterok = self.filters.setBloom(blend=(0,0,0,1), desat= 0.0, intensity=10.0, size="small")

        self.setupLights()
        self.loadModels()
        self.accept("escape", sys.exit)
        self.player = playertank.PlayerTank()
        self.computer = enemytank.EnemyTank()
        taskMgr.add(self.player.moveplayerTurret, "moveplayerturretTask")
        taskMgr.add(self.player.moveplayerBase, "moveplayerbaseTask")
        taskMgr.add(self.getplayerPos, "getplayerpositionTask")
        taskMgr.add(self.computer.moveenemyTurret, "moveenemyturretTask")
        taskMgr.add(self.player.setHeadlights, "setheadlightTask")
        
        self.accept("w", self.setKey, ["forward", 1])
        self.accept("s", self.setKey, ["back", 1])
        self.accept("a", self.setKey, ["left", 1]) 
        self.accept("d", self.setKey, ["right", 1]) 
        self.accept("w-up", self.setKey, ["forward", 0])
        self.accept("s-up", self.setKey, ["back", 0]) 
        self.accept("a-up", self.setKey, ["left", 0]) 
        self.accept("d-up", self.setKey, ["right", 0]) 
        self.accept("h", self.player.toggleHeadlights)
        
     
    def setKey(self, key, value):
        self.keyMap[key] = value
        self.player.setkeyMap(self.keyMap)
        

    def getplayerPos(self,task):
        self.player.turret.getPos()
        playerPos = [self.player.turret.getX(),self.player.turret.getY(),self.player.turret.getZ()]
        self.computer.setplayerPos(playerPos)
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
        self.environment = loader.loadModel("models/environment")
        self.environment.reparentTo(render)
        self.environment.setScale(0.25)
        self.environment.setPos(-8,42,0)
