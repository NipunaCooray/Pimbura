import numpy as np
import cv2

# Load an color image in grayscale
#img = cv2.imread('messi5.jpg',0)

print(cv2. __version__)

stratVal = 9
endValMid = 307

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

#print(gradThld)

highest = -1e-5


for tempk in range(3):
    temp = img[:,:,tempk]
    np.st
    print(tempk)
    