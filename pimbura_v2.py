# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 08:46:43 2017

@author: buddhinip
"""
import numpy as np
#import scipy as sp
from scipy import signal
import cv2
import matplotlib.pyplot as plt

# Load an color image in grayscale
#img = cv2.imread('messi5.jpg',0)

print(cv2. __version__)

startVal = 9            #for MatLab
startVal = startVal-1   #for python
endValMid = 307         #for Matlab
endValMid = endValMid-1 #for python

img = cv2.imread('C:/My Documents/Work/Elastic cutting/trunk/1.PNG',1)

cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

minFactor = 5   # % Threshold for begining and end of letters, interms of value  
maxFactor = 0.2   # % Threshold for features of importance, interms of value      
clustLen = 1       #% min gap between peaks [features of important]
rThreshold = 0.80   #% Threshold Pearsons'Corr Coeff [r] value of matching


######## Way to select to the best colour [r, g, or b] that would highlight features
highest = -1e-5

for tempk in range(3):
    temp = img[:,:,tempk]
    temp = np.std(temp)  

    
    if temp > highest:
        highest = temp
        colourInd = tempk


rawData = img[:,:,colourInd]

(p,q) = rawData.shape


####### Thresholding Operation





