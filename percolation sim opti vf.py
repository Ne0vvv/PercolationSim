# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 17:04:15 2024

@author: achil

Percolation simulation

basic idea
On veut une grille de pixel tels que ils ont la même couleur si il y a une arrete qui les relis
on a une grille de nxn pixels x=l y=c
"""
from PIL import Image
import random as rd
import sys
import matplotlib.pyplot as plt


sys.setrecursionlimit(15000000) #computationnaly intensive, lower depending of the computer
#A=Image.new("RGB", (5000,5000), (0,0,0))
#A.show() 

"matrix functions to have all edges open or closed"

def noise(n):
    "To have random set of colors for initialisatin"
    A=Image.new("RGB", (n,n), (0,0,0))
    for c in range(n):
        for l in range(n):
            A.putpixel((c,l), color())
    return A

def matriceH(p,n):  #horizontal vertices
    H=[[None for c in range (n)]for l in range(n-1)] #M[y][x]
    for l in range (n-1):
        for c in range(n):
            if rd.randint(0, 100)>=100*p:
                H[l][c]=1
            else:
                H[l][c]=0
    return H

def matriceV(p,n): #M[y][x] Vertical edges
    V=[[None for c in range (n-1)]for l in range(n)]
    for l in range (n):
        for c in range(n-1):
            if rd.randint(0, 100)>=100*p:
                V[l][c]=1
            else:
                V[l][c]=0
    return V


"H,V[col][ligne]"
def color():
    r=rd.randint(0,255)
    g=rd.randint(0,255)
    b=rd.randint(0,255)
    return (r,g,b)

def samecolor(A,c,l, x, y):
    if A.getpixel((c,l))==A.getpixel((x,y)):
        return True
    else:
        return False

def simulationperlin(p, n):
    H=matriceH(p,n)
    V=matriceV(p,n)
    A= Image.new("RGB", (n,n), (50,50,200))
    for l in range (n-1):
        for c in range(n-1):
            if V[c][l]==1:
                A.putpixel((c,l+1), A.getpixel((c,l)))
            elif H[c][l]==1:
                A.putpixel(((c+1),l), A.getpixel((c,l)))
            elif V[c][l]==0:
                A.putpixel((c,l+1), color())
            elif H[c][l]==0:
                A.putpixel((c+1,l), color())       
    #A.show()
    return A
             

        
        

def nbconnect(H,V,c,l,n): #BON
    "return the number of connected edges of the (c,l) pixel"
    if l==0:
        if c==0:
            return H[c][l]+V[c][l]   #ok
        elif c==n-1:
            return H[c-1][l]+V[c][l]  #ok
        else:
            return H[c-1][l]+H[c][l]+V[c][l] #ok
    elif c==0:
        if l==n-1:
            return V[c][l-1]+H[c][l]  #ok
        else:
            return V[c][l-1]+V[c][l]+H[c][l] #ok
    elif l==n-1 and c==n-1:
        return V[c][l-1]+H[c-1][l]
    else:
        return V[c][l-1]+H[c-1][l]+V[c][l]+H[c][l]
        
        
        

def nbcouleur(A,c, l, n): #voir amélio
    "counts the same adjacent colors of the pixel (c,l)"
    if l==0:
        if c==0:
            return 2+samecolor(A,c ,l,c+1,l)+samecolor(A,c ,l,c,l+1)
        elif c==(n-1):
            return 2+samecolor(A,c ,l,c-1,l)+samecolor(A,c ,l,c,l+1)
        else:
            return 1+samecolor(A,c ,l,c-1,l)+samecolor(A,c ,l,c+1,l)+samecolor(A,c ,l,c,l+1)
    elif c==0:
        if l==n-1:
            return 2+samecolor(A,c ,l,c+1,l)+samecolor(A,c ,l,c,l-1)
        else:
            return 1+samecolor(A,c ,l,c+1,l)+samecolor(A,c ,l,c,l+1)+samecolor(A,c ,l,c,l-1)
    elif l==n-1 and c==n-1:
        return 2+samecolor(A,c ,l,c,l-1)+samecolor(A,c ,l,c-1,l)
    else:
        return samecolor(A,c ,l,c+1,l)+samecolor(A,c ,l,c,l+1)+samecolor(A,c ,l,c,l-1)+samecolor(A,c,l, c-1, l)

"nd, si on veut baisser la récussivité faudrais une mémoire qui stocke les valeurs déja faites"

def pathb(A,H,V, c, l, n, memoire):
    "With memory, follow the probability matrix to color the connected edges (cases for matrix edge)"
    if memoire[c][l]==1:
            return A
    else:
        while c<n-1 and l<n-1:
            if (l==n or c==n) or nbcouleur(A,c,l,n)==nbconnect(H,V,c,l,n): 
                return A   #CAS DARRET PARFAIT
            
            elif H[c][l]==1 and samecolor(A, c, l, c+1, l)==False:
                A.putpixel((c+1,l), A.getpixel((c,l)))
                memoire[c][l]=1
                pathb(A,H,V, c+1, l, n, memoire)
            elif V[c][l]==1 and samecolor(A,c,l, c,l+1)==False:
                A.putpixel((c,l+1), A.getpixel((c,l)))
                memoire[c][l]=1
                pathb(A,H,V, c, l+1,n, memoire)
            elif l==0:
                if c==0:
                    memoire[c][l]=1
                    return A
                else:
                    if H[c-1][l]==1 and samecolor(A,c,l, c-1,l)== False:
                        A.putpixel((c-1,l), A.getpixel((c,l)))
                        memoire[c][l]=1
                    else: return A
            elif c==0:
                if l!=0:
                    if V[c][l-1]==1 and samecolor(A,c,l,c,l-1)== False:
                        A.putpixel((c,l-1), A.getpixel((c,l)))
                        memoire[c][l]=1
                    else: return A
            elif l!=0 and c!=0:
                if V[c][l-1]==1 and samecolor(A,c,l,c,l-1)==False:
                    A.putpixel((c,l-1), A.getpixel((c,l)))
                    memoire[c][l]=1
                    pathb(A,H,V,c,l-1,n, memoire)
                elif H[c-1][l]==1 and samecolor(A,c,l,c-1,l)==False:
                    A.putpixel((c-1,l), A.getpixel((c,l)))
                    memoire[c][l]==1
                    pathb(A,H,V,c-1,l,n,memoire)
                else: return A
            else: return A
        return A


"Showing functions"

    
def simulation(p, n):
    H=matriceH(p,n)
    V=matriceV(p,n)
    A= noise(n) #takes a random color so that even if no edges is connected the colors arent the same
    memoire=[[0 for k in range(n)]for k in range(n)]
    for l in range (n):
        for c in range(n):
            if  memoire[c][l]==0:
                if c!= 0:
                    if samecolor(A,c,l,c-1,l)==False:
                        pathb(A, H, V, c, l, n, memoire) 
                    else: pass
            #if l!=0:
                #if samecolor(A,c,l,c,l-1)== False:
                    #pathb(A, H, V, c, l, n) 
                #else: pass
                else:
                    pathb(A, H, V, c, l, n, memoire)    
            else: pass
    return A
  
      
def hist(start, end, pas,n):
    "Create picture with different edge probability next to each other"
    HIST=Image.new("RGB", (n*pas,n), (255,255,255))
    for k in range(pas):
        P=simulation(start+k*((end-start)/pas), n)
        print(start+k*((end-start)/pas))
        for c in range(n):
            for l in range(n):
                HIST.putpixel((k*n+c,l), P.getpixel((c,l)))
    HIST.show()
    
    
def pict(p,n):
    "Create a single picture (png) of edge probability p and size n*n"
    A=simulation(p, n)
    A.show()
    
    
def pourcentagecouleur(pas, n):
    "plot the color distribution as a function of the edge parameter"
    Y=[]
    X=[]
    for k in range(pas):
        X.append(k/pas)
        P=simulation(k/pas, n)
        H=[]
        memoire=[[0 for k in range(n)]for i in range(n)]
        for c in range (n):
            for l in range (n):
                C = P.getpixel((c,l))
                COUNT=0
                for c2 in range(c,n):
                    for l2 in range(l,n):
                        if memoire[c2][l2]==1:
                            pass
                        else:
                            if C==P.getpixel((c2,l2)):
                                memoire[c2][l2]=1
                                COUNT=COUNT+1
                            else:
                                pass
                H.append(COUNT)
        Y.append(max(H)/(n**2))
    plt.plot(X,Y)
    plt.xlabel("p")
    plt.ylabel("%couleurmax")
    plt.show()
    
"AUTOSTART FCT"

print("type:\n 0 for imbedded picture \n 1 for png\n 2 for a range of picture with scaling edge parameter \n 3 for an histogram of color presence \n TYPE HERE:  ")
choice=int(input())


if choice==0:
    print("imput edge probability : ")
    p=float(input())
    print("side size (in pixel): ")
    n=int(input())
    simulation(p,n) #doesnt work for some reason
if choice==1:
    print("imput edge probability : ")
    p=float(input())
    print("side size (in pixel): ")
    n=int(input())
    pict(p,n)
if choice==2:
    print("imput start probability: ")
    start=input()
    print("imput end probability: ")
    stop=input()
    print("how many pictures? :")
    pas=int(input())
    print("side size (in pixels): ")
    n=int(input())
    hist(int(start), int(stop), pas,n)
if choice==3:
    print("How many pictures? ")
    pas=int(input())
    print("side size (in pixel): ")
    n=int(input())
    pourcentagecouleur(pas,n)
















    
    
    