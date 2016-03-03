import cv2
import operator
import numpy as np

MIN_CONTOUR_AREA = 800.0
MAX_CONTOUR_AREA = 4500.0
RESIZED_IMAGE_WIDTH = 20
RESIZED_IMAGE_HEIGHT = 20
MIN_CHARACTER_AREA = 100
MAX_CHARACTER_AREA = 1000
MIN_ASPECTRATIO = 3
MAX_ASPECTRATIO = 10
MIN_ASPECTRATIO_CHAR = 0.1
MAX_ASPECTRATIO_CHAR = 1.5
PATH = 'FINL/1.jpg'
FILE = "/tmp/numberPlateInfo.npy"
numberPlateCoordinates = []


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
		if (aspectRatioNumberPlate > MIN_ASPECTRATIO  and aspectRatioNumberPlate < MAX_ASPECTRATIO and (self.fltArea > MIN_CONTOUR_AREA and self.fltArea < MAX_CONTOUR_AREA)) : 
			# print aspectRatioNumberPlate
			return True        # much better validity checking would be necessary
		return False 

	def getID(self):
		self.id = True


### Preprocessing ###

def preprocessing(img):

	imgCopy = img.copy()

	imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	imgGrayCopy = imgGray.copy()
	imgBlur = cv2.medianBlur(imgGray, 3, 0)
	otsuReturn, imgThresh = cv2.threshold ( imgBlur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
	imgThreshCopy = imgThresh.copy()
	imgMorphed = cv2.morphologyEx(imgThresh, cv2.MORPH_OPEN, (5, 5))
	edge = cv2.Canny (imgBlur, 100, 255 )
	cv2.imshow("Number Plates detected", edge)
	return edge, imgGrayCopy, imgCopy

def writeToFile(resizingParameter):

	numberPlateCoordinates.append(resizingParameter)
	np.save(FILE, numberPlateCoordinates)



def numberPlateCategorization(sumBGR , characterCount):

	sumBGR = sumBGR / characterCount

	if(sumBGR[0] > 127 and sumBGR[1] > 127 and sumBGR[2] > 127):

		print "white : Personal Vehichle"

	elif(sumBGR[0] <= 127 and sumBGR[1] <= 127 and sumBGR[2] <= 127):

		print "black : Commercial Vehichle"

	elif(sumBGR[0] > 127 and sumBGR[1] <= 127 and sumBGR[2] <= 127):

		print "blue: Foreign Vehichle"

	elif(sumBGR[0] <= 127 and sumBGR[1] <= 127 and sumBGR[2] > 127):

		print "red : Official Car of Governers or President "

	else:

		print "yellow : Taxi"

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

def states(a):

	print "The vehicle belongs to the state:"

	if(a[0] == 'A' and a[1] == 'N'):

		print "Andaman and Nicobar"

	elif(a[0] == 'A' and a[1] == 'P'):

		print "Andhra Pradesh"

	elif(a[0] == 'A' and a[1] == 'R'):

		print "Arunachal Pradesh"

	elif(a[0] == 'A' and a[1] == 'S'):

		print "Assam"

	elif(a[0] == 'B' and a[1] == 'R'):

		print "Bihar"

	elif(a[0] == 'C' and a[1] == 'G'):

		print "Chattisgarh"

	elif(a[0] == 'C' and a[1] == 'H'):

		print "Chandigarh"

	elif(a[0] == 'R' and a[1] == 'J'):

		print "Rajasthan"

	elif(a[0] == 'G' and a[1] == 'J'):

		print "Gujarat"

	elif(a[0] == 'P' and a[1] == 'B'):

		print "Punjab"

	elif(a[0] == 'H' and a[1] == 'R'):

		print "Haryana"
	
	elif(a[0] == 'H' and a[1] == 'P'):
		
		print "Himachal Pradesh"
	
	elif(a[0] == 'T' and a[1] == 'R'):
		
		print "Tripura"
	
	elif(a[0] == 'W' and a[1] == 'B'):
		
		print "West Bengal"
	
	elif(a[0] == 'J' and a[1] == 'K'):
		
		print "Jammu and Kashmir"
	
	elif(a[0] == 'Q' and a[1] == 'Q'):
		
		print "Daman and Diu"
	
	elif(a[0] == 'U' and a[1] == 'K'):
		
		print "Uttrakhand"
	
	elif(a[0] == 'K' and a[1] == 'A'):
		
		print "Karnataka"
	
	elif(a[0] == 'L' and a[1] == 'Q'):
		
		print "Lakshwadeep"
	
	elif(a[0] == 'D' and a[1] == 'L'):
		
		print "Delhi"
	
	else:
		
		print "Not a State vehicle"

	if(a[2]%2):
		
		print "Odd"
	
	else:
		
		print "Even"


def OCR (img , position):

	if ( position == 1 or position == 2):

		npaClassifications = np.loadtxt ("classification_alphabets.txt", np.float32)
		npaFlattenedImages = np.loadtxt ("flattened_alphabets.txt", np.float32)

	else:
		npaClassifications = np.loadtxt("classification_numbers.txt", np.float32)
		npaFlattenedImages = np.loadtxt("flattened_numbers.txt", np.float32)
	# print npaClassifications.shape, npaFlattenedImages.shape
	npaClassifications = npaClassifications.reshape((npaClassifications.size, 1))
	kNearest = cv2.KNearest()
	kNearest.train (npaFlattenedImages, npaClassifications)
	imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	imgBlurred = cv2.medianBlur(imgGray, 1, 0)
	imgThresh = cv2.adaptiveThreshold(imgBlurred,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)
	imgThresh = cv2.resize (imgThresh, (RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT))
	# print imgThresh.shape
	npaROIResized = np.float32(imgThresh.reshape((1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT )))
	# print npaROIResized.shape
	retval, npaResults, neigh_resp, dists = kNearest.find_nearest(npaROIResized, k = 1)
	
	if (retval >= 65):
		return chr(int(retval))

	else:
		return int(retval)

def main():

	img = cv2.imread(PATH)
	imgShape = img.shape [:2]
	resizingParameter = imgShape[1] / 1000.0 if (imgShape[1] > imgShape[0]) else imgShape[0] / 1000.0
	increment = 0.2

	for counter in xrange(1, 20):

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
				
				if (plateContourWithData.fltArea > MIN_CHARACTER_AREA and plateContourWithData.fltArea < MAX_CHARACTER_AREA and characterRatio > MIN_ASPECTRATIO_CHAR and characterRatio < MAX_ASPECTRATIO_CHAR):
					
					characters.append (plateContourWithData)

			if (len(characters) >= 5 and len(characters) < 11):

				cv2.rectangle(imgCopy, (possiblyValidContour.intRectX, possiblyValidContour.intRectY), (possiblyValidContour.intRectX + possiblyValidContour.intRectWidth, possiblyValidContour.intRectY + possiblyValidContour.intRectHeight ),( 0, 255, 0 ),2 )
				possiblyValidContour.contourCharacters = characters
				possiblyValidContour.getID()
				sahiWaliNoPlate.append (possiblyValidContour)

		cv2.imshow("number plates detected", imgCopy )
		cv2.waitKey(0)

		noOfPlatesDetected = 0
		sahiWaliNoPlate.sort ( key = operator.attrgetter("intRectX"))
		print "Total plates detected:", len(sahiWaliNoPlate)

		### Going through the Number Plates found ###
		for noPlate in sahiWaliNoPlate:

			imgROI = img [noPlate.intRectY * resizingParameter : (noPlate.intRectY + noPlate.intRectHeight ) * resizingParameter, noPlate.intRectX * resizingParameter : (noPlate.intRectX + noPlate.intRectWidth) * resizingParameter]
			numberPlateCoordinates.append([int(noPlate.intRectX * resizingParameter)  , int(noPlate.intRectY* resizingParameter) , int(noPlate.intRectHeight* resizingParameter) , int(noPlate.intRectWidth* resizingParameter) ])
			
			noOfPlatesDetected +=1
			noPlate.contourCharacters.sort( key = operator.attrgetter("intRectX"))

			characterCount = 0
			sumBGR = np.zeros(3)
			NP = []

			for validCharacters in noPlate.contourCharacters:

				characterCount += 1
				characters = imgROI [validCharacters.intRectY : (validCharacters.intRectY + validCharacters.intRectHeight) , validCharacters.intRectX : (validCharacters.intRectX + validCharacters.intRectWidth) ]
				cv2.imshow("character", characters)
				cv2.waitKey(0)
				
				if(characterCount == 1 or characterCount == 2 ):

					NP.append(OCR(characters, characterCount)) 
					# print NP

				for i in range(3):

					sumBGR[i] = sumBGR[i] + imgROI[validCharacters.intRectY-1][validCharacters.intRectX-1][i]

			NP.append(OCR(characters, characterCount)) 
			states(NP)

				# cv2.imwrite("Char"+str(characterCount)+".jpg", characters)
				# cv2.waitKey(0)
					
			print "Total characters detected in number plate:", characterCount
			# print "avg: ",sumBGR/characterCount
			numberPlateCategorization (sumBGR,characterCount)
			cv2.waitKey(0)

		if (len(sahiWaliNoPlate) > 0):

			break

		else:

			resizingParameter += increment
	
	# writeToFile(resizingParameter)

main()                   