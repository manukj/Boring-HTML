import cv2
import os
from os import walk
for files in os.listdir(os.getcwd()):
	print(files)
	if(".jpg" in files):
		image = cv2.imread(files)
		image = cv2.resize(image,None,fx=0.125, fy=0.125, interpolation=cv2.INTER_AREA)
		cv2.imwrite(files,image)
