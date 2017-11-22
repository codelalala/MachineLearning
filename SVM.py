# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 22:32:55 2017

Apachecn
"""
from numpy import *
import matplotlib.pyplot as plt

def loadDataSet(fileName):
    dataMat=[]
    labelMat=[]
    fr=open(fileName)
    for line in fr.readlines():
        lineArr=line.strip().split('\t')
        dataMat.append([float(lineArr[0]),float(lineArr[1])])
        labelMat.append(float(lineArr[2]))
    return dataMat, labelMat
def selectJrand(i,m):
    #generate a random integer (0,m)
    j=i
    while j==i:
        j=int(random.uniform(0,m))
    return j
    
def clipAlpha(aj,H,L):
    #aj has to be in range(L,H), here H is maximun and L is minimun
    if aj>H:
        aj=H
    if aj<L:
        aj=L
    return aj
        

def smoSimple(dataMatIn, classLabels, C, toler, maxIter):
    dataMatrix=mat(dataMatIn)
    #why transpose here? 
    labelMat=mat(classLabels).transpose()
    
    m,n=shape(dataMatrix)
    
    b=0
    alphas=mat(zeros((m,1)))
    
    iter=0
    while(iter<maxIter):
        alphaPairsChanged=0
        for i in range(m):
            fXi=float(multiply(alphas, labelMat).T*(dataMatrix*dataMatrix[i,:].T))+b
            Ei=fXi-float(labelMat[i])
            
            if((labelMat[i]*Ei<-toler) and (alphas[i]<C)) or ((labelMat[i]*Ei>toler) and (alphas[i]>0)):
                #random? What is SMO and Simplified SMO
                j=selectJrand(i,m)
                fXj=float(multiply(alphas,labelMat).T*(dataMatrix*dataMatrix[j,:].T))+b
                Ej=fXj-float(labelMat[j])
                alphaIold=alphas[i].copy()
                alphaJold=alphas[j].copy()
                
                if(labelMat[i]!=labelMat[j]):
                    L=max(0,alphas[j]-alphas[i])
                    H=min(C,C+alphas[j]-alphas[i])
                else:
                    L=max(0,alphas[j]+alphas[i]-C)
                    H=min(C,alphas[j]+alphas[i])
                    
                if L==H:
                    print("L==H")
                    continue
                
                
                eta=2.0*dataMatrix[i,:]*dataMatrix[j,:].T-dataMatrix[i,:]*dataMatrix[i,:].T-dataMatrix[j,:]*dataMatrix[j,:].T
                
                if eta>=0:
                    print("eta>=0")
                    continue
                
                alphas[j]-=labelMat[j]*(Ei-Ej)/eta
                alphas[j]=clipAlpha(alphas[j],H,L)
                
                if(abs(alphas[j]-alphaJold)<0.00001):
                    print("j not moving enough")
                    continue
                alphas[i]+=labelMat[j]*labelMat[i]*(alphaJold-alphas[j])
                
                
                
                b1 = b - Ei- labelMat[i]*(alphas[i]-alphaIold)*dataMatrix[i, :]*dataMatrix[i, :].T - labelMat[j]*(alphas[j]-alphaJold)*dataMatrix[i, :]*dataMatrix[j, :].T
                b2 = b - Ej- labelMat[i]*(alphas[i]-alphaIold)*dataMatrix[i, :]*dataMatrix[j, :].T - labelMat[j]*(alphas[j]-alphaJold)*dataMatrix[j, :]*dataMatrix[j, :].T
                
                
                
                
                if(0<alphas[i]) and (C>alphas[i]):
                    b=b1
                elif(0<alphas[j]) and (C>alphas[j]):
                    b=b2
                else:
                    b=(b1+b2)/2.0
                alphaPairsChanged+=1
                print("iter: %d i: %d, paris changed %d" %(iter, i, alphaPairsChanged))
        if(alphaPairsChanged==0):
            iter+=1
        else:
            iter=0
        print("iteration number: %d" % iter)
        
    return b, alphas
def calcWs(alphas,dataArr,classLabels):
    X=mat(dataArr)
    labelMat=mat(classLabels).transpose()
    m,n=shape(X)
    w=zeros((n,1))
    for i in range(m):
        w+=multiply(alphas[i]*labelMat[i],X[i,:].T)
    return w

def plotfig_SVM(xMat,yMat,ws,b,alphas):
    
    xMat=mat(xMat)
    yMat=mat(yMat)
    
    b=array(b)[0]
    fig=plt.figure()
    ax=fig.add_subplot(111)
    
    ax.scatter(xMat[:,0].flatten().A[0],xMat[:,1].flatten().A[0])
    
    x=arange(-1.0,10.0,0.1)
    
    y=(-b-ws[0,0]*x)/ws[1,0]
    
    ax.plot(x,y)
    for i in range (shape(yMat[0,:])[1]):
        if yMat[0,1]>0:
            ax.plot(xMat[i,0],xMat[i,1],'cx')
        else:
            ax.plot(xMat[i,0],xMat[i,1],'kp')
    for i in range(100):
        if alphas[i]>0.0:
            ax.plot(xMat[i,0],xMat[i,1],'ro')
    plt.show()
if __name__=="__main__":
    dataArr,labelArr=loadDataSet('input/6.SVM/testSet.txt')
    
    b,alphas=smoSimple(dataArr,labelArr,0.6,0.001,40)
    
    print('/n/n/n')
    print('b=',b)
    print('alphas[alphas>0]=',alphas[alphas>0])
    print('shape(alphas[alphas>0])=',shape(alphas[alphas>0]))
    for i in range(100):
        if alphas[i]>0:
            print(dataArr[i],labelArr[i])
    ws=calcWs(alphas,dataArr,labelArr)
    plotfig_SVM(dataArr,labelArr,ws,b,alphas)
