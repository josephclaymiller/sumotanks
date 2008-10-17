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
                'boom': loader.loadSfx("../art/long_boom.wav"),
                'bang': loader.loadSfx("../art/bang.wav"),
            }
        self.playerPos = [0,0,0,0]
        self.bal = 1


    def enqueue(self, soundname, x, y, z):

        self.queue.append([soundname, x, y, z])

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

'''
self.thing.getH()


        dx = self.playerPos[0]-xposition
        dy = self.playerPos[1]-yposition

heading = rad2Deg(math.atan2(dy, dx)) + 90
        heading = heading+90'''
