#entity - a physics controlled object in the game world

import sys, math

from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject

class force():
    def __init__(self, magnitude, angle):
        self.magnitude = magnitude
        self.angle = angle

    def xcomp(self):
        return self.magnitude * math.cos(self.angle)

    def ycomp(self): 
        return self.magnitude * math.sin(self.angle)

    def add(self, other):
        x = self.xcomp() + other.xcomp()
        y = self.ycomp() + other.ycomp()

        angle = math.atan2(y,x)
        magnitude = math.sqrt(math.pow(x,2) + math.pow(y,2))

        return force(magnitude, angle)

class entity(DirectObject):
    def __init__(self, mass):
        self.move = force(0,0)
        self.mass = mass
        self.acc = force(0,0)
        self.vel = force(0,0)

    def update(self):
        """Calculates kinetic friction and drag, applies it, calculates 
        new acc, then new vel"""
        frictAngle = self.vel.angle
        if self.vel.magnitude != 0:
            frictMagnitude = -((4.5 * self.mass * 0.05) + ((1/(2.0))*1.3*math.pow(self.vel.magnitude,2)))
        else:
            frictMagnitude = 0
        friction = force(frictMagnitude, frictAngle)

        forces = self.move.add(friction)
        self.acc = forces
        self.acc.magnitude = self.acc.magnitude/(self.mass+0.0)

        self.vel = self.vel.add(self.acc)
        if self.vel.magnitude < 0.1 and self.move.magnitude >= 0:
            self.vel.magnitude = 0

