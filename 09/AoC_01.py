import sys
import os

class Operation : 
    
    def __init__(self, opCode, handleFunction, size, name) :
        self.opCode = opCode
        self.handleFunction = handleFunction
        self.size = size
        self.name = name

    def handleOperation(self, memory, currentIdx) :
        return self.handleFunction(memory, currentIdx, self)
    
    def __str__(self) :
        return self.name

    @staticmethod
    def add(memory, currentIdx, operation) : 
        return Operation.__operation(memory, currentIdx, operation, lambda x,y : x + y)

    @staticmethod
    def mul(memory, currentIdx, operation) :
        return Operation.__operation(memory, currentIdx, operation, lambda x,y : x * y)

    @staticmethod
    def __operation(memory, currentIdx, operation, fct) :
        opCodeAsString = str(memory.getValueAtIndex(currentIdx)).rjust(5, '0')

        firstParameterMode = int(opCodeAsString[2])
        secondParameterMode = int(opCodeAsString[1])
        thirdParameterMode = int(opCodeAsString[0])

        firstTerm = memory.getValue(currentIdx + 1, firstParameterMode)
        secondTerm = memory.getValue(currentIdx + 2, secondParameterMode)

        result = fct(firstTerm, secondTerm)
        memory.setValue(currentIdx + 3, thirdParameterMode, result)
        
        return currentIdx + operation.size

    @staticmethod
    def read(memory, currentIdx, operation) : 
        value = input("Please enter an ID:\n<<< ")

        opCodeAsString = str(memory.getValueAtIndex(currentIdx)).rjust(5, '0')

        firstParameterMode = int(opCodeAsString[2])

        memory.setValue(currentIdx + 1, firstParameterMode, int(value))

        return currentIdx + operation.size

    @staticmethod
    def print(memory, currentIdx, operation) : 
        opCodeAsString = str(memory.getValueAtIndex(currentIdx)).rjust(5, '0')
        firstParameterMode = int(opCodeAsString[2])

        print(">>> ", memory.getValue(currentIdx + 1, firstParameterMode))

        return currentIdx + operation.size

    @staticmethod
    def jumpIfTrue(memory, currentIdx, operation) : 
        return Operation.__jumpIf(memory, currentIdx, operation, lambda x : x != 0)
    
    @staticmethod
    def jumpIfFalse(memory, currentIdx, operation) : 
        return Operation.__jumpIf(memory, currentIdx, operation, lambda x : x == 0)

    @staticmethod
    def __jumpIf(memory, currentIdx, operation, predicate) :
        opCodeAsString = str(memory.getValueAtIndex(currentIdx)).rjust(5, '0')        
    
        firstParameterMode = int(opCodeAsString[2])
        secondParameterMode = int(opCodeAsString[1])

        result = memory.getValue(currentIdx + 1, firstParameterMode)

        if (predicate(result)) :
            currentIdx = memory.getValue(currentIdx + 2, secondParameterMode)
        else :
            currentIdx = currentIdx + operation.size

        return currentIdx

    @staticmethod
    def lessThan(memory, currentIdx, operation) :   
        return Operation.__condition(memory, currentIdx, operation, lambda x,y : x < y)

    @staticmethod
    def equals(memory, currentIdx, operation) : 
        return Operation.__condition(memory, currentIdx, operation, lambda x,y : x == y)

    @staticmethod
    def __condition(memory, currentIdx, operation, predicate) :
        opCodeAsString = str(memory.getValueAtIndex(currentIdx)).rjust(5, '0')        
        firstParameterMode = int(opCodeAsString[2])
        secondParameterMode = int(opCodeAsString[1])
        thirdParameterMode = int(opCodeAsString[0])

        firstTerm = memory.getValue(currentIdx + 1, firstParameterMode)
        secondTerm = memory.getValue(currentIdx + 2, secondParameterMode)

        result = 0

        if (predicate(firstTerm, secondTerm)) :
            result = 1
        
        memory.setValue(currentIdx + 3, thirdParameterMode, result)

        return currentIdx + operation.size

    @staticmethod
    def adjustBase(memory, currentIdx, operation) :
        opCodeAsString = str(memory.getValueAtIndex(currentIdx)).rjust(5, '0')        
        firstParameterMode = int(opCodeAsString[2])

        #print("!!!B", memory.getRelativeBase())

        firstTerm = memory.getValue(currentIdx + 1, firstParameterMode)

        #print("!!!", currentIdx+1, opCodeAsString, memory.getValueAtIndex(currentIdx+1), firstTerm)

        memory.addToRelativeBase(firstTerm)

        #print("!!!A", memory.getRelativeBase())

        return currentIdx + operation.size

    @staticmethod
    def halt(memory, currentIdx, operation) : 
        print("Program halted")
        return -1

    @staticmethod
    def noop(memory, currentIdx, operation) : 
        print("OPCODE {} unknown => ignored".format(operation.name))
        return currentIdx + operation.size

