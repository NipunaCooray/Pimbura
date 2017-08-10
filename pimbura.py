import numpy as np
#import scipy as sp
from scipy import signal
import cv2

# Load an color image in grayscale
#img = cv2.imread('messi5.jpg',0)

print(cv2. __version__)

startVal = 9            #for MatLab
startVal = startVal-1   #for python
endValMid = 307         #for Matlab
endValMid = endValMid-1 #for python

img = cv2.imread('C:\Users\BuddhiniP\Dropbox\MATLAB\Elastic\images\Capture.png',1)

cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

minFactor = 10   # % Threshold for begining and end of letters, interms of value  
maxFactor = 0.2   # % Threshold for features of importance, interms of value      
clustLen = 1       #% min gap between peaks [features of important]
gradThld = 1e3    #% Grad Threshold value for selection of valleys 
wrdGap = 10      # % num of pixels between words. Seeting a very low values will pick gaps between letters. too high and gaps between words will be missed-> 10
rThreshold = 0.80   #% Threshold Pearsons'Corr Coeff [r] value of matching
fwinLen = 5        #% Median filter window length
#errArr=0
#errArr = np.matrix(errArr)
#errArr.astype(float)

#print(gradThld)

highest = -1e-5


for tempk in range(3):
    temp = img[:,:,tempk]
    temp = np.std(temp)
#    



    
    if temp > highest:
        highest = temp
        colourInd = tempk


rawData = img[:,:,colourInd]

(p,q) = rawData.shape


# median filter to reduce noise
K = signal.medfilt2d(rawData,fwinLen)
K = np.array(K)
rawData = K.astype(float)

baseTemplate = rawData[:,startVal]

cv2.imshow('image',K)
cv2.waitKey(0)
cv2.destroyAllWindows()

errArr =  []
maxErr = 1e-5

for k in range(startVal,endValMid+1):
    tempc  = rawData[:,k]
#    errArr[k-startVal] = sum(np.power((tempc - baseTemplate),2))
    errArr.append(sum(np.power((tempc - baseTemplate),2)))
#    errArr = np.array(errArr)
#    if errArr[k-startVal] > maxErr:
#        maxErr = errArr[k-startVal]
    
    
errArr = np.array(errArr)

for k in range(startVal,endValMid+1):
    if errArr[k-startVal] > maxErr:
        maxErr = errArr[k-startVal]

       
# set of peaks, initialisation : main components
lastPos = 0
lastMag = 1e-5
countMax = 0
#maxArray = zeros(100,2) # % (position, value)





    
    