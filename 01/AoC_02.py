import sys
import os
import math

def computeFuel(mass) :
    
    #Fuel required to launch a given module is based on its mass. Specifically, to find the fuel required for a module, 
    # take its mass, divide by three, round down, and subtract 2.
    
    #Fuel itself requires fuel just like a module - take its mass, divide by three, round down, and subtract 2. 
    # However, that fuel also requires fuel, and that fuel requires fuel, and so on. Any mass that would require negative fuel 
    # should instead be treated as if it requires zero fuel;

    fuel = math.floor( mass / 3 ) - 2

    if (fuel > 0) :
        return fuel + computeFuel(fuel)
        
    return 0

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