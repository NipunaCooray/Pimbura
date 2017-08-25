import numpy as np
from scipy import signal
import cv2
import matplotlib.pyplot as plt

# finds peaks in a 1 D array
def findpeaks(inpArray): # inpArray is a column array of n x 1 dimensions
    arrSize = inpArray.shape # sise of the array   
    if arrSize[0] < 2:
        print('Array passed to find peaks is not an array OR not in the correct column array format')
    pInds = np.zeros((1,arrSize[0]))
    pVals = np.zeros((1,arrSize[0]))
    count = 0
    for k in range(1,arrSize[0]-1):
        if inpArray[k+1] < inpArray[k] and inpArray[k-1] <= inpArray[k]:
            pInds[0,count] = k
            pVals[0,count] = inpArray[k]
            count += 1
    return [pVals, pInds, count]
#==============================================================================

print(cv2. __version__)

startVal = 9            #for MatLab
startVal = startVal-1   #for python
endValMid = 307         #for Matlab
endValMid = endValMid-1 #for python

img = cv2.imread('C:/Users/BuddhiniP/Documents/Pimbura/trunk/1.PNG',1)

#cv2.imshow('image',img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

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
I = rawData
level, imgf = cv2.threshold(I,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

rawData = np.array(imgf)
rawData = rawData.astype(float)
#cv2.imshow('rawData',rawData)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

####### Selection of base Template
baseTemplate1 = rawData[:,startVal]
baseTemplate2 = rawData[:,endValMid]
#baseTemplate = 0.0

baseTemplate = (baseTemplate1 + baseTemplate2)*0.5

errArr =  []    #create a list
#errArr = np.array(errArr)   #convert list to an array
#maxErr = 1e-5

for k in range(startVal,endValMid+1):
    tempc  = rawData[:,k]
    errArr.append(sum(np.power((tempc - baseTemplate),2))) # assign values one after another
    l = len(errArr) #length of list
    

errArr = np.array(errArr)   #convert list to an array
maxErr = np.amax(errArr)   #max value of the array

####### set of peaks, initialisation : main components
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
if minErr == 0:
    minErr = 1e5
    
###### Valleys
minArray = np.zeros((100,2)) # start and end of words in 2 columnss
countMin = 0

#t2 =  np.asarray(np.where(errArr<= (minFactor*minErr)))
#t4 =  np.asarray(np.gradient(t2[1,:]) > 1)

t2= np.where(errArr<= (minFactor*minErr))   #####CHANGE THESE TUPELS TO ARRAYS
t4= np.where(np.gradient(t2[0])>1)      
gradErr = np.gradient(errArr)

for k in range (len(t4[0])):    ### LENGTH OF TUPEL    
    a = t4[0]       #
    aa = a[k]       #   THESE VARIABLES ARE INITIALIZED ONLY FOR PYTHON
    b = t2[0]       #   
    bb = b[aa]      #
#    bb = t2[t4[k]]
    
    if gradErr[bb] >= 0:                
        if minArray[countMin,0] > 0:            
            if countMin > 1:
                minArray[countMin,1] = minArray[countMin-1,1]
                
        minArray[countMin,0] = bb       # begining of a letter
    else:        
        if minArray[countMin,0]==0 and countMin > 1:
            minArray[countMin,0] = minArray[countMin-1,0]            
        
        minArray[countMin,1] = bb      # end of a letter
        countMin = countMin + 1
        
if countMin > 1:
    countMin = countMin -1
    
gap = minArray[countMin,1] - minArray[0,0]+1

if countMax < 10:
    t22 = np.asarray(np.where(errArr > maxFactor*maxErr))
    tx = errArr[t22[0,:]]
    
    t = findpeaks(tx)
    t4 = np.asarray(t[1])
    if not t4.size and len(t4) > 9:
        countMax = len(t[1])
        maxArray = np.zeros((countMax,1))
    
    
    
    
    










