import sys
import os
import functools
from collections import defaultdict

class Node :
    def __init__(self, data):
        self.data = data
        self.nodes = []

    def __repr__(self) :
        return f'-{self.data}|{self.nodes}'
   
class Tree : 
    
    def createNode(self, data) :
        return Node(data)

    def insert(self, node, data) :
        #print("Inserting {} in node {}".format(data, node))

        newNode = self.createNode(data)

        if (node == None) :
            return newNode

        for n in node.nodes : 
            if n.data == data :
                print("Data {} already in node {} nodes".format(data, node))
                return node
        

        node.nodes.append(newNode)
        return node
        
    def searchNode(self, node, data) :
        #print("Searching for {} in node {}".format(data, node))

        for n in node.nodes :
            if (n.data == data) : 
                return n
            
            foundNode = self.searchNode(n, data)

            if (foundNode != None) :
                return foundNode

        return None

    def display(self, node):
        if (node != None) :
            for n in node.nodes :
                print(n.data)
                self.display(n)

def count(node, depth) :
    print("{} @ {}".format(node.data, depth))

    if (len(node.nodes) == 0) :
        return depth

    total = depth

    for n in node.nodes :
        total += count(n, depth+1)
    
    return total

def extractLinkInfos(linkInfosAsString) :
    infos = linkInfosAsString.split(')')

    return {
        "from" : infos[0],
        "to" : infos[1].rstrip()
    }

def processDatas2(allOrbits, currentFrom, tree, rootNode) :
    orbitsToProcess = allOrbits[currentFrom]
    
    for orbit in orbitsToProcess :
        rootNode = tick(orbit, tree, rootNode)
        processDatas2(allOrbits, orbit['to'], tree, rootNode)
      

def tick(link, tree, rootNode) :
    #print(link)

    if (rootNode == None) : 
        rootNode = tree.createNode(link['from'])
        parentNode = rootNode
    else :
        parentNode = tree.searchNode(rootNode, link['from'])  
    
    #print(parentNode)

    if (parentNode == None) :
        newNode = tree.insert(rootNode, link['from'])
        parentNode = newNode
        rootNode = parentNode
    
    tree.insert(parentNode, link['to'])
    #print(rootNode)
    
    return rootNode
   
filename = 'input_01.txt'
orbits = []

with open(filename) as fp :    
    for line in fp :
        link = extractLinkInfos(line)
        print(link)

        orbits.append(link)

res = defaultdict(list)
for i in orbits:
    res[i['from']].append(i)

tree = Tree()
rootNode = None

rootNode = tick(res['COM'][0], tree, rootNode)
processDatas2(res, 'COM', tree, rootNode)

#tree.display(rootNode)
print(count(rootNode, 0)-1)
