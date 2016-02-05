import cv2
import operator
import numpy as np

MIN_CONTOUR_AREA = 300.0
MAX_CONTOUR_AREA = 600.0
RESIZED_IMAGE_WIDTH = 100
RESIZED_IMAGE_HEIGHT = 100

class ContourWithData():

    npaContour = None           # contour
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


    def checkIfContourIsValid(self):                            # this is oversimplified, for a production grade program
        if self.fltArea < MIN_CONTOUR_AREA or self.fltArea > MAX_CONTOUR_AREA : return False        # much better validity checking would be necessary
        return True



def main():

    allContoursWithData = []
    validContoursWithData = [];
    PlatesContour=[]
    crossingContour=[]

    img=cv2.resize(cv2.imread('car1.jpg'),(800,600))
    imgCopy=img.copy()
    img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgGrayCopy=img.copy()
    # imgBlurred = cv2.GaussianBlur(img, (5,5), 0)
    # cv2.imshow("Blurr",imgBlurred)
    ret,imgThresh = cv2.threshold(img,100,255,cv2.THRESH_BINARY_INV)     #for detecting car
    cv2.waitKey(0)
    cv2.imshow('imgThresh',imgThresh)
    imgThreshCopy = imgThresh.copy()
    # gx = cv2.Sobel(img, cv2.CV_32F, 1, 0)
    # gy = cv2.Sobel(img, cv2.CV_32F, 0, 1)
    # cv2.imshow("sobelx",gx)
    # cv2.imshow("sobely",gy)
    npaContours , npaHierarchy = cv2.findContours(imgThresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    # print len (npaContours)
    for npaContour in npaContours:
        contourWithData = ContourWithData()                                             # instantiate a contour with data object
        contourWithData.npaContour = npaContour                                         # assign contour to contour with data
        contourWithData.boundingRect = cv2.boundingRect(contourWithData.npaContour)     # get the bounding rect
        contourWithData.calculateRectTopLeftPointAndWidthAndHeight()                    # get bounding rect info
        contourWithData.fltArea = cv2.contourArea(contourWithData.npaContour)           # calculate the contour area
        allContoursWithData.append(contourWithData)
    # print allContoursWithData
    c=0
    for contourWithData in allContoursWithData: 

        [intX,intY,intWidth,intHeight] = contourWithData.boundingRect
        # if contourWithData.checkIfContourIsValid():
        ratio = float(intWidth)/intHeight
        if ( ratio > 2 and ratio < 5 ) :
            if contourWithData.checkIfContourIsValid():
                # contourWithData=np.array(contourWithData)
                print contourWithData.fltArea , ratio
                cv2.rectangle(imgCopy,(contourWithData.intRectX, contourWithData.intRectY),(contourWithData.intRectX + contourWithData.intRectWidth, contourWithData.intRectY + contourWithData.intRectHeight),(255, 255, 0),2)
                # cv2.drawContours(imgCopy,contourWithData.npaContour,-1,(255,255,0),2)
                c+=1
                print c
                PlatesContour.append(contourWithData)
    cv2.imshow("Number Plates",imgCopy)
    cv2.waitKey(0)
    validContoursWithData.sort(key = operator.attrgetter("intRectX"))
    i=0

    for contourWithData in validContoursWithData:
        i+=1
        cv2.rectangle(img,(contourWithData.intRectX, contourWithData.intRectY),(contourWithData.intRectX + contourWithData.intRectWidth, contourWithData.intRectY + contourWithData.intRectHeight),(0, 255, 0),2)
        imgROI = img[contourWithData.intRectY : contourWithData.intRectY + contourWithData.intRectHeight,contourWithData.intRectX : contourWithData.intRectX + contourWithData.intRectWidth]
        imgROIResized = cv2.resize(imgROI, (RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT))
        npaROIResized = imgROIResized.reshape((1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))
        # npaROIResized = imgROIResized.reshape((1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))
        cv2.namedWindow('Detected Contours'+str(i),cv2.WINDOW_NORMAL)
        cv2.imshow('Detected Contours'+str(i),imgROI)
        cv2.waitKey(0)



###### For Pedestrian Crossing

    ret1,imgThresh1 = cv2.threshold(img,150,255,cv2.THRESH_BINARY_INV)   # for detecting crossing
    cv2.imshow('Thresh 1',imgThresh1)
    imgThresh1Copy= imgThresh1.copy()
    edge = cv2.Canny( imgCopy , 100 , 200 )
    cv2.imshow("edges detected", imgThresh1 )
    edgesInContour , edgesHierarchy  = cv2.findContours(edge , cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE )
    # cv2.drawContours ( imgCopy , edgesInContour , -1 , (255,0,0) , 2 )
    cv2.waitKey(0)
    # mask = cv2.inRange ( imgCopy ,np.array ( [ 150,150,150 ] ),np.array ( [ 255,255,255 ] ) )
    # print mask
    # imgmask=cv2.bitwise_and ( imgCopy , imgCopy , mask=mask )
    # cv2.imshow ( "Masked Image" , imgThresh1Copy )
    # cv2.waitKey(0)
    # npaContours1 , npaHierarchy = cv2.findContours(imgmask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(imgCopy,npaContours1,-1,(255,0,255),2)

    for npaContour in edgesInContour:

        contourWithData = ContourWithData()                                             # instantiate a contour with data object
        contourWithData.npaContour = npaContour                                         # assign contour to contour with data
        contourWithData.boundingRect = cv2.boundingRect( contourWithData.npaContour )     # get the bounding rect
        contourWithData.calculateRectTopLeftPointAndWidthAndHeight()                    # get bounding rect info
        contourWithData.fltArea = cv2.contourArea( contourWithData.npaContour )           # calculate the contour area
        allContoursWithData.append ( contourWithData )

    for contourWithData in allContoursWithData: 

        [intX,intY,intWidth,intHeight] = contourWithData.boundingRect

        # if contourWithData.checkIfContourIsValid():
        ratio = float( intWidth ) / intHeight
        if ( ratio > 2  and ratio < 4 and contourWithData.fltArea > 1000.0 and contourWithData.fltArea < 1500.0 ):
        # if contourWithData.checkIfContourIsValid():
            # contourWithData=np.array(contourWithData)
            print contourWithData.fltArea , ratio , contourWithData.npaContour , len ( contourWithData.npaContour )
            # for i in xrange (len(contourWithData.npaContour)):
            #     print contourWithData.npaContour[i]
                # M = cv2.moments(contourWithData.npaContour[i])
                # cx1 = int( M['m10'] / M['m00'] )
                # cy1 = int( M['m01'] / M['m00'] )

                # cv2.drawContours(imgCopy,(cx1,cy1),2,(255,0,255),-1)
            cv2.rectangle(imgCopy,(contourWithData.intRectX , contourWithData.intRectY) , (contourWithData.intRectX + contourWithData.intRectWidth , contourWithData.intRectY + contourWithData.intRectHeight ),( 255, 255, 0 ),2 )

        # cv2.drawContours(imgCopy,contourWithData.npaContour,-1,(255,255,0),2)
        # c+=1
        # print c
        crossingContour.append(contourWithData)

    # x = crossingContour[0].intRectX + 2
    # y = crossingContour[0].intRectY + 2
    # X = x + crossingContour[-1]
    # Y = 
    # cv2.rectangle(imgCopy,() , (crossingContour[0].intRectX + 2 , ((crossingContour[-1].intRectX - crossingContour[0].intRectX) + crossingContour[-1].intWidth + 2 , (crossingContour[0].intRectY + 2 , ((crossingContour[-1].intRectY - crossingContour[0].intRectY) + crossingContour[-1].intWidth + 2 )
    # cv2.imshow("Crossings and number plate",imgCopy)
    cv2.imshow("Contours After Edge Detection", imgCopy )
    cv2.waitKey(0)


    


main()
