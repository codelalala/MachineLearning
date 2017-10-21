# -*- coding: utf-8 -*-
"""
ApacheCN

"""
from numpy import *
import operator
from os import listdir
import matplotlib
import matplotlib.pyplot as plt

def creatDataSet():
    
    group=array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels=['A','A','B','B']
    return group,labels

def classify0(inX,dataSet,labels,k):
    dataSetSize=dataSet.shape[0]
    diffMat=tile(inX,(dataSetSize,1))-dataSet
    sqDiffMat=diffMat**2
    sqDistance=sqDiffMat.sum(axis=1)
    distances=sqDistance**0.5
    #sorted the distance base on L2 distance,return the indices
    sortedDistIndicies=distances.argsort()
    
    classCount={}
    for i in range(k):
        #this is the index for label, and classCount is incremented by the the number of labels voted
        voteIlabel=labels[sortedDistIndicies[i]]
        classCount[voteIlabel]=classCount.get(voteIlabel,0)+1
    sortedClassCount=sorted(classCount.items(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]
def file2matrix(filename):
    fr=open(filename)
    numberOfLines=len(fr.readlines())
    
    returnMat=zeros((numberOfLines,3))
    classLabelVector=[]
    fr=open(filename)
    index=0
    for line in fr.readlines():
        line=line.strip()
        listFromLine=line.split('\t')
        returnMat[index,:]=listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))
        index+=1
    return returnMat,classLabelVector
        
        
        
def autoNorm(dataSet):
    minVals=dataSet.min(0)
    maxVals=dataSet.max(0)
    ranges=maxVals-minVals
    normDataSet=zeros(shape(dataSet))
    m=dataSet.shape[0]
    normDataSet=dataSet-tile(minVals,(m,1))
    normDataSet=normDataSet/tile(ranges,(m,1))
    return normDataSet,ranges,minVals
    
    
def datingClassTest():
    hoRatio=0.1
    datingDataMat,datingLabels=file2matrix('input/2.knn/datingTestSet2.txt')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(datingDataMat[:, 0], datingDataMat[:, 1], 15.0*array(datingLabels), 15.0*array(datingLabels))
    plt.show()
    #数据归一化，normalized to [0,1]
    normMat,ranges,minVals=autoNorm(datingDataMat)
    #number of total data 
    m=normMat.shape[0]
    #number of testing data
    numTestVecs=int(m*hoRatio)
    errorCount=0.0
    for i in range(numTestVecs):
        classifierResult=classify0(normMat[i,:],normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],3)
        #print("the classifier came back with: %d, the real answer is: %d" %(classifierResult,datingLabels[i]))
        if(classifierResult!=datingLabels[i]):errorCount+=1.0
    print("the total error rate is: %f" %(errorCount/float(numTestVecs)))
    print(errorCount)
    
    
def cladifyPerson():
    resultList=['not at all','in small doses','in large doses']
    percentTats=float(raw_input("percentage of time spent playing video games? "))
    ffMiles=float(raw_input("frequent filer miles earned per year?"))
    iceCream=float(raw_input("liters of ice cream consumed per year?"))
    datingDataMat, datingLabels=file2matrix('input/2.knn/datingTestSet2.txt')
    normMat,ranges,minVals=autoNorm(datingDataMat)
    inArr=array([ffMiles,percentTats,iceCream])
    classifierResult=classify0((inArr-minVals)/ranges,normMat,datingLabels,3)
    print("you will probably like this persion: ",resultList[classifierResult-1])
    
def img2vector(filename):
    returnVect=zeros((1,1024))
    fr=open(filename)
    for i in range(32):
        lineStr=fr.readline()
        for j in range(32):
            returnVect[0,32*i+j]=int(lineStr[j])
    return returnVect
    
def handwritingClassTest():
    hwLabels=[]
    trainingFileList=listdir('input/2.KNN/trainingDigits')
    m=len(trainingFileList)
    trainingMat=zeros((m,1024))
    
    for i in range(m):
        fileNameStr=trainingFileList[i]
        fileStr=fileNameStr.split('.')[0]
        classNumStr=int(fileStr.split('_')[0])
        hwLabels.append(classNumStr)
        trainingMat[i,:]=img2vector('input/2.KNN/trainingDigits/%s'% fileNameStr)
        
    testFileList=listdir('input/2.KNN/testDigits')
    errorCount=0.0
    mTest=len(testFileList)
    for i in range(mTest):
        fileNameStr=testFileList[i]
        fileStr=fileNameStr.split('.')[0]
        classNumStr=int(fileStr.split('_')[0])
        vectorUnderTest=img2vector('input/2.KNN/testDigits/%s'%fileNameStr)
        classifierResult=classify0(vectorUnderTest,trainingMat,hwLabels,3)
        print("the classifier cam back with: %d, the real answer is: %d" %(classifierResult,classNumStr))
        if (classifierResult!=classNumStr):
            errorCount+=1
    print("\n the total number of error is: %d" %errorCount)
    print("\n the total error rate is: %f" %(errorCount/float(mTest)))


def test1():
    group, labels=creatDataSet()
    print(str(group))
    print(str(group))
    print(classify0([0.1,0.1],group,labels,3))
if __name__=='__main__':
    #test1()
    #datingClassTest()
    handwritingClassTest()
    