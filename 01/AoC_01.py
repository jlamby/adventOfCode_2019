import sys
import os
import math

def computeFuel(mass) :
    #Fuel required to launch a given module is based on its mass. Specifically, to find the fuel required for a module, take its mass, divide by three, round down, and subtract 2.
    return math.floor( mass / 3 ) - 2

def tick(line) :
    mass = int(line)
    fuelRequired = computeFuel(mass)

    print("Mass = {}, fuel required = {}".format(mass, fuelRequired))

    return fuelRequired

filename = 'input_01.txt'
totalFuelRequirement = 0

with open(filename) as fp :    
    for line in fp :
        totalFuelRequirement += tick(line)

print("Total fuel required = {}".format(totalFuelRequirement))