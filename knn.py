def OCR (img , position):
	cv2.imshow("uhitgrhu", img)
	cv2.waitKey(0)
	if ( position == 0 or position == 1):

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
	imgThresh = cv2.resize (imgThresh, (20, 20))
	print imgThresh.shape
	npaROIResized = np.float32(imgThresh.reshape((1, 20 * 20 )))
	print npaROIResized.shape
	retval, npaResults, neigh_resp, dists = kNearest.find_nearest(npaROIResized, k = 1)
	if (retval > 65):
		print chr(int(retval))

	else:
		print int(retval)
