# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 19:36:28 2017

ApachCN
"""
from numpy import *
def loadDataSet():
    postingList=postingList = [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'], #[0,0,1,1,1......]

                   ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],

                   ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],

                   ['stop', 'posting', 'stupid', 'worthless', 'gar e'],

                   ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],

                   ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec=[0,1,0,1,0,1]
    return postingList, classVec
def setOfWords2Vec(vocabList,inputSet):
    returnVec=[0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)]=1
        else:
            print("the word:%s is not in my Vocabulary!" %word)
    return returnVec
def trainNB0(trainMatrix, trainCategory):
    #each column of trainMatrix is a doc
    numTrainDocs=len(trainMatrix)
    #each row element of a column is one binary marker for a specific word in that vector position
    numWords=len(trainMatrix[0])
    #since abusive is 1, and non-abusive is 0, so sum(trainCategory) is sum of abusive
    pAbusive=(sum(trainCategory))/float(numTrainDocs)
    print(pAbusive)
    #with Laplase Smoothing
    pAbusive=(sum(trainCategory)+1)/float(numTrainDocs+numWords)
    print(pAbusive)
    print(shape(trainMatrix))
    print(shape(trainMatrix[1])[0])
    p0Num=ones(numWords)
    
    p1Num=ones(numWords)
    #total num of words of non-abusive
    #p0Denom=2.0
    p0Denom=0
    #total num of words of abusive
    #p1Denom=2.0
    p1Denom=0;
    for i in range(numTrainDocs):
        if trainCategory[i]==1:
            #print(trainMatrix[i])
            p1Num+=trainMatrix[i]
            p1Denom+=1
            #print(sum(trainMatrix[i]))
        else:
            p0Num+=trainMatrix[i]
            p0Denom+=1
    #probability to obervice this word given non-abusive 
    #vector
    p1Vect=log(p1Num+1/p1Denom+2)
    #probability to obervice this word given abusive
    #vector
    p0Vect=log(p0Num+1/p0Denom+2)
    return p0Vect,p1Vect,pAbusive
def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    p1=sum(vec2Classify*p1Vec)+log(pClass1)
    p0=sum(vec2Classify*p0Vec)+log(1-pClass1)
    if p1>p0:
        return 1
    else:
        return 0
def creatVocabList(dataSet):
    vocabSet=set([])
    for document in dataSet:
        vocabSet=vocabSet|set(document)
    return list(vocabSet)
def testingNB():
    listOPost, listClasses=loadDataSet()
    myVocabList=creatVocabList(listOPost)
    trainMat=[]
    for postinDoc in listOPost:
        trainMat.append(setOfWords2Vec(myVocabList,postinDoc))
    p0V,p1V,pAb=trainNB0(array(trainMat),array(listClasses))
    testEntry=['love', 'my','dalmation']
    thisDoc=array(setOfWords2Vec(myVocabList,testEntry))
    print(testEntry,'classified as :',classifyNB(thisDoc,p0V,p1V,pAb))
    testEntry=['stupid','garbage']
    thisDoc=array(setOfWords2Vec(myVocabList,testEntry))
    print(testEntry,'classified as :',classifyNB(thisDoc,p0V,p1V,pAb))
    
def textParse(bigString):
    import re
    listOfTokens=re.split(r'W*', bigString)
    return [tok.lower() for tok in listOfTokens if len(tok)>2]
def spamTest():
    docList=[]
    classList=[]
    fullText=[]
    for i in range(1,26):
        wordList=textParse(open('input/4.NaiveBayes/email/spam/%d.txt' %i,encoding='ISO-8859-1').read())
        docList.append(wordList)
        classList.append(1)
        wordList=textParse(open('input/4.NaiveBayes/email/ham/%d.txt' %i,encoding='ISO-8859-1').read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList=creatVocabList(docList)
    trainingSet=list(range(50))
    testSet=[]
    for i in range(10):
        randIndex=int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    trainMat=[]
    trainClasses=[]
    for docIndex in trainingSet:
        #print(docIndex)
        #print(docList[docIndex])
        trainMat.append(setOfWords2Vec(vocabList,docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0V,p1V,pSpam=trainNB0(array(trainMat),array(trainClasses))
    errorCount=0
    for docIndex in testSet:
        print('docIndex=',docIndex)
        wordVector=setOfWords2Vec(vocabList,docList[docIndex])
        if classifyNB(array(wordVector),p0V,p1V,pSpam)!=classList[docIndex]:
            errorCount+=1
    print('the errorCount is: ', errorCount)
    print('the testSet length is:',len(testSet))
    print('the error rate is:%', float(errorCount)/len(testSet)*100)
    
if __name__=="__main__":
    #testingNB()
    spamTest()