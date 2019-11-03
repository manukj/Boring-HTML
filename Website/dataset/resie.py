import cv2
import os
from os import walk
i = 0
for files in os.listdir(os.getcwd()):
	print(files)
	if(".jpg" in files):
#compress of image
		#image = cv2.imread(files)
		#image = cv2.resize(image,None,fx=0.125, fy=0.125, interpolation=cv2.INTER_AREA)
		#cv2.imwrite(files,image)
#rename of files
		i = i + 1
		image = cv2.imread(files)
		files = str(i) + ".jpg"
		print(files)	
		cv2.imwrite(files,image)

