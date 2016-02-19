import cv2

for i in range(6):

	for j in range(1):
		img = cv2.imread("sample/"+str(i)+"/7.png")
		# cv2.imshow("d",img)
		# cv2.waitKey(0)
		img = cv2.resize(img,(20,20))
		img = cv2.medianBlur(img,3,0)
		cv2.imwrite("sample/"+str(i)+"/7.png",img)
		# cv2.imshow("dh",img)
		# cv2.waitKey(0)