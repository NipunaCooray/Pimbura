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

errArr =  []    #create a list
maxErr = 1e-5

for k in range(startVal,endValMid+1):
    tempc  = rawData[:,k]
#    errArr[k-startVal] = sum(np.power((tempc - baseTemplate),2))
    errArr.append(sum(np.power((tempc - baseTemplate),2))) # assign values one after another
    l = len(errArr) #length of list
    
    if errArr[k-startVal] > maxErr:
#        print (errArr[k-startVal])
        maxErr = errArr[k-startVal]
      
errArr = np.array(errArr)   #convert list to an array
       
# Havent done the plotting

# set of peaks, initialisation : main components
lastPos = 0
lastMag = 1e-5
countMax = 0
maxArray = np.zeros((100,2)) #  (position, value)

for k in range(1,len(errArr)-1):
    # peaks search  
    if errArr[k] > (maxFactor*maxErr):
                
        if (errArr[k] > errArr[k-1]) and (errArr[k] > errArr[k+1]): #   check Maximums 
            
            if ((errArr[k]-errArr[k-2])*(errArr[k+2]-errArr[k])) <=0:   # eliminate local maximuma from the maximum identified                                
                if k - lastPos > clustLen:                                      
                    
                    lastPos = k
                    lastMag = errArr[k]
                    maxArray[countMax,0] = lastPos+1    # +1 for python since indexing difference
                    maxArray[countMax,1] = lastMag
                    countMax = countMax + 1
                    
                elif errArr[k] >= lastMag:
                     # Could not test this expression no values passed
                     lastMag = errArr[k];
                     lastPos = k;
                     maxArray[countMax,0] = lastPos+1;
                     maxArray[countMax,1] = lastMag;
                     
# set of valleys initialisation : main components
minErr = errArr[endValMid - startVal]
minArray = np.zeros((100,2)) # start and end of words in 2 columnss
flag = 0
countMin = 0
status = 0    

for k in range(2,len(errArr)-1):    
    #   Valleys search
    if errArr[k] < minErr*minFactor:
        
        if flag == 0:      # encountering a new valley or interesting area for the fist time
            flag = 1
            gradVal =  (errArr[k + 1] - errArr[k - 1])/2    #put  gradVal(k)
            
            if np.abs(gradVal) < gradThld:  #thershold value for gradient
                status = 1  #within the background region and about to enter a letter
                
            else:
                if gradVal < 0:
                    status = 1
                    minArray[countMin,1] = k+1
                    countMin = countMin + 1
                
                else :
                    status = 1  #entering a letter
                
        else:
            gradVal =  (errArr[k  +1] - errArr[k  -1])/2
            
            if status == 1: #store values
                if np.abs(gradVal) < gradThld:
                    minArray[countMin,0] = k + 1    #+1 is added to stick to letter

            else:
                print ("something is not right")
    
    else:
        if (countMin > 1) and (minArray[countMin,0] - minArray[countMin-1,1] < wrdGap):
            print(countMin)
            if flag ==1:
                countMin = countMin -1
                
                flag = 0
            else:
                pause ###########################

        else:
            if flag == 1:
                flag = 0
                
                
############## stopped due to further modifications in the algorithm

                
                
        
            
            
    
                    
                    
                

            
        
