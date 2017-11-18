# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 21:44:47 2017

ApachCN
"""
from numpy import *
import matplotlib.pyplot as plt

def loadDataSet(file_name):
    dataMat=[]
    labelMat=[]
    fr=open(file_name)
    for line in fr.readlines():
        lineArr=line.strip().split()
        #why add this 1.0 data in front?
        dataMat.append([1.0,float(lineArr[0]),float(lineArr[1])])
        labelMat.append(int(lineArr[2]))
    return dataMat,labelMat
        
def sigmoid(inX):
    return 1.0/(1+exp(-inX))


def plotBestFit(dataArr,labelMat,weights):
    
    n=shape(dataArr)[0]
    
    xcord1=[]
    ycord1=[]
    xcord2=[]
    ycord2=[]
    for i in range(n):
        if int(labelMat[i])==1:
            xcord1.append(dataArr[i,1])
            ycord1.append(dataArr[i,2])
        else:
            xcord2.append(dataArr[i,1])
            ycord2.append(dataArr[i,2])
    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.scatter(xcord1,ycord1,s=30,c='red', marker='s')
    ax.scatter(xcord2,ycord2,s=30,c='green')
    x=arange(-3.0,3.0,0.1)
    #what is this weight? Is it right to calculate weight by this method
    y=(-weights[0]-weights[1]*x)/weights[2]
    ax.plot(x,y)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()
def gradDecent(dataMatin, classLabels):
    
#    dataMatrix=mat(dataMatin)
#    m,n=shape(dataMatrix)
#    
#    alpha=0.01
#    weights=one(n)
#
    dataMatrix=mat(dataMatin)
    labelMat=mat(classLabels).T
    m,n=shape(dataMatin)
    weights=mat(ones(n)).T
    alpha=0.01
    maxCycles=500
    for j in range(maxCycles):
        h=sigmoid(dataMatrix*weights)
        error=(h-labelMat)
        derivative=multiply(error,h,(1-h)).T*dataMatrix
        weights=weights-alpha*derivative.T
        #weights=weights-alpha*dataMatrix.transpose()*error
    
    
    return array(weights)

def stoGradDecent1(dataMatin, classLabels,numIter=1500):
    #how to change from gradeAscent to gradDecent?
    #sign of the loss function and gredient?
    dataMatrix=array(dataMatin)
    #labelMat=mat(classLabels).transpose()
    m,n=shape(dataMatrix)
    
    #maxCycles=500
    weights=ones(n)
    for j in range(numIter):
        dataIndex=list(range(m))
        for i in range(m):
            alpha=4/(1.0+j+i)+0.0001
            randIndex=int(random.uniform(0,len(dataIndex)))
            if shape(dataMatrix[randIndex])!=shape(weights):
                print("the shape is not the same")
            h=sigmoid(sum(dataMatrix[randIndex]*weights))
            error=-(classLabels[randIndex]-h)
            derivative=h*(1-h)*dataMatrix[randIndex]
            print(weights,"*"*10,dataMatrix[i],"*"*10,error)
            #weights=weights-alpha*dataMatrix[randIndex]*error
            weights=weights-alpha*derivative
            del(dataIndex[randIndex])
        return array(weights)
def testLR():
    
    dataMat,labelMat=loadDataSet("input/5.Logistic/TestSet.txt")
    
    dataArr=array(dataMat)
    weights=gradDecent(dataArr,labelMat)
    #weights=stoGradDecent1(dataArr,labelMat)
    plotBestFit(dataArr,labelMat,weights)
    
    
    
if __name__=="__main__":
    testLR()