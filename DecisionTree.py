# -*- coding: utf-8 -*-
"""
ApachCN
"""

import operator
from math import log
#import dicisionTreePlot as dtPlot

def createDataSet():
    dataSet=[[1,1,'yes'],
             [1,1,'yes'],
             [1,0,'no'],
             [0,1,'no'],
             [0,1,'no']]
    labels=['no surfacing','flippers']
    return dataSet,labels
def calcShannonEnt(dataSet):
    numEntries=len(dataSet)
    labelCounts={}
    for featVec in dataSet:
        currentLabel=featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel]=0
        labelCounts[currentLabel]+=1
    shannonEnt=0.0
    for key in labelCounts:
        prob=float(labelCounts[key]/numEntries)
        shannonEnt-=prob*log(prob,2)
    return shannonEnt

def splitDataSet(dataSet,index,value):
    retDataSet=[]
    for featVec in dataSet:
        if featVec[index]==value:
            reducedFeatVec=featVec[:index]
            reducedFeatVec.extend(featVec[index+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet

def chooseBestFeatureToSplit(dataSet):
    numFeatures=len(dataSet[0])-1
    baseEntropy=calcShannonEnt(dataSet)
    bestInfoGain,bestFeature=0.0,-1
    for i in range(numFeatures):
        featList=[example[i] for example in dataSet]
        uniqueVals=set(featList)
        newEntropy=0.0
        for value in uniqueVals:
            subDataSet=splitDataSet(dataSet,i,value)
            prob=len(subDataSet)/float(len(dataSet))
            newEntropy+=prob*calcShannonEnt(subDataSet)
        infoGain=baseEntropy-newEntropy
        print('infoGain=', infoGain,'bestFeature=',i,baseEntropy,newEntropy)
        if(infoGain>bestInfoGain):
            bestInfoGain=infoGain;
            bestfeature=i
    return bestFeature
def creatTree(dataSet,labels):
    classList=[example[-1] for example in dataSet]
    if classList.count(classList[0])==len(classList):
        return classList[0]
    if len(dataSet[0])==1:
        return majorityCnt(classList)
    bestFeat=chooseBestFeatureToSplit(dataSet)
    bestFeatLabel=labels[bestFeat]
    myTree={bestFeatLabel:{}}
    del(labels[bestFeat])
    featValues=[example[bestFeat] for example in dataSet]
    uniqueVals=set(featValues)
    for value in uniqueVals:
        subLabels=labels[:]
        myTree[bestFeatLabel][value]=creatTree(splitDataSet(dataSet,bestFeat,value),subLabels)
    return myTree
def classify(inputTree,featLabels,testVec):
    firstStr=list(inputTree.keys())[0]
    secondDict=inputTree[firstStr]
    featIndex=featLabels.index(firstStr)
    key=testVec[featIndex]
    valueOfFeat=list(secondDict)[key]
    print('+++',firstStr,'xxx',secondDict,'---',key,'>>>',valueOfFeat)
    if isinstance(valueOfFeat,dict):
        classLabel=classify(valueOfFeat,featLabels,testVec)
    else:
        classLabel=valueOfFeat
    return classLabel

def fishTest():
    myDat,labels=createDataSet()
    import copy
    myTree=creatTree(myDat,copy.deepcopy(labels))
    print(myTree)
    print(classify(myTree,labels,[1,1]))
    #dtPlot.creatPlot(myTree)

if __name__=="__main__":
    fishTest()