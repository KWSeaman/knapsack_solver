#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime

import sys
import Queue

def Greedy_Algorithm(capacity, items, taken, value, values, weight, weights):
    for i in range(0, items):
        if weight + weights[i] <= capacity:
            taken.append(1)
            value += values[i]
            weight += weights[i]
        else:
            taken.append(0)

    return value

def Dynamic_Programming_Algorithm(capacity, items, taken, value, values, weight, weights):
    Matrix = [[0 for x in range(capacity+1)] for x in range(items+1)]

    #Define Big-O
    def O(k,j):
        if j==0:
            return 0
        elif weights[j-1] <= k:
            return max(Matrix[j-1][k], values[j-1]+Matrix[j-1][k-weights[j-1]])
        else:
            return Matrix[j-1][k]

    #Iterate over items/capacity to create Matrix holding solution
    for j in range (0, items+1):
        for k in range (0, capacity+1):
            Matrix[j][k] = O(k,j)

    #Set value to bottom right corner of matrix
    value = Matrix[items][capacity]

    #Initialize taken[] to 0s
    for t in range (items):
        taken.append(0)

    #Traceback to find taken[]
    currentK = capacity
    currentJ = items

    while currentJ>0:
        if Matrix[currentJ][currentK] > Matrix[currentJ-1][currentK]:
            taken[currentJ-1]=1
            currentK -= weights[currentJ-1]
        currentJ -=1

    return value

def BandB_Cap_Algorithm(capacity, items, taken, value, values, weight, weights):
    class Node:
        def __init__(self, value, room, estimate, contains):
            self.estimate = estimate
            self.value = value
            self.room = room
            self.contains = contains

    #Set maxvalue to sum of all values
    uBound = 0
    for i in range (0, items):
        uBound += values[i]

    myQueue = Queue.Queue()
    root = Node(0, capacity, uBound, [])
    myQueue.put(root)

    maxValue = 0
    maxSeq = []

    while not myQueue.empty():
        v=myQueue.get()
        level = len(v.contains)

        #examine 1 node
        left = Node(v.value+values[level], v.room-weights[level], v.estimate, v.contains[:])
        left.contains.append(1)
        if left.room >= 0 and left.value >= maxValue:
            maxValue = left.value
            if left.contains.count>maxSeq.count:
                maxSeq = left.contains[:]
        if left.room >= 0 and left.estimate > maxValue and left.value!=left.estimate:
            myQueue.put(left)

        #examine 0 node
        right = Node(v.value, v.room, v.estimate-values[level], v.contains[:])
        right.contains.append(0)
        if right.estimate > maxValue:
            myQueue.put(right)

    value = maxValue
    #Add maxSeq to Taken
    for i in range (0, len(maxSeq)):
        taken.append(maxSeq[i])

    #Add trailing 0s
    for i in range (len(taken), items-1):
        taken.append(0)


    return value

def BandB_Linear_Algorithm(capacity, items, taken, value, values, weight, weights):
    class Node:
        def __init__(self, value, room, estimate, contains):
            self.estimate = estimate
            self.value = value
            self.room = room
            self.contains = contains

    def getBound(node):
        if node.room < 0: return 0
        else:
            uBound = node.value
            bagCap = node.room
            level = len(node.contains)

            #create a set of subarrays from values and weights still in the decision
            boundValues = values[level:items]
            boundWeights = weights[level:items]

            #create a new array of value/weight
            ratio = []
            for x in range(0, len(boundValues)):
                ratio.append(boundValues[x]/boundWeights[x])

            #loop to add items to knapsack with highest ration until bag is full

            while bagCap>=0 and len(ratio) > 0:
                #find most efficient object
                index = ratio.index(max(ratio))
                #if it fits add it, otherwise break
                if boundWeights[index] <= bagCap:
                    #Add It
                    uBound += boundValues[index]
                    bagCap -= boundWeights[index]

                    #remove it from list
                    del boundValues[index]
                    del boundWeights[index]
                    del ratio[index]
                else:
                    #Break
                    break

            #Add fraction of last item
            if len(ratio)>0:
                uBound += (max(ratio)*bagCap)
            bagCap = 0

            return uBound

    myQueue = Queue.Queue()
    root = Node(0, capacity, 0, [])
    myQueue.put(root)

    maxValue = 0
    maxSeq = []

    while not myQueue.empty():
        v=myQueue.get()
        level = len(v.contains)

        #examine 1 node
        left = Node(v.value+values[level], v.room-weights[level], v.estimate, v.contains[:])
        left.contains.append(1)
        left.estimate = getBound(left)

        if left.room >= 0 and left.value >= maxValue:
            maxValue = left.value
            if len(left.contains)>len(maxSeq):
                maxSeq = left.contains[:]
        if left.room >= 0 and left.estimate > maxValue:
            myQueue.put(left)

        #examine 0 node
        right = Node(v.value, v.room, v.estimate-values[level], v.contains[:])
        right.contains.append(0)
        right.estimate = getBound(right)

        if right.estimate > maxValue:
            myQueue.put(right)

    value = maxValue
    #Add maxSeq to Taken
    for i in range (0, len(maxSeq)):
        taken.append(maxSeq[i])

    #Add trailing 0s
    for i in range (len(taken), items):
        taken.append(0)


    return value

def BandB_Linear_DF_Algorithm(capacity, items, taken, value, values, weight, weights):
    class Node:
        def __init__(self, value, room, estimate, contains):
            self.estimate = estimate
            self.value = value
            self.room = room
            self.contains = contains

    def getBound(node):
        if node.room < 0: return 0
        else:
            uBound = node.value
            bagCap = node.room
            level = len(node.contains)

            #create a set of subarrays from values and weights still in the decision
            boundValues = values[level:items]
            boundWeights = weights[level:items]

            #create a new array of value/weight
            ratio = []
            for x in range(0, len(boundValues)):
                ratio.append(boundValues[x]/boundWeights[x])

            #loop to add items to knapsack with highest ration until bag is full

            while bagCap>=0 and len(ratio) > 0:
                #find most efficient object
                index = ratio.index(max(ratio))
                #if it fits add it, otherwise break
                if boundWeights[index] <= bagCap:
                    #Add It
                    uBound += boundValues[index]
                    bagCap -= boundWeights[index]

                    #remove it from list
                    del boundValues[index]
                    del boundWeights[index]
                    del ratio[index]
                else:
                    #Break
                    break

            #Add fraction of last item
            if len(ratio)>0:
                uBound += (max(ratio)*bagCap)
            bagCap = 0

            return uBound

    class PriorityQueue(Queue.Queue):
        def _put(self, item):
            if len(self.queue)>0:
                if self.queue[0].estimate<item.estimate:
                    self.queue.appendleft(item)
                else: self.queue.append(item)
            else:
                self.queue.append(item)

        def _fakeFunc(selfself):
            x =1
        # def _get(self):
        #     queueList = list(self.queue)
        #     index = queueList.index(next((x for x in queueList if x.estimate == max(node.estimate for node in queueList)), None))
        #
        #     return self.queue.pop(0)[1]

    myQueue = PriorityQueue()
    root = Node(0, capacity, 0, [])
    myQueue.put(root)

    maxValue = 0
    maxSeq = []

    while not myQueue.empty():
        v=myQueue.get()
        level = len(v.contains)

        #examine 1 node
        left = Node(v.value+values[level], v.room-weights[level], v.estimate, v.contains[:])
        left.contains.append(1)
        left.estimate = getBound(left)

        if left.room >= 0 and left.value >= maxValue:
            maxValue = left.value
            if len(left.contains)>len(maxSeq):
                maxSeq = left.contains[:]
        if left.room >= 0 and left.estimate > maxValue:
            myQueue.put(left)

        #examine 0 node
        right = Node(v.value, v.room, v.estimate-values[level], v.contains[:])
        right.contains.append(0)
        right.estimate = getBound(right)

        if right.estimate > maxValue:
            myQueue.put(right)

    value = maxValue
    #Add maxSeq to Taken
    for i in range (0, len(maxSeq)):
        taken.append(maxSeq[i])

    #Add trailing 0s
    for i in range (len(taken), items):
        taken.append(0)


    return value

def ExhaustiveSearch(capacity, items, taken, value, values, weight, weights):
    return 0

