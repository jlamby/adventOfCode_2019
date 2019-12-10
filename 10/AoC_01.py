import sys
import os

class Spot : 
    def __init__(self, x, y) :
        self.x = x
        self.y = y

    def __eq__(self, other):
      return other and self.x == other.x and self.y == other.y

    def __hash__(self):
      return hash((self.x, self.y))

    def __str__(self) : return f'@({self.x},{self.y})'

def retrieveItemAtCoord(x, y) :
    #print("Getting item @", x, ",", y)

    global spaceMap, width, height

    if x < 0 or x >= width :
        #print("Bad value for x, ignored")
        return False

    if y < 0 or y >= height :
        #print("Bad value for y, ignored")
        return False

    value = spaceMap[y][x]

    if value == '#' :
        return True
    
    return False

def isOnStraightLine(deltaX, deltaY) : 
    if deltaX == 0 or deltaY == 0 : 
        return True
    return False

def isDiagonal(deltaX, deltaY) :
    if abs(deltaX) == abs(deltaY) : 
        return True
    return False

def retrieveOneAndKeepSign(value) : 
    if value < 0 :
        return -1
    return 1

def computeLineOfSight(startX, startY, asteroidX, asteroidY) :
    global height, width

    deltaX = startX - asteroidX
    deltaY = startY - asteroidY

    if isDiagonal(deltaX, deltaY) : 
        deltaX = retrieveOneAndKeepSign(deltaX)
        deltaY = retrieveOneAndKeepSign(deltaY)

    if isOnStraightLine(deltaX, deltaY) :
        if deltaX == 0 :
            deltaY = retrieveOneAndKeepSign(deltaY)
        else :
            deltaX = retrieveOneAndKeepSign(deltaX)

    #print(deltaX, deltaY)

    hiddenSpots = []

    for i in range(0, max(height,width)) : 
        hiddenSpotX = asteroidX - i * deltaX
        hiddenSpotY = asteroidY - i * deltaY

        hiddenSpots.append(Spot(hiddenSpotX, hiddenSpotY))

    return hiddenSpots

def ifAsteroidHidden(hiddenSpots, asteroidX, asteroidY) :
    tmpSpot = Spot(asteroidX, asteroidY)

    if tmpSpot in hiddenSpots : return True

    return False

def detectAsteroids(startX, startY, depth, hiddenSpots) :
    detectedAsteroids = 0 

    bounds = depth + 1

    for modX in range(-bounds, bounds+1) :
        for modY in range(-bounds, bounds+1) :
            x = modX
            y = modY

            #print(x,y)

            if (x != 0 or y != 0) :
                isAsteroid = retrieveItemAtCoord(startX + x, startY + y)

                if isAsteroid :
                    asteroidX = startX + x
                    asteroidY = startY + y

                    #print("Found asteroid @", asteroidX, asteroidY)
                    if ifAsteroidHidden(hiddenSpots, asteroidX, asteroidY) == False :
                        #if startX == 11 and startY == 13 : 
                        #    print("Asteroid @", asteroidX, asteroidY, "is visible")

                        hiddenSpotsToAdd = computeLineOfSight(startX, startY, asteroidX, asteroidY)
                        hiddenSpots.update(hiddenSpotsToAdd)

                        detectedAsteroids += 1
                    #else : 
                        #print("Asteroid @", asteroidX, asteroidY, "is hidden")
    return detectedAsteroids

def dumpHiddenSpots(hiddenSpots) :
    global height, width

    print(len(hiddenSpots))

    for h in range(0, height) :
        line = ''
        for w in range(0, width) : 
            spot = Spot(w, h)

            if spot in hiddenSpots : 
                line += str('@')
            else : 
                line += str('-')
        print(line)

def tick(line) :
    print(line)

filename = 'input_04.txt'

spaceMap = []

width = 0
height = 0

with open(filename) as fp :    
    for line in fp :
        lineAsList = list(line.rstrip())
        spaceMap.append(lineAsList)

        height += 1
        width = len(lineAsList)

print(spaceMap)

#print(computeLineOfSight(1,0,3,2))

#quit()

from datetime import datetime
print("Start", datetime.now())

maxAsteroids = 0
monitoringStation = None
'''
for h in range(0, height) :
    for w in range(0, width) : 
'''
for h in range(13, 14) :
    for w in range(11, 12) :
        
        if retrieveItemAtCoord(w, h) :
            #print("On asteroid @", w, h)
            depth = 0
            hiddenSpots = set()
            detectedAsteroids = 0

            while depth < max(height, width) :
                #print("Scan for depth", depth)
                detectedAsteroids += detectAsteroids(w, h, depth, hiddenSpots)
                depth += 1

            dumpHiddenSpots(hiddenSpots)

            #print(">>", detectedAsteroids)

            if (detectedAsteroids > maxAsteroids) :
                maxAsteroids = detectedAsteroids
                monitoringStation = Spot(w, h)

print("End", datetime.now())

print(">>>", monitoringStation)
print(">>>", maxAsteroids)
'''
depth = 0
hiddenSpots = []
detectedAsteroids = 0

while depth < max(height, width) :
    print("Scan for depth", depth)
    detectedAsteroids += detectAsteroids(3, 4, depth, hiddenSpots)
    depth += 1

print(">>>", detectedAsteroids)
'''