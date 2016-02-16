import cv2
import numpy as np
from skimage.feature import local_binary_pattern

img = cv2.imread ("testImages/car.jpg")
imgShape = img.shape [:2]
resizingParameter = imgShape[1] / 1000.0 if (imgShape[1] > imgShape[0]) else imgShape[0] / 1000.0
imgResized = cv2.resize(img, ( int(imgShape[1] / resizingParameter), int(imgShape[0] / resizingParameter)))
imgGray = cv2.cvtColor (imgResized, cv2.COLOR_BGR2GRAY)
imgBlurr = cv2.medianBlur (imgGray, 1, 0)
imgMorph = cv2.morphologyEx (imgBlurr, cv2.MORPH_OPEN, (5,5))
print imgMorph, imgMorph.shape
# edge = cv2.Canny (imgMorph , 100, 255)
radius = 30
no_points = 8
lbp = local_binary_pattern(imgMorph, no_points, radius, method = 'uniform')
lbp = lbp.astype(np.uint8)
thresh, lbpThresh = cv2.threshold (lbp, 1, 255, cv2.THRESH_BINARY_INV)
print lbpThresh.shape
cv2.imshow("fuckfuck", lbpThresh)
cv2.waitKey(0)
contours, hierarchy = cv2.findContours (lbpThresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for i in range(len(contours)-1):

	[RectX, RectY, RectWidth, RectHeight] = cv2.boundingRect(contours[i])
	aspectRatio = float(RectWidth) / RectHeight
	if(cv2.contourArea(contours[i]) > 1000 and cv2.contourArea(contours[i]) < 1500 and  aspectRatio > 1.5 and aspectRatio < 4.0):

		print cv2.contourArea(contours[i]) , aspectRatio

		cv2.rectangle(imgResized, (RectX, RectY), (RectX + RectWidth , RectY + RectHeight), (255,255,0), 2)

cv2.imshow ("Contours Found After LBP", imgResized)
cv2.waitKey(0)

		