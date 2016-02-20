import cv2
import numpy as np
import sys
import os

# class preProcessing():
#     def __init__(self,image_file):
#         self.npaFlattenedImages = np.empty((0,400))
#         self.image_file = image_file
#         #self.preProcessImage()

#     def preProcessImage(self):

#         MIN_CONTOUR_AREA = 60
#         RESIZED_IMAGE_WIDTH = 20
#         RESIZED_IMAGE_HEIGHT = 20

#         # cv2.imshow('img',self.image_file)
#         self.imgGray = cv2.cvtColor(self.image_file, cv2.COLOR_BGR2GRAY)
#         self.imgBlurred = cv2.GaussianBlur(self.imgGray, (5,5), 0)
#         self.imgThresh = cv2.adaptiveThreshold(self.imgBlurred,255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)

#         # cv2.imshow('imgGray',self.imgGray)
#         # cv2.imshow('imgBlurred',self.imgBlurred)
#         # cv2.imshow('imgThresh',self.imgThresh)

#         self.imgThreshCopy = self.imgThresh.copy() 

#         self.npaContours, self.npaHierarchy = cv2.findContours(self.imgThreshCopy,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

#         # cv2.drawContours(self.imgThreshCopy,self.npaContours,-1,(255,0,0),1)
        

#         check=1
#         for self.npaContour in self.npaContours:
#             #print cv2.contourArea(self.npaContour)
#             if cv2.contourArea(self.npaContour) > MIN_CONTOUR_AREA:
#                 check=check+1
#                 [intX, intY, intW, intH] = cv2.boundingRect(self.npaContour)

#                 cv2.rectangle(self.imgThreshCopy, (intX, intY),(intX + intW, intY + intH),(255, 0, 255),1)
#                 self.imgROI = self.imgThresh[intY : intY + intH, intX : intX + intW]
#                 # print self.imgROI.shape
#                 self.imgROIResized = cv2.resize(self.imgROI, (RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT))
                
#                 # cv2.imshow("ROI",self.imgROI)
#                 # cv2.imshow("ROIResized",self.imgROIResized)              
#                 npaFlattenedImage = self.imgROIResized.reshape((1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))
#                 self.npaFlattenedImages = np.append(self.npaFlattenedImages, npaFlattenedImage, 0)
#                 if check > 2:
#                     #print check
#                     sys.exit(0)
#         #cv2.imshow('imgThreshCopy',self.imgThreshCopy)
#         #print self.npaFlattenedImages

#         #print "training complete"
#         return self.npaFlattenedImages
npaFlattenedImages = np.loadtxt("flattened_text.txt")
npaClassifications = np.loadtxt ("classification.txt")
# npaClassification = []
# for x in xrange (0, 10):

#     for y in xrange (1,7):
#     	npaClassification.append([x])
#     	# print chr(x)
#         # img = cv2.imread ("font/sample/" + chr(x) + "/" + str(y) + ".png")
#         # npaFlattenedImage = np.loadtxt('font/sample/' + str(x) + '/' + str(y) +'.txt')
#     #if i==500:
#     #print "training complete"
#     #text =obj=preProcessing('samples/sample(0)/node'+str(i)+'.jpg')
#     #print i
#         # obj=preProcessing(img)
#         # text = obj.preProcessImage()
#         # npaFlattenedImages= np.append(npaFlattenedImages, [npaFlattenedImage],0)
# npaClassifications = npaClassifications.reshape((npaClassifications.size, 1))
# np.savetxt ("classification.txt", npaClassifications)
# print len(npaClassifications), npaClassifications.shape
# npaClassification = np.array(npaClassification,np.float32)
# # npaClassifications = np.array(npaClassifications,np.float32)
# # npaFlattenedImages = np.loadtxt("flattened_text.txt", np.float32)
# npaClassifications = np.append (npaClassifications, npaClassification, 0)
# print len(npaClassifications), npaClassifications.shape

# npaClassification = np.append (npaClassification, npaClassification, 0)
# npaClassification = npaClassification.reshape((npaClassification.size, 1))
# npaClassifications = np.append()

# np.savetxt("classification.txt", npaClassifications)
print len(npaClassifications), npaClassifications.shape
print len(npaFlattenedImages), npaFlattenedImages.shape
# cv2.waitKey(0)
cv2.destroyAllWindows()
        