def solverAttempt (capacity, items, taken, value, values, weight, weights):
    #Create solver model file
    path='C:\\Solver\\bin\\'
    filename='test_'+str(items)+'_'+str(capacity)+'_'+str(datetime.datetime.now().date())+'_'+ str(datetime.datetime.now().hour)+'_'+str(datetime.datetime.now().minute)+'_'+str(datetime.datetime.now().second)+'.mzn'
    solverFile = open(path+filename,'w')
    solverFile.write('%G12 Solver File for '+str(items)+' items and '+str(capacity)+' Capacity run at '+ str(datetime.datetime.now())+'\n')
    solverFile.write('\n%Parameters\n')
    solverFile.write('int: n='+str(items)+'; \n')
    solverFile.write('int: k='+str(capacity)+'; \n')
    solverFile.write('int: maxValue='+str(sum(values))+'; \n')
    sizeString = 'array[1..n] of int: size = ['
    for i in range(0,items):
        sizeString += str(weights[i])
        if i!=items-1:sizeString+=','
    sizeString +="]; \n"
    solverFile.write(sizeString);

    valueString = 'array[1..n] of int: value = ['
    for i in range(0,items):
        valueString += str(values[i])
        if i!=items-1:valueString+=','
    valueString +="]; \n"
    solverFile.write(valueString);

    solverFile.write('\n%Decision Variables\n')

    solverFile.write('array [1..n] of var 0..1: x;\n')
    solverFile.write('var 0..maxValue: v;\n')

    solverFile.write('\n%Constraints\n')
    solverFile.write('constraint sum (i in 1..n) (value[i] * x[i]) >= v; \n')
    solverFile.write('constraint sum (i in 1..n) (size[i] * x[i]) <= k; \n')

    solverFile.write('\n%Solve - Greedy Naive Solver\n')
    solverFile.write('solve maximize v; \n')
    #:: int_search(x, input_order, indomain_max, complete)
    solverFile.write('')

    solverFile.write(r'output [show(v) , "\n"] ++ [show(x[i]) ++"\n" | i in 1..n];')
    solverFile.close()

    #run solver and get solution
    import os
    from subprocess import check_output as qx

    os.chdir('c:\\Solver\\bin')
    cmd = r'mzn-g12fd.bat '+filename
    output = qx(cmd)
    os.chdir('C:\\Users\\keseaman\\Dropbox\\Coursera\\Discrete Optimization\\knapsack')
    lines=output.splitlines();

    #format output and return
    value = int(lines[0])
    #numColors = int(max(lines [:nodeCount]))+1
    opt = 0
    if lines [-1]=='==========': opt = 1

    #outputData = str(numColors) + ' ' + str(opt) + '\n'
    #outputData += ' '.join(map(str, lines[:nodeCount]))
    for line in lines[1:items+1]:
        taken.append(line)
    return [value, opt];



def solveIt(inputData):
    # Modify this code to run your optimization algorithm
    # parse the input
    lines = inputData.split('\n')

    firstLine = lines[0].split()
    items = int(firstLine[0])
    capacity = int(firstLine[1])

    values = []
    weights = []

    for i in range(1, items+1):
        line = lines[i]
        parts = line.split()

        values.append(int(parts[0]))
        weights.append(int(parts[1]))

    items = len(values)

    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    weight = 0
    taken = []

    #value = Greedy_Algorithm(capacity, items, taken, value, values, weight, weights)
    #value = Dynamic_Programming_Algorithm(capacity, items, taken, value, values, weight, weights)
    #value  = BandB_Cap_Algorithm(capacity, items, taken, value, values, weight, weights)
    #value  = BandB_Linear_Algorithm(capacity, items, taken, value, values, weight, weights)
    #value  = BandB_Linear_DF_Algorithm(capacity, items, taken, value, values, weight, weights)
    output = solverAttempt(capacity, items, taken, value, values, weight, weights)
    value = output[0]
    opt = output[1]

    # prepare the solution in the specified output format
    outputData = str(value) + ' ' + str(opt) + '\n'
    outputData += ' '.join(map(str, taken))
    return outputData






if __name__ == '__main__':
    if len(sys.argv) > 1:
        fileLocation = sys.argv[1].strip()
        inputDataFile = open(fileLocation, 'r')
        inputData = ''.join(inputDataFile.readlines())
        inputDataFile.close()
        print solveIt(inputData)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)'

