import cv2
import operator
import numpy as np

MIN_CONTOUR_AREA = 200.0
MAX_CONTOUR_AREA = 800.0
RESIZED_IMAGE_WIDTH = 28
RESIZED_IMAGE_HEIGHT = 28
PATH = 'testImages/car.jpg'

class ContourWithData():

	contourCharacters = None
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
		aspectRatioNumberPlate = float( self.intRectWidth ) / self.intRectHeight
		if (aspectRatioNumberPlate > 2  and aspectRatioNumberPlate < 5 and (self.fltArea > MIN_CONTOUR_AREA and self.fltArea < MAX_CONTOUR_AREA)) : return True        # much better validity checking would be necessary
		return False 


### Preprocessing ###

def preprocessing(img):

	imgCopy=img.copy()
	img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	imgGrayCopy=img.copy()
	imgBlur = cv2.medianBlur(img, 1, 0)
	otsuReturn, imgThresh = cv2.threshold ( imgBlur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
	imgThreshCopy = imgThresh.copy()
	imgMorphed = cv2.morphologyEx(imgThresh, cv2.MORPH_OPEN, (5, 5))
	edge = cv2.Canny (imgBlur, 100, 255 )
	# cv2.imshow("Number Plates detected", edge)
	return edge, imgGrayCopy, imgCopy


def main():

	img = cv2.imread(PATH)
	imgShape = img.shape [:2]
	resizingParameter = imgShape[1] / 1000.0 if (imgShape[1] > imgShape[0]) else imgShape[0] / 1000.0
	increment = 0.2

	for counter in xrange(1, 20, 1):

		### Resizing the Image and initializing the variables ###

		allContoursWithData = []
		validContoursWithData = []
		possiblePlateContour = []
		sahiWaliNoPlate = []
		# crossingContour = []
		imgResized = cv2.resize(img, ( int(imgShape[1] / resizingParameter), int(imgShape[0] / resizingParameter)))
		edge, imgGrayCopy, imgCopy = preprocessing (imgResized)
		Contour, Hierarchy  = cv2.findContours ( edge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE )

		### Assigning Attributes to the object ###

		for foundContours in Contour:

			contourWithData = ContourWithData()                                             # instantiate a contour with data object
			contourWithData.foundContours = foundContours                                         # assign contour to contour with data
			contourWithData.boundingRect = cv2.boundingRect( contourWithData.foundContours)     # get the bounding rect
			contourWithData.calculateRectTopLeftPointAndWidthAndHeight()                    # get bounding rect info
			contourWithData.fltArea = cv2.contourArea( contourWithData.foundContours)           # calculate the contour area
			allContoursWithData.append (contourWithData)

	### Checking for possible contour of the number plate based upon the aspect ratio and area ###
		
		for contourWithData in allContoursWithData: 

			if (contourWithData.checkIfContourIsValid()):
				possiblePlateContour.append(contourWithData)
			


		i = 0
### Checking for possible valid characters in Probable Number Plates ###

		for possiblyValidContour in possiblePlateContour:
			i+=1
			# cv2.rectangle (img, (Data.intRectX, Data.intRectY), (Data.intRectX + Data.intRectWidth, Data.intRectY + Data.intRectHeight),(0, 255, 0),2)
			imgROI = img [possiblyValidContour.intRectY * resizingParameter : (possiblyValidContour.intRectY + possiblyValidContour.intRectHeight ) * resizingParameter, possiblyValidContour.intRectX * resizingParameter : (possiblyValidContour.intRectX + possiblyValidContour.intRectWidth) * resizingParameter]
			# cv2.imshow('Possibly Valid Contours of the Number Plate'+str(i), imgROI)
			# cv2.waitKey(0)
			imgROICopy = imgROI.copy()
			imgROIBlurred = cv2.medianBlur (imgROI, 1, 0)
			imgROIGray = cv2.cvtColor (imgROIBlurred, cv2.COLOR_BGR2GRAY)
			
			threshPlate = cv2.adaptiveThreshold (imgROIGray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,  11, 2)
			contourInNumberPlate, contourHierarchy = cv2.findContours (threshPlate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

			### Assigning attributes to the objects corresponding to every contours found and checking whether the possible contour is valid or not ###
			
			characters = []

			for foundContours in contourInNumberPlate:

				plateContourWithData = ContourWithData()                                             # instantiate a contour with data object
				plateContourWithData.foundContours = foundContours                                         # assign contour to contour with data
				plateContourWithData.fltArea = cv2.contourArea (plateContourWithData.foundContours)           # calculate the contour area
				plateContourWithData.boundingRect = cv2.boundingRect (plateContourWithData.foundContours)     # get the bounding rect
				plateContourWithData.calculateRectTopLeftPointAndWidthAndHeight ()                    # get bounding rect info
				characterRatio = float (plateContourWithData.intRectWidth) / plateContourWithData.intRectHeight   # get aspect ratio
				
				if (plateContourWithData.fltArea > 10 and plateContourWithData.fltArea < 100 and characterRatio > 0.2 and characterRatio < 0.8):
					characters.append (plateContourWithData)

			if (len (characters) > 7 and len(characters) < 11):
				cv2.rectangle(imgCopy, (possiblyValidContour.intRectX, possiblyValidContour.intRectY), (possiblyValidContour.intRectX + possiblyValidContour.intRectWidth, possiblyValidContour.intRectY + possiblyValidContour.intRectHeight ),( 0, 255, 0 ),2 )
				possiblyValidContour.contourCharacters = characters
				sahiWaliNoPlate.append (possiblyValidContour)

		cv2.imshow("number plates detected", imgCopy )
		cv2.waitKey(0)

		noOfPlatesDetected = 0
		sahiWaliNoPlate.sort( key = operator.attrgetter("intRectX"))
		print "Total sahi wali plates detected:", len(sahiWaliNoPlate)

		### Going through the Number Plates found ###
		for noPlate in sahiWaliNoPlate:

			imgROI = img [noPlate.intRectY * resizingParameter : (noPlate.intRectY + noPlate.intRectHeight ) * resizingParameter, noPlate.intRectX * resizingParameter : (noPlate.intRectX + noPlate.intRectWidth) * resizingParameter]
			noOfPlatesDetected +=1
			noPlate.contourCharacters.sort( key = operator.attrgetter("intRectX"))

			characterCount = 0

			for validCharacters in noPlate.contourCharacters:

				characterCount += 1
				characters = imgROI [validCharacters.intRectY : (validCharacters.intRectY + validCharacters.intRectHeight) , validCharacters.intRectX : (validCharacters.intRectX + validCharacters.intRectWidth) ]
				cv2.imshow("Char"+str(characterCount)+".jpg", characters)
				cv2.waitKey(0)
					
			print "Total characters detected in number plate:", characterCount

			cv2.waitKey(0)






		
		if (noOfPlatesDetected > 0):
			print "No. of Number Plates Detected:",noOfPlatesDetected
			break

		else:

			resizingParameter += increment


main()                   