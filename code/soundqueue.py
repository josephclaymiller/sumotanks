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
                'engine':           loader.loadSfx("../art/sounds/engine.wav"),
                'enemyengineidle':  loader.loadSfx("../art/sounds/engineidle.wav"),
                'idle':             loader.loadSfx("../art/sounds/engineidle.wav")
        }

        self.activeloops = []

        for loop in self.loops:
            self.loops[loop].setLoop(True)

        self.playerPos = [0,0,0,0]
        self.enemyPos = [0, 0, 0]
        self.bal = 1


    def enqueue(self, soundname, x, y, z):

        self.queue.append([soundname, x, y, z])

    def loop(self, soundname):

        if self.loops[soundname].status() != 2:
            self.loops[soundname].play()

    def unloop(self, soundname):

        if soundname == 'engine' and self.loops[soundname].status() == 2:
            self.sounds['engineoff'].play()    
        self.loops[soundname].stop()
        


    def setplayerPos(self,playerPosition, h, newEnemyPos):
        self.playerPos = playerPosition + [h]
        self.enemyPos = newEnemyPos


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
            self.bal *= -1
            self.sounds[sound[0]].setBalance(self.bal)
        

            self.sounds[sound[0]].play()


        for loop in self.loops:

            if loop.startswith('enemy') and self.loops[loop].status() == 2 :

                #set sound volume according to distance in x, y and z
                hdistance = math.sqrt((self.playerPos[0] - self.enemyPos[0]) ** 2 + (self.playerPos[1] - self.enemyPos[1]) ** 2)
                distance = math.sqrt(hdistance ** 2 + (self.playerPos[2] - self.enemyPos[2]) ** 2)
                vol = 1 - (distance / maxdistance)
                if vol < 0:
                    vol = 0
                self.loops[loop].setVolume(vol)

                #sets pan
                soundheading = rad2Deg(math.atan2(self.playerPos[1] - self.enemyPos[1], self.playerPos[0] - self.enemyPos[2])) + 90
                theta = soundheading - (self.playerPos[3] % 360)
                if theta > 180:
                    theta -= 360
                self.bal *= -1
                self.loops[loop].setBalance(self.bal)
        

    
        self.queue = []

        return Task.cont

