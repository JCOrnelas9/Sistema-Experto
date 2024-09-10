# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 20:27:38 2024

@author: Usuario
"""

import numpy as np


def SIGN(WT,n,My,Mx):
    MxT = Mx[n]
    for y in WT:        
        Z = np.sign((np.dot(WT, MxT)))
    return Z
            

def omega(WT,Z,n,My,Mx):
    MxT = Mx[n]
    MyT = My[n]
    W1 = WT+(1/2)*(MyT-Z)*(MxT)
    return W1


W = np.array([[1],
              [1],
              [1]
    ])
Mx = np.array([[1,-1,-1],
              [1,1,-1],
              [1,-1,1],
              [1,1,1]
              ])
My = np.array([[-1],
               [-1],
               [-1],
               [1]
    ])

WT = np.transpose(W)


Z = SIGN(WT,0,My,Mx)
W1 = omega(WT,Z,0,My,Mx)

Z1 = SIGN(W1,1,My,Mx)
W2 = omega(W1,Z,1,My,Mx)

Z2 = SIGN(W2,2,My,Mx)
W3 = omega(W2,Z,2,My,Mx)

Z3 = SIGN(W3,3,My,Mx)
W4 = omega(W3,Z,3,My,Mx)





