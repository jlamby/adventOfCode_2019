import sys
import os
from pprint import pprint
from enum import Enum

class Moon :
    def __init__(self, x, y, z, vx=0, vy=0, vz=0) : 
        self.x = x
        self.y = y
        self.z = z

        self.vx = vx
        self.vy = vy
        self.vz = vz
    
    def __str__(self) : return f'Moon @({self.x},{self.y},{self.z}) / Velocity={self.vx} / {self.vy} / {self.vz}'
    def __repr__(self) : return self.__str__()

    def computePotentialEnergy(self) : return abs(self.x) + abs(self.y) + abs(self.z)
    def computeKineticEnergy(self) : return abs(self.vx) + abs(self.vy) + abs(self.vz)
    def computeTotalEnergy(self) : return self.computePotentialEnergy() * self.computeKineticEnergy()

    def computeGravity(self, otherMoon) :        
        if self.x != otherMoon.x :
            if self.x < otherMoon.x :
                self.vx += 1
                otherMoon.vx += -1
            else :
                self.vx += -1
                otherMoon.vx += 1
        
        if self.y != otherMoon.y :
            if self.y < otherMoon.y :
                self.vy += 1
                otherMoon.vy += -1
            else :
                self.vy += -1
                otherMoon.vy += 1
        
        if self.z != otherMoon.z :
            if self.z < otherMoon.z :
                self.vz += 1
                otherMoon.vz += -1
            else :
                self.vz += -1
                otherMoon.vz += 1
    
    def updatePosition(self) :
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz

def computeGravity(moon1, moon2, moon3, moon4) :
    moon1.computeGravity(moon2)
    moon1.computeGravity(moon3)
    moon1.computeGravity(moon4)
    moon2.computeGravity(moon3)
    moon2.computeGravity(moon4)
    moon3.computeGravity(moon4)

def updatePositions(moon1, moon2, moon3, moon4):
    moon1.updatePosition()
    moon2.updatePosition()
    moon3.updatePosition()
    moon4.updatePosition()

def tick(moons) :
    moon1 = moons[0]
    moon2 = moons[1]
    moon3 = moons[2]
    moon4 = moons[3]

    computeGravity(moon1, moon2, moon3, moon4)
    updatePositions(moon1, moon2, moon3, moon4)

def decodeMoon(line) :
    datas = line.rstrip()[1:-1].split(', ')
    print(datas)
    x = int(datas[0].split('=')[1])
    y = int(datas[1].split('=')[1])
    z = int(datas[2].split('=')[1])

    return Moon(x,y,z)

filename = 'input_02.txt'
moons = list()

with open(filename) as fp :    
    for line in fp :
        moons.append(decodeMoon(line))

steps = int(input("Simulate for :\n<<<"))
pprint(moons)

for i in range (0, steps) :
    tick(moons)

pprint(moons)

print(sum(list(map(lambda moon: moon.computeTotalEnergy(), moons))))
