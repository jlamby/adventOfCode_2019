import sys
import os

class Operation : 
    
    def __init__(self, opCode, handleFunction, size, name) :
        self.opCode = opCode
        self.handleFunction = handleFunction
        self.size = size
        self.name = name

    def handleOperation(self, memory, currentIdx) :
        self.handleFunction(memory, currentIdx)
    
    def __str__(self) :
        return self.name

    @staticmethod
    def add(memory, currentIdx) : return Operation.__bifunction(memory, currentIdx, Operation.__addFct)

    @staticmethod
    def mul(memory, currentIdx) : return Operation.__bifunction(memory, currentIdx, Operation.__mulFct)

    @staticmethod
    def sav(memory, currentIdx) : 
        value = input("Please enter an ID:\n")
        #print("OP ({}) for {} and {} yields {} @ {}".format(fct, firstTerm, secondTerm, result, currentIdx + 3))

        memory.setValueAtIndex(currentIdx + 1, int(value))

    @staticmethod
    def prt(memory, currentIdx) : 
        opCodeAsString = str(memory.getValueAtIndex(currentIdx)).rjust(5, '0')
        firstParameterMode = int(opCodeAsString[2])

        print(memory.getValue(currentIdx + 1, firstParameterMode))

    @staticmethod
    def halt(memory, currentIdx) : print("Program halted")

    @staticmethod
    def noop(memory, currentIdx) : print("OPCODE {} unknown => ignored".format('a'))

    @staticmethod
    def __addFct(a, b) : return a + b

    @staticmethod
    def __mulFct(a, b) : return a * b

    @staticmethod
    def __bifunction(memory, currentIdx, fct) :
        opCodeAsString = str(memory.getValueAtIndex(currentIdx)).rjust(5, '0')

        firstParameterMode = int(opCodeAsString[2])
        secondParameterMode = int(opCodeAsString[1])

        firstTerm = memory.getValue(currentIdx + 1, firstParameterMode)
        secondTerm = memory.getValue(currentIdx + 2, secondParameterMode)

        result = fct(firstTerm, secondTerm)

        #print("OP ({}) for {} and {} yields {} @ {}".format(fct, firstTerm, secondTerm, result, currentIdx + 3))

        memory.setValueAtIndex(currentIdx + 3, result)

ADD = Operation(1, Operation.add, 4, "ADD")
MUL = Operation(2, Operation.mul, 4, "MUL")
INP = Operation(3, Operation.sav, 2, "SAVE")
OUT = Operation(4, Operation.prt, 2, "DISPLAY")
STP = Operation(99, Operation.halt, -1, "STOP")
NOOP= Operation(-1, Operation.noop, 1, "NOOP")

__OPERATIONS = [
    ADD,
    MUL,
    STP,
    INP,
    OUT
]

def retrieveOperation(opCode) :
    realOpCode = int(opCode[-2:])

    for op in __OPERATIONS :
        if op.opCode == realOpCode : return op
    
    return NOOP

class Memory :
    
    def __init__(self, values) :
        self.values = []

        for s in values :
            self.values.append(int(s))

    def getValueAtIndex(self, idx) : return self.values[idx]
    def setValueAtIndex(self, idx, value) : self.values[self.getValueAtIndex(idx)] = value

    def getValue(self, idx, argMode) :
        if (argMode == 0) :
            return self.getValueAtIndex(self.values[idx])
        return self.values[idx]
        

def retrieveOpCode(memory, currentIdx) :
    opcode = memory.getValueAtIndex(currentIdx)

    opcodeAsString = str(opcode).rjust(5, '0')

    operation = retrieveOperation(opcodeAsString)
    operation.handleOperation(memory, currentIdx)

    return operation.size

def prepare(memory, nounAsInt, verbAsInt) : 
    print("Starting compute for noun = {} and verb = {}".format(nounAsInt, verbAsInt))

    memory.setValueAtIndex(1, nounAsInt)
    memory.setValueAtIndex(2, verbAsInt)

def tick(line) :
    memory = Memory(line.split(','))

    #prepare(memory, nounAsInt, verbAsInt)

    currentIdx = 0
    shouldContinue = True
    while shouldContinue :
        result = retrieveOpCode(memory, currentIdx)

        if (result == -1) :
            shouldContinue = False
        else :
            currentIdx += result
    
    print(memory.getValueAtIndex(4))

filename = 'input_01.txt'
lineWithNoDiff = None

with open(filename) as fp :    
    for line in fp :
        lineWithNoDiff = line

tick(lineWithNoDiff)