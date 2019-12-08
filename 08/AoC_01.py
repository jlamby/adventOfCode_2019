import sys
import os

class Layer :

    def __init__(self, width, height, lines) :
        self.width = width
        self.height = height
        self.lines = lines

    def __str__(self) :
        return f'Layer[{self.width}*{self.height}]\n\t{self.lines}'

    def __repr__(self) : return self.__str__()

    def computeNumberOfDigits(self, digitToFind) :
        allLinesAsChars = list("".join(self.lines))        
        print(allLinesAsChars)

        xxx = [c for c in allLinesAsChars if c == str(digitToFind)]

        return len(xxx)

    def retrievePixelValueAt(self, width, height) :
        return self.lines[height][width]

    def toString(self) :
        return list("".join(self.lines))

    @staticmethod
    def createFromDatas(width, height, datas) :
        lines = []
        for i in range(height) :
            lines.append(datas[:width])
            datas = datas[width:]

        return Layer(width, height, lines)

def tick(line, width, height) :
    size = width * height
    
    layers = []

    while len(line) > 0 :
        layers.append(Layer.createFromDatas(width, height, line[:size]))
        line = line[size:]

    return layers

filename = 'input_01.txt'

width = int(input("Width = "))
height = int(input("Height = "))

layers = []

with open(filename) as fp :    
    for line in fp :
        layers = tick(line, width, height)


identifiedLayer = None
fewestZero = sys.maxsize

for l in layers :
    numberOfZero = l.computeNumberOfDigits(0)

    if numberOfZero < fewestZero :
        fewestZero = numberOfZero
        identifiedLayer = l

result = identifiedLayer.computeNumberOfDigits(1) * identifiedLayer.computeNumberOfDigits(2)
print(result)
