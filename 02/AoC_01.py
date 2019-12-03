import sys
import os

def retrieveOpCode(ints, currentIdx) :
    opcode = ints[currentIdx]

    if (opcode == "1") :
        handleOpCode(ints, currentIdx, add)
        return 1
    elif (opcode == "2") :
        handleOpCode(ints, currentIdx, mul)
        return 1
    elif (opcode == "99") :
        return -1
    else : 
        print("OPCODE {} unknown => ignored".format(opcode))
        return 0
    
def handleOpCode(intAsStrings, currentIdx, operationFct) :
    firstTermIdx = extractValueFromArray(intAsStrings, currentIdx + 1)
    secondTermIdx = extractValueFromArray(intAsStrings, currentIdx + 2)

    firstTerm = extractValueFromArray(intAsStrings, firstTermIdx)
    secondTerm = extractValueFromArray(intAsStrings, secondTermIdx)

    result = operationFct(firstTerm, secondTerm)

    print("OP ({}) for {} @ #{} and {} @ #{} yields {}".format(operationFct, firstTerm, firstTermIdx, secondTerm, secondTermIdx, result))

    storageIdx = extractValueFromArray(intAsStrings, currentIdx + 3)

    print("Storing result ({}) to #{}".format(result, storageIdx))

    intAsStrings[storageIdx] = result

def prepare(intAsStrings) : 
    intAsStrings[1] = 12
    intAsStrings[2] = 2

def extractValueFromArray(intAsStrings, idx) : return int(intAsStrings[idx])
def add(a, b) : return a + b
def mul(a, b) : return a * b

def tick(line) :
    ints = line.split(',')

    prepare(ints)

    currentIdx = 0
    shouldContinue = True
    while shouldContinue :
        result = retrieveOpCode(ints, currentIdx)

        if (result == 1) :
            currentIdx += 4
        elif (result == 0) :
            currentIdx += 1
        else :
            shouldContinue = False

filename = 'input_01.txt'

with open(filename) as fp :    
    for line in fp :
        tick(line)