class Memory :
    
    def __init__(self, values) :
        self.__values = [0] * 99999999
        self.__result = 0
        self.__relativeBase = 0

        i = 0
        for s in values :
            self.__values[i]= int(s)
            i += 1

    def getValueAtIndex(self, idx) : return self.__values[idx]
    def setValueAtIndex(self, idx, value) : return self.setValue(idx, 0, value)

    def setValue(self, idx, argMode, value) :
        valueAtIdx = self.__values[idx]

        #print("SET {} @ {} with mode {} => {}".format(value, idx, argMode, valueAtIdx))

        if argMode == 0 :
            self.__values[valueAtIdx] = value
        else :
            self.__values[self.__relativeBase + valueAtIdx] = value

    def getValue(self, idx, argMode) :
        valueAtIdx = self.__values[idx]

        #print("GET @ {} with mode {} => {}".format(idx, argMode, valueAtIdx))

        if (argMode == 1) :
            return valueAtIdx
        elif (argMode == 0) :
            return self.getValueAtIndex(valueAtIdx)
                
        return self.getValueAtIndex(self.__relativeBase + valueAtIdx)
    
    def setResult(self, value) : self.__result = value
    def getResult(self) : return self.__result

    def setRelativeBase(self, newValue) : self.__relativeBase = newValue
    def addToRelativeBase(self, valueToAdd) : self.__relativeBase += valueToAdd
    def getRelativeBase(self) : return self.__relativeBase

def retrieveOperation(opCode) :
    realOpCode = int(opCode[-2:])

    for op in __OPERATIONS :
        if op.opCode == realOpCode : return op
    
    return NOOP        

def retrieveOpCode(memory, currentIdx) :
    opcode = memory.getValueAtIndex(currentIdx)

    opcodeAsString = str(opcode).rjust(5, '0')

    operation = retrieveOperation(opcodeAsString)
    #print(opcodeAsString, operation.name)
    currentIdx = operation.handleOperation(memory, currentIdx)

    return currentIdx

import collections

def tick(line) :
    memory = Memory(line.split(','))

    currentIdx = 0
    shouldContinue = True

    while shouldContinue :
        currentIdx = retrieveOpCode(memory, currentIdx)

        if (currentIdx == -1) :
            shouldContinue = False

NOOP = Operation(-1, Operation.noop, 1, "NOOP")

__OPERATIONS = [
    Operation(1, Operation.add, 4, "ADD"),
    Operation(2, Operation.mul, 4, "MUL"),
    Operation(3, Operation.read, 2, "READ"),
    Operation(4, Operation.print, 2, "WRITE"),
    Operation(5, Operation.jumpIfTrue, 3, "JUMP-IF-TRUE"),
    Operation(6, Operation.jumpIfFalse, 3, "JUMP-IF-FALSE"),
    Operation(7, Operation.lessThan, 4, "LESS-THAN"),
    Operation(8, Operation.equals, 4, "EQUALS"),
    Operation(9, Operation.adjustBase, 2, "ADJUST-RBASE"),
    Operation(99, Operation.halt, -1, "STOP")
]

filename = 'input_01.txt'
lineWithNoDiff = None

with open(filename) as fp :    
    for line in fp :
        lineWithNoDiff = line

tick(lineWithNoDiff)