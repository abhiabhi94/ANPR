import cv2
import operator
import numpy as np

MIN_CONTOUR_AREA = 200.0
MAX_CONTOUR_AREA = 500.0
RESIZED_IMAGE_WIDTH = 28
RESIZED_IMAGE_HEIGHT = 28
PATH = 'testImages/sample9.jpg'

class ContourWithData():

	foundContours = None           # contour
	boundingRect = None         # bounding rect for contour
	intRectX = 0                # bounding rect top left corner x location
	intRectY = 0                # bounding rect top left corner y location
	intRectWidth = 0            # bounding rect width
	intRectHeight = 0           # bounding rect height
	fltArea = 0.0               # area of contour

	def calculateRectTopLeftPointAndWidthAndHeight(self):               # calculate bounding rect info
		
		[intX, intY, intWidth, intHeight] = self.boundingRect
		self.intRectX = intX
		self.intRectY = intY
		self.intRectWidth = intWidth
		self.intRectHeight = intHeight


	def checkIfContourIsValid(self):                            # contour selection
		ratio = float( self.intRectWidth ) / self.intRectHeight
		if ratio > 3  and ratio < 5 and (self.fltArea > MIN_CONTOUR_AREA and self.fltArea < MAX_CONTOUR_AREA) : return True        # much better validity checking would be necessary
		return False 


def preprocessing(img):

	imgCopy=img.copy()
	img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	imgGrayCopy=img.copy()
	imgBlur = cv2.medianBlur(img, 1, 0)
	otsuReturn, imgThresh = cv2.threshold ( imgBlur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
	imgThreshCopy = imgThresh.copy()
	imgMorphed = cv2.morphologyEx(imgThresh, cv2.MORPH_OPEN, (5, 5))
	edge = cv2.Canny (imgBlur, 100, 255 )
	cv2.imshow("Number Plates detected", edge)
	return edge, imgGrayCopy, imgCopy


def main():

	img = cv2.imread(PATH)
	imgShape = img.shape [:2]
	resizingParameter = imgShape[1] / 1000.0 if (imgShape[1] > imgShape[0]) else imgShape[0] / 1000.0
	increment = 0.2

	for counter in xrange(1, 20, 1):

		allContoursWithData = []
		validContoursWithData = []
		platesContour = []
		crossingContour = []
		imgResized = cv2.resize(img, ( int(imgShape[1] / resizingParameter), int(imgShape[0] / resizingParameter)))
		edge, imgGrayCopy, imgCopy = preprocessing (imgResized)
		Contour, Hierarchy  = cv2.findContours ( edge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE )

		for foundContours in Contour:

			contourWithData = ContourWithData()                                             # instantiate a contour with data object
			contourWithData.foundContours = foundContours                                         # assign contour to contour with data
			contourWithData.boundingRect = cv2.boundingRect( contourWithData.foundContours)     # get the bounding rect
			contourWithData.calculateRectTopLeftPointAndWidthAndHeight()                    # get bounding rect info
			contourWithData.fltArea = cv2.contourArea( contourWithData.foundContours)           # calculate the contour area
			allContoursWithData.append (contourWithData)

		for contourWithData in allContoursWithData: 

			[intX,intY,intWidth,intHeight] = contourWithData.boundingRect
			ratio = float( intWidth ) / intHeight
			meanVal = cv2.mean (imgCopy)

			if (contourWithData.checkIfContourIsValid()):
				print contourWithData.fltArea, ratio, meanVal[:3] 
				cv2.rectangle(imgCopy, (contourWithData.intRectX, contourWithData.intRectY), (contourWithData.intRectX + contourWithData.intRectWidth, contourWithData.intRectY + contourWithData.intRectHeight ),( 255, 255, 0 ),2 )
				platesContour.append(contourWithData)
			

		cv2.imshow("Contours After Edge Detection", imgCopy )
		ch = chr(cv2.waitKey(0) & 255)

		if (ch == 'y'):
			print counter

			i = 0

			for validPlatesContour in platesContour:
				i+=1
				contourCharacters=[]
				# cv2.rectangle (img, (Data.intRectX, Data.intRectY), (Data.intRectX + Data.intRectWidth, Data.intRectY + Data.intRectHeight),(0, 255, 0),2)
				imgROI = img [validPlatesContour.intRectY * resizingParameter : (validPlatesContour.intRectY + validPlatesContour.intRectHeight ) * resizingParameter, validPlatesContour.intRectX * resizingParameter : (validPlatesContour.intRectX + validPlatesContour.intRectWidth) * resizingParameter]
				cv2.imshow('Detected Contours'+str(i), imgROI)
				imgROICopy = imgROI.copy()
				imgROIBlurred = cv2.medianBlur (imgROI, 1, 0)
				imgROIGray = cv2.cvtColor (imgROIBlurred, cv2.COLOR_BGR2GRAY)
				
				threshPlate = cv2.adaptiveThreshold(imgROIGray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,  11, 2)
				contourInNumberPlate, contourHierarchy = cv2.findContours (threshPlate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
				cv2.drawContours (imgROI , contourInNumberPlate, -1, (0, 0, 255), 2)
				cv2.imshow ("Contour in Threshed Plated", threshPlate)
				cv2.imshow ("Contours in Number Plate", imgROI)

				cv2.waitKey(0)

				for foundContours in contourInNumberPlate:

					plateContourWithData = ContourWithData()                                             # instantiate a contour with data object
					plateContourWithData.foundContours = foundContours                                         # assign contour to contour with data
					plateContourWithData.boundingRect = cv2.boundingRect (plateContourWithData.foundContours)     # get the bounding rect
					plateContourWithData.calculateRectTopLeftPointAndWidthAndHeight ()                    # get bounding rect info
					plateContourWithData.fltArea = cv2.contourArea (plateContourWithData.foundContours)           # calculate the contour area
					contourCharacters.append (plateContourWithData)

				contourCharacters.sort( key = operator.attrgetter("intRectX"))

				c = 0

				for validCharacters in contourCharacters:
					characterRatio = float (validCharacters.intRectWidth) / validCharacters.intRectHeight

					if (validCharacters.fltArea > 10 and validCharacters.fltArea < 100 and characterRatio > 0.25 and characterRatio < 0.75):
						c += 1
						# cv2.rectangle(imgROICopy, (validCharacters.intRectX, validCharacters.intRectY), ((validCharacters.intRectX + validCharacters.intRectWidth), (validCharacters.intRectY + validCharacters.intRectHeight) ), (255,0,125),2)
						character = imgROICopy [validCharacters.intRectY : validCharacters.intRectY + validCharacters.intRectHeight , validCharacters.intRectX : validCharacters.intRectX + validCharacters.intRectWidth ]
						# cv2.namedWindow("Characters in Number Plate", cv2.WINDOW_NORMAL)
						cv2.imwrite("ML/data/char_"+str(c)+".jpg", cv2.resize(character,(RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT)))
						# cv2.waitKey(0)
						
				print "Total characters detected in number plate:", c

				cv2.waitKey(0)







			break

		resizingParameter += increment


main()