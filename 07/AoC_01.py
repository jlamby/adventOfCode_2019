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

        firstTerm = memory.getValue(currentIdx + 1, firstParameterMode)
        secondTerm = memory.getValue(currentIdx + 2, secondParameterMode)

        result = fct(firstTerm, secondTerm)
        memory.setValueAtIndex(currentIdx + 3, result)
        
        return currentIdx + operation.size

    @staticmethod
    def read(memory, currentIdx, operation) : 
        global xxx, previousResult, amplifierSetting

        if xxx is True :
            xxx = False
            value = amplifierSetting
        else :
            xxx = True
            value = previousResult

        print("<<< ", value)
        
        memory.setValueAtIndex(currentIdx + 1, int(value))

        return currentIdx + operation.size

    @staticmethod
    def print(memory, currentIdx, operation) : 
        opCodeAsString = str(memory.getValueAtIndex(currentIdx)).rjust(5, '0')
        firstParameterMode = int(opCodeAsString[2])

        result = memory.getValue(currentIdx + 1, firstParameterMode)

        print(">>> ", result)
        memory.result = result

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

        firstTerm = memory.getValue(currentIdx + 1, firstParameterMode)
        secondTerm = memory.getValue(currentIdx + 2, secondParameterMode)

        result = 0

        if (predicate(firstTerm, secondTerm)) :
            result = 1
        
        memory.setValueAtIndex(currentIdx + 3, result)

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
        self.values = []
        self.result = 0

        for s in values :
            self.values.append(int(s))

    def getValueAtIndex(self, idx) : return self.values[idx]
    def setValueAtIndex(self, idx, value) : self.values[self.getValueAtIndex(idx)] = value

    def getValue(self, idx, argMode) :
        #print("GET @ {} with mode {}".format(idx, argMode))

        if (argMode == 0) :
            return self.getValueAtIndex(self.values[idx])
        return self.values[idx]

def retrieveOperation(opCode) :
    realOpCode = int(opCode[-2:])

    for op in __OPERATIONS :
        if op.opCode == realOpCode : return op
    
    return NOOP        

def retrieveOpCode(memory, currentIdx) :
    opcode = memory.getValueAtIndex(currentIdx)

    opcodeAsString = str(opcode).rjust(5, '0')

    operation = retrieveOperation(opcodeAsString)
    currentIdx = operation.handleOperation(memory, currentIdx)

    return currentIdx

def tick(line) :
    memory = Memory(line.split(','))

    currentIdx = 0
    shouldContinue = True
    while shouldContinue :
        currentIdx = retrieveOpCode(memory, currentIdx)

        if (currentIdx == -1) :
            shouldContinue = False

    return memory.result

NOOP = Operation(-1, Operation.noop, 1, "NOOP")

__OPERATIONS = [
    Operation(1,    Operation.add,         4,   "ADD"),
    Operation(2,    Operation.mul,         4,   "MUL"),
    Operation(3,    Operation.read,        2,   "READ"),
    Operation(4,    Operation.print,       2,   "WRITE"),
    Operation(5,    Operation.jumpIfTrue,  3,   "JUMP-IF-TRUE"),
    Operation(6,    Operation.jumpIfFalse, 3,   "JUMP-IF-FALSE"),
    Operation(7,    Operation.lessThan,    4,   "LESS-THAN"),
    Operation(8,    Operation.equals,      4,   "EQUALS"),
    Operation(99,   Operation.halt,       -1,   "STOP")
]

filename = 'input_01.txt'
lineWithNoDiff = None

with open(filename) as fp :    
    for line in fp :
        lineWithNoDiff = line

maxResult = 0

allSettings = []

for b1 in range(0,5) :
    for b2 in range(0,5) :
        for b3 in range(0,5) :
            for b4 in range(0,5) :
                for b5 in range(0,5) :
                    setting = [b1,b2,b3,b4,b5]
                    allSettings.append(setting)

print(len(allSettings))

filteredSettings = []
for setting in allSettings :
    if len(set(setting)) == 5 :
        filteredSettings.append(setting)

print(len(filteredSettings))


for setting in filteredSettings :
    print(setting)
    previousResult = 0
    xxx = True

    for i in range(0, 5) :
        amplifierSetting = setting[i]
        previousResult = tick(lineWithNoDiff)    

        if previousResult > maxResult :
            maxResult = previousResult

print("Max = ", maxResult)