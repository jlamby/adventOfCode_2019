import sys
import os
import math
from pprint import pprint
from enum import Enum

class Compound :
    def __init__(self, name, quantity, inputs=[]) : 
        self.name = name
        self.quantity = quantity
        self.inputs = inputs
    
    def __str__(self) : return f'{self.name}*{self.quantity} = {self.inputs}'
    def __repr__(self) : return self.__str__()
    
    def isBaseElement(self) :
        #print("isBaseElement",self)
        if len(self.inputs) == 1 : 
            if self.inputs[0].name == 'ORE' :
                return True
        return False

def parseProduct(productString) : 
    product = productString.strip().split(' ')

    return Compound(product[1], int(product[0]))

def parse(line) :
    line = line.rstrip()
    parts = line.split(' => ')

    inputParts = parts[0]
    output = parseProduct(parts[1])

    inputsAsString = inputParts.split(', ')
    
    inputs = []

    for s in inputsAsString : 
        inputs.append(parseProduct(s))
    
    output.inputs = inputs
    
    return  output

def addCompoundInRequirements(requirements, compound, qty) :
    if compound.name not in requirements : 
        requirements[compound.name] = qty
    else :
        requirements[compound.name] += qty

def computeRequirements(recipes, item, qty, requirements) : 
    print("req for", qty, "x", item)
    compound = recipes[item]
    
    #print(compound)

    for input in compound.inputs : 
        element = recipes[input.name]

        if element.isBaseElement() :
            addCompoundInRequirements(requirements, element, qty * input.quantity) 
        else :
            computeRequirements(recipes, element.name, input.quantity, requirements)
    
    return requirements

def transformToOres(recipes, requirements) :
    totalOres = 0
    
    for key, value in requirements.items() :
        element = recipes[key]
        multiplier = math.ceil(value / element.quantity)

        totalOres += multiplier * element.inputs[0].quantity

    return totalOres


def tick(line, recipes) :
    result = parse(line)

    recipes[result.name] = result

def doMagic(fileName) :
    recipes = dict()

    with open(fileName) as fp :    
        for line in fp :
            tick(line, recipes)

    #pprint(recipes)
    requirements = computeRequirements(recipes, 'FUEL', 1, dict())
    #print(requirements)
    print(">>>>>>>", transformToOres(recipes, requirements))

#To produce 1 FUEL, a total of 31 ORE is required: 1 ORE to produce 1 B, 
#then 30 more ORE to produce the 7 + 7 + 7 + 7 = 28 A (with 2 extra A wasted) 
# required in the reactions to convert the B into C, C into D, D into E, 
# and finally E into FUEL. 
# (30 A is produced because its reaction requires that it is created in
#  increments of 10.)

'''
7A + 1E =>
7A + 7A + 1D =>
7A + 7A + 7A + 1C =>
7A + 7A + 7A + 7A + 1B =>
28A + 1B =>
30A + 1B =>
31 ORE
 
'''

doMagic('input_00.txt')
doMagic('input_01.txt')
doMagic('input_02.txt')
doMagic('input_03.txt')
doMagic('input_04.txt')