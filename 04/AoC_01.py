import sys
import os
from collections import OrderedDict

def isValidNumber(candidate) :
    numberAsString = str(candidate)

    adjacentDigitRuleResult = adjacentDigitRule(numberAsString)
    increaseDigitOnlyResult = increaseDigitOnly(numberAsString)
    pairRuleResult = pairRule(numberAsString)

    return adjacentDigitRuleResult and increaseDigitOnlyResult and pairRuleResult

def adjacentDigitRule(numberAsString) :
    
    for i in range(0, 5) :
        substr = numberAsString[i:i+2]
        
        if (substr[0] == substr[1]) :
            return True

    return False

def increaseDigitOnly(numberAsString) :
    
    for i in range(0, 5) :
        substr = numberAsString[i:i+2]
        
        if (substr[0] > substr[1]) :
            return False

    return True

def pairRule(numberAsString) :
    allChars = list(numberAsString)
    res = [(el, allChars.count(el)) for el in allChars] 
    
    res = (list(OrderedDict(res).items()))

    for item in res :
        if (item[1] == 2) : return True

    return False

validNumbers = []

for number in range(272091, 815432) :
    result = isValidNumber(number)

    if (result) : 
        validNumbers.append(number)

print(len(validNumbers))