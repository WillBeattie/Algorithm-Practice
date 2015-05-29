# -*- coding: utf-8 -*-
"""
Created on Wed May 27 13:01:27 2015

@author: Will
"""

import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
from random import randint
from operator import itemgetter

def evalPath(ys):
    #This function returns the time it takes an object to slide
    #along the frictionless path described by ys
    ts=[0]
    vs=[0]
    lastY=ys[0]
    Yo=ys[0]
    time=0
    
    for y in ys[1:]:
        if y>Yo: #The ball will come to a stop if any point along the path exceeds the initial height
            return 999999999
        
        v=sqrt(ys[0]-(y+lastY)/2)  #We'll assume the speed at the midpoint of the segment is the average speed across the segment.  This is wrong, but probably OK.
        vs.append(v)
        
        L=sqrt(1+(y-lastY)**2)        
        
        time += L/v
        ts.append(time)

        lastY=y        

    #Plotting bullshit happens here
    """
    plt.clf()   

    plt.subplot(3,1,1)
    plt.plot(ys)
    plt.ylabel('Height')
    
    plt.subplot(3,1,2)
    plt.plot(vs)
    plt.ylabel('Speed')
    
    plt.subplot(3,1,3)
    plt.plot(ts)
    plt.ylabel('Time')
    """    
    return time

def jiggle(ys,delta=.05):
    #Returns a perturbed copy of the path ys
    #The first and last points of ys must stay the same 

    #I want a perturbation weighted so pull the point back up if it's below
    #the plum line, and push it back down if it's above
    final= ys[-1]
    L=len(ys)
    result=[ys[0]]
    for i in range(len(ys))[1:-1]:
        remainingSlope=(final-ys[i-1])/(L-i)        
        result.append(ys[i-1]+remainingSlope+delta*np.random.normal(0,1))
    result.append(ys[-1])
    return result
        
def jiggle2(ys,delta=.05):
    #Returns a perturbed copy of the path ys
    #The first and last points of ys must stay the same 

    #I want a perturbation weighted so pull the point back up if it's below
    #the plum line, and push it back down if it's above
    result=[ys[0]]    
    for i in range(len(ys))[1:-1]:
        result.append(ys[i]+delta*np.random.normal(0,1))
    result.append(ys[-1])
    return result
                


def main(a=6,b=0,n=100,tests=1000,delta=.05):
    #First test to demonstrate the genetic nature.  Compare twenty candidates, pick a winner
    #No attempt at speed optimization, just brute force

    #Currently we're only taking the single best member of each generation,
    #but it shouldn't be hard to modify the structure to select the 'n' best candidates

    plt.clf()    
    points=np.linspace(a,b,n) #Our initial guess is a straight line between points
    cands=[[points,evalPath(points)]]  #Store our paths as a [path,score] pair (probably better structured in OOP, to be edited later?)
    
    for j in range(tests):
        points=cands[0][0]

        if j%800==0:
            plt.plot(points)

        cands=[[points,evalPath(points)]]  #Reseed our candidate list with only the winner from last time

        for i in range(10):
            newPoints=jiggle2(points,delta)
            cands.append([newPoints,evalPath(newPoints)])
    
        cands=sorted(cands,key=itemgetter(1)) #Sort the [path,score] pairs by score
        
        if j%500==0:
            print "The best score for round ",j," is: ", cands[0][1]

    plt.plot(cands[0][0])
    print "The final round's best score is: ", cands[0][1]
    return cands[0]


    
def test1(a=6,b=4):
    plt.clf()    
    a=np.linspace(a,b,100)
    plt.plot(a)
    b=jiggle2(a)
    plt.plot(b)    
    print evalPath(a),evalPath(b)      
    
def test2(a=6,b=4):
    plt.clf()
    points=np.linspace(a,b,100)
    plt.plot(points)
    
    for i in range(20): 
        points=jiggle(points)
        plt.plot(points)
        
        
def test3(a=6,b=4):
    plt.clf()
    points=np.linspace(a,b,100)
    plt.plot(points)
    
    for i in range(20): 
        points=np.linspace(a,b,100)
        plt.plot(jiggle2(points))
        