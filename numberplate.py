import cv2
import operator
import numpy as np

MIN_CONTOUR_AREA = 100.0
MAX_CONTOUR_AREA = 800.0
RESIZED_IMAGE_WIDTH = 28
RESIZED_IMAGE_HEIGHT = 28
PATH = 'testImages/car.jpg'


class ContourWithData():

	def __init__(self):

		self.contourCharacters = None
		self.foundContours = None           # contour
		self.boundingRect = None         # bounding rect for contour
		self.intRectX = 0                # bounding rect top left corner x location
		self.intRectY = 0                # bounding rect top left corner y location
		self.intRectWidth = 0            # bounding rect width
		self.intRectHeight = 0           # bounding rect height
		self.fltArea = 0.0               # area of contour
		self.id = False

	def calculateRectTopLeftPointAndWidthAndHeight(self):               # calculate bounding rect info
		
		[intX, intY, intWidth, intHeight] = self.boundingRect
		self.intRectX = intX
		self.intRectY = intY
		self.intRectWidth = intWidth
		self.intRectHeight = intHeight


	def checkIfContourIsValid(self):                            # contour selection
		aspectRatioNumberPlate = float( self.intRectWidth ) / self.intRectHeight
		if (aspectRatioNumberPlate > 1.5  and aspectRatioNumberPlate < 6 and (self.fltArea > MIN_CONTOUR_AREA and self.fltArea < MAX_CONTOUR_AREA)) : return True        # much better validity checking would be necessary
		return False 

	def getID(self):
		self.id = True


### Preprocessing ###

def preprocessing(img):

	imgCopy = img.copy()
	imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	imgGrayCopy = imgGray.copy()
	imgBlur = cv2.medianBlur(imgGray, 1, 0)
	otsuReturn, imgThresh = cv2.threshold ( imgBlur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
	imgThreshCopy = imgThresh.copy()
	imgMorphed = cv2.morphologyEx(imgThresh, cv2.MORPH_OPEN, (5, 5))
	edge = cv2.Canny (imgBlur, 100, 255 )
	# cv2.imshow("Number Plates detected", edge)
	return edge, imgGrayCopy, imgCopy



def numberPlateCategorization(sumBGR , characterCount):

	sumBGR = sumBGR / characterCount
	if(sumBGR[0] > 127 and sumBGR[1] > 127 and sumBGR[2] > 127):
		print "white"
	elif(sumBGR[0] <= 127 and sumBGR[1] <= 127 and sumBGR[2] <= 127):
		print "black"
	elif(sumBGR[0] > 127 and sumBGR[1] <= 127 and sumBGR[2] <= 127):
		print "blue"
	elif(sumBGR[0] <= 127 and sumBGR[1] <= 127 and sumBGR[2] > 127):
		print "red"
	else:
		print "yellow"
	# print image, image.shape, x, y
	# print "pixel value:",image[y-5][x]
	# for i in range(3):
	# 	sumBGR[i] = sumBGR[i] + image[y-5][x][i]
	# numberPlateBlurred = cv2.medianBlur (character, 1, 0)
	# M = cv2.moments(character)
	# cx = M['m']

	# threshValue, numberPlateThreshed = cv2.threshold (numberPlateBlurred, 120, 255, cv2.THRESH_BINARY)
	# colorsCount ={}
	# (R, G, B) = cv2.split(numberPlateBlurred)
	# R = R.flatten()
	# G = G.flatten()
	# B = B.flatten()

	# for i in xrange (len(R)):

	# 	RGB = str(R[i]) + str(G[i]) + str(B[i])

	# 	if (RGB in colorsCount):
	# 		colorsCount[RGB] +=1

	# 	else:
	# 		colorsCount[RGB] = 1

	# print colorsCount
	# cv2.imshow("fuck", numberPlateThreshed)


	# cv2.waitKey(0)

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
		imgResizedCopy = imgResized.copy()
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
				
				if (plateContourWithData.fltArea > 10 and plateContourWithData.fltArea < 100 and characterRatio > 0.1 and characterRatio < 0.9):
					characters.append (plateContourWithData)

			if (len(characters) > 7 and len(characters) < 11):
				cv2.rectangle(imgCopy, (possiblyValidContour.intRectX, possiblyValidContour.intRectY), (possiblyValidContour.intRectX + possiblyValidContour.intRectWidth, possiblyValidContour.intRectY + possiblyValidContour.intRectHeight ),( 0, 255, 0 ),2 )
				possiblyValidContour.contourCharacters = characters
				possiblyValidContour.getID()
				sahiWaliNoPlate.append (possiblyValidContour)

		cv2.imshow("number plates detected", imgCopy )
		cv2.waitKey(0)

		noOfPlatesDetected = 0
		sahiWaliNoPlate.sort ( key = operator.attrgetter("intRectX"))
		print "Total sahi wali plates detected:", len(sahiWaliNoPlate)

		### Going through the Number Plates found ###
		for noPlate in sahiWaliNoPlate:

			imgROI = img [noPlate.intRectY * resizingParameter : (noPlate.intRectY + noPlate.intRectHeight ) * resizingParameter, noPlate.intRectX * resizingParameter : (noPlate.intRectX + noPlate.intRectWidth) * resizingParameter]
			
			
			noOfPlatesDetected +=1
			noPlate.contourCharacters.sort( key = operator.attrgetter("intRectX"))

			characterCount = 0
			sumBGR = np.zeros(3)

			for validCharacters in noPlate.contourCharacters:

				characterCount += 1
				characters = imgROI [validCharacters.intRectY : (validCharacters.intRectY + validCharacters.intRectHeight) , validCharacters.intRectX : (validCharacters.intRectX + validCharacters.intRectWidth) ]
				
				for i in range(3):

					sumBGR[i] = sumBGR[i] + imgROI[validCharacters.intRectY-1][validCharacters.intRectX-1][i]

				cv2.imshow("Char"+str(characterCount)+".jpg", characters)
				cv2.waitKey(0)
					
			print "Total characters detected in number plate:", characterCount
			print "avg: ",sumBGR/characterCount
			numberPlateCategorization (sumBGR,characterCount)
			cv2.waitKey(0)

		if (noOfPlatesDetected > 0):
			print "No. of Number Plates Detected:",noOfPlatesDetected
			break

		else:

			resizingParameter += increment


main()                   