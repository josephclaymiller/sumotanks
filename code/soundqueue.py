import direct.directbase.DirectStart
from pandac.PandaModules import *
import math
from direct.task import Task
import world

maxdistance = 500


class SoundQueue():

    def __init__(self):
        self.queue = []

        self.sounds = {
                'boom':         loader.loadSfx("../art/sounds/long_boom.wav"),
                'bang':         loader.loadSfx("../art/sounds/bang.wav"),
                'engineoff':    loader.loadSfx("../art/sounds/engineoff.wav")
            }

        self.loops = {
                'engine':   [loader.loadSfx("../art/sounds/engine.wav"), [], [], []],
                'idle':     [loader.loadSfx("../art/sounds/engineidle.wav"), [], [], []]
        }

        for loop in self.loops:
            self.loops[loop][0].setLoop(True)

        self.playerPos = [0,0,0,0]
        self.bal = 1


    def enqueue(self, soundname, x, y, z):

        self.queue.append([soundname, x, y, z])

    def loop(self, soundname, x, y, z):

        if self.loops[soundname][0].status() != 2:
            self.loops[soundname][0].play()

    def unloop(self, soundname):

        if soundname == 'engine' and self.loops[soundname][0].status() == 2:
            self.sounds['engineoff'].play()    
        self.loops[soundname][0].stop()
        


    def setplayerPos(self,playerPosition, h):
        self.playerPos = playerPosition + [h]


    def playqueue(self, task):

        for sound in self.queue:

            #set sound volume according to distance in x, y and z
            hdistance = math.sqrt((self.playerPos[0] - sound[1]) ** 2 + (self.playerPos[1] - sound[2]) ** 2)
            distance = math.sqrt(hdistance ** 2 + (self.playerPos[2] - sound[3]) ** 2)
            vol = 1 - (distance / maxdistance)
            if vol < 0:
                vol = 0
            self.sounds[sound[0]].setVolume(vol)
    
            #sets pan
            soundheading = rad2Deg(math.atan2(self.playerPos[1] - sound[2], self.playerPos[0] - sound[1])) + 90
            theta = soundheading - (self.playerPos[3] % 360)
            if theta > 180:
                theta -= 360
            print math.sin(deg2Rad(theta) * -1)
            self.bal *= -1
            self.sounds[sound[0]].setBalance(self.bal)   #math.sin(deg2Rad(theta) * -1))
        

            self.sounds[sound[0]].play()

    
        self.queue = []

        return Task.cont

