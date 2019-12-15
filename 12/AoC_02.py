import sys
import os
import copy
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
    def __eq__(self, other) : 
        return self.x == other.x and self.y == other.y and self.z == other.z \
            and self.vx == other.vx and self.vy == other.vy and self.vz == other.vz

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

def hasDoneARevolution(moonsInitialPosition, moonsCurrentPosition) :
    return moonsInitialPosition[0] == moonsCurrentPosition[0] and \
        moonsInitialPosition[1] == moonsCurrentPosition[1] and \
        moonsInitialPosition[2] == moonsCurrentPosition[2] and \
        moonsInitialPosition[3] == moonsCurrentPosition[3]

def gcd(a, b):
    while b > 0:
        a, b = b, a % b
    return a

def lcm(a, b):
    return (a * b) // gcd(a, b)

def getAxisValueById(moon, axisId) :
    if axisId == 0 : return moon.x
    if axisId == 1 : return moon.y
    if axisId == 2 : return moon.z

def getVelocityValueById(moon, axisId) :
    if axisId == 0 : return moon.vx
    if axisId == 1 : return moon.vy
    if axisId == 2 : return moon.vz

filename = 'input_02.txt'
moons = list()
with open(filename) as fp :    
    for line in fp :
        moons.append(decodeMoon(line))

pprint(moons)
periods = [0, 0, 0]

for i in range(3):
    print("Iter#", i)
    rptCounter = 0
    seen = set()

    while True :
        tick(moons)

        state = []
        for moon in moons :
            state.append(getAxisValueById(moon, i))
            state.append(getVelocityValueById(moon, i))
        
        state = str(state)
        
        if state in seen:
            print("Seen:", state)
            periods[i] = rptCounter
            break

        seen.add(state)
        rptCounter += 1

print(periods)
print(lcm(lcm(periods[0], periods[1]), periods[2]))