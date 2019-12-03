import sys
import os

class Position :

    def __init__(self, x = 0, y = 0, deltaX = 0, deltaY = 0) :
        self.x = x + deltaX
        self.y = y + deltaY
    
    @classmethod
    def fromPosition(cls, otherPosition) :
        return cls(otherPosition.x, otherPosition.y)

    @classmethod
    def fromPositionWithDelta(cls, otherPosition, deltaX = 0, deltaY = 0) :
        return cls(otherPosition.x, otherPosition.y, deltaX, deltaY) 

    def __repr__(self) :
        return f'@({self.x},{self.y})'

    def __eq__(self, other) :
        return self.x == other.x and self.y == other.y

    def __hash__(self) :   
      return hash((self.x, self.y))

    def distanceTo(self, otherPosition) :
        return abs(self.x - otherPosition.x) + abs(self.y - otherPosition.y)

def convertItemToStep(item, currentPosition) :
    op = item[0]
    count = int(item[1:])

    computedOperations = []

    if (op == 'U') :
        computedOperations.extend(handleOp(up, currentPosition, count))
    elif (op == 'D') :
        computedOperations.extend(handleOp(down, currentPosition, count))
    elif (op == 'L') :
        computedOperations.extend(handleOp(left, currentPosition, count))
    elif (op == 'R') :
        computedOperations.extend(handleOp(right, currentPosition, count))
    else:
        print("ignored op ({})".format(op))
    
    return computedOperations

def handleOp(opFct, currentPosition, count) : return opFct(currentPosition, count)

def up(currentPosition, count) : return computeOperations(currentPosition, "UP", count, 1, 0)
def down(currentPosition, count) : return computeOperations(currentPosition, "DOWN", count, -1, 0)
def left(currentPosition, count) : return computeOperations(currentPosition, "LEFT", count, 0, -1)
def right(currentPosition, count) : return computeOperations(currentPosition, "RIGHT", count, 0, 1)

def computeOperations(startingPos, opName, count, deltaX, deltaY) :
    print("{} for {} steps".format(opName, count))

    currentPos = Position.fromPosition(startingPos)
    i = 0
    newPositions = []
    while (i < count)  :
        currentPos = Position.fromPositionWithDelta(currentPos, deltaX, deltaY)
        newPositions.append(currentPos)
        i+=1

    return newPositions

def tick(line) :
    ops = line.split(',')

    allPositions = []
    currentPosition = Position()

    for item in ops :
        allPositions.extend(convertItemToStep(item, currentPosition))
        currentPosition = allPositions[-1]

    print("End of move {}".format(currentPosition))
    return allPositions

def findIntersections(allPosByLine) :
    firstCablePositions = allPosByLine[0]
    secondCablePositions= allPosByLine[1]

    #intersections = [value for value in firstCablePositions if value in secondCablePositions]

    intersections = set(firstCablePositions).intersection(secondCablePositions)

    return intersections

def computeDistance(pointA, pointB) :
    return pointA.distanceTo(pointB)

def computeStepsToPoint(allPositions, point) :
    i = 0

    while (i < len(allPositions)) : 
        if (allPositions[i] == point) :
            return i + 1
        i += 1

filename = 'input_03.txt'

allPosByLine = []

with open(filename) as fp :    
    for line in fp :
        allPosByLine.append(tick(line))

intersections = findIntersections(allPosByLine)

startPos = Position()

closestIntersection = None
minSteps = sys.maxsize

for intersection in intersections :

    totalSteps = computeStepsToPoint(allPosByLine[0], intersection) + computeStepsToPoint(allPosByLine[1], intersection)
    
    if (totalSteps < minSteps) :
        minSteps = totalSteps
        closestIntersection = intersection
    

print("Closest intersection is {} with {} steps".format(closestIntersection, minSteps))

distance = computeDistance(startPos, closestIntersection)
print("Distance between {} and {} is equal to {}".format(startPos, intersection, distance))
