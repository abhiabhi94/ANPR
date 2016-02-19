import cv2
import numpy as np

img = cv2.imread("font81.png",0)
cv2.imshow("fd",img)
cv2.waitKey(0)

x = 14	
y = 20

width =49
height = 100

noOfCharacters = 14
for i in range(noOfCharacters):
	# if( i == 1):
	# 	w = width - 30
	# elif( i == 5):
	# 	h = height + 8
	# elif( i == 9):
	# 	h = height + 8
	# else:
	# 	h = height
	# else:
	w = width
	# if(i == 6):
	# 	# cv2.imwrite("sample/"+str(i*10 + 1)+".jpg",img[y-4	:h, x : x + w - 7])
	# 	cv2.imwrite("sample/"+str(i)+"/5.png",cv2.resize(img[y-4:h, x : x + w - 7] , (28,28)))

	# cv2.imwrite("sample/"+str(unichr(i+78))+"/7.png",cv2.resize(img[y:height, x : x + w - 4] , (28,28)))
	# cv2.imwrite("sample/"+str(i)+"/7.png",cv2.resize(img[y:height, x : x + w] , (28,28)))
	cv2.imwrite("sample/"+str(i*10 + 1)+".jpg",img[y:height, x : x + w])


	# else:
	# 	cv2.imwrite("sample/"+str(i)+"/5.png",cv2.resize(img[y:h, x : x + w - 7] , (28,28)))
	# 	# cv2.imwrite("sample/"+str(i*10 + 1)+".jpg",img[y:h, x : x + w - 7])


	x = x + w
	# if( i == 11):
	# 	x = x-2
	# if( i == 5):
	# 	x = x-2


