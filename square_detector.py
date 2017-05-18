# Jackie Loven
# 17 May 2017
# Thanks Odell for the advice!

import argparse
import cv2
import numpy as np
import imutils
from imutils import contours
import os
import shutil
from color_detector import display, auto_canny, grab_image_data, grab_color, erode_dilate_canny_blur, canny_image, find_contours


ap = argparse.ArgumentParser()
ap.add_argument("-di", "--directory", required=True, 
	help="path to the input image")
ap.add_argument("-si", "--size", required=True, 
	help="size of scale bar in image")
ap.add_argument("-sa", "--sample", required=True, 
	help="sample composition")
args = vars(ap.parse_args())
size = args["size"]

#BGR
#RGB
RED_MIN = np.array([0, 0, 209], np.uint8)
RED_MAX = np.array([136, 117, 255], np.uint8)
GREEN_MIN = np.array([52, 200, 38], np.uint8)
GREEN_MAX = np.array([115, 245, 110], np.uint8)

kernel = np.ones((7, 7), np.uint8)

def manipulate_image(filename, imageInfoList):
	image = cv2.imread(args["directory"] + filename)
	imageCopy1 = image.copy()
	imageCopy2 = image.copy()
	invertImage1 = grab_color(imageCopy1, RED_MIN, RED_MAX)
	invertImage2 = grab_color(imageCopy2, GREEN_MIN, GREEN_MAX)
	editImage1 = erode_dilate_canny_blur(invertImage2, kernel)
	editImage2 = canny_image(invertImage1)
	relevantContour1 = find_contours(editImage1, imageCopy1)
	relevantContour2 = find_contours(editImage2, imageCopy1)
	# GET SOME SORT OF BOUDNING QUADRILATERAL ON RELCONTOUR1


	x, y, w, h = cv2.boundingRect(relevantContour2)
	pixelsPerMetric = float(size) / float(w)
	contourArea = cv2.contourArea(relevantContour1)
	areaInMicrons = contourArea * pixelsPerMetric * pixelsPerMetric
	# save image somewhere
	generatedImageDirectoryName = os.path.expanduser("~/opencv-2.4.9/samples/python2/hardness_test/generated_images/") + args["sample"] + "_square"
	if os.path.exists(generatedImageDirectoryName):
		shutil.rmtree(generatedImageDirectoryName)
	os.makedirs(generatedImageDirectoryName)
	cv2.imwrite("generated_images/" + args["sample"] + "_square" + "/" + str(imageInfoList[0]) + "_" 
		+ str(imageInfoList[1]) + "_square.png", imageCopy1)
	return areaInMicrons

def images_in_directory(directory):
	directoryName = os.path.expanduser("~/opencv-2.4.9/samples/python2/hardness_test/generated_images/") + args["sample"] + "_square"
	if os.path.exists(directoryName):
		shutil.rmtree(directoryName)
	os.makedirs(directoryName)

	currentFile = open("generated_files/" + args["sample"] + "_square.txt", "w")
	line = "Load" + "\t" + "Indent Number" + "\t" + "My Area" + "\t" + "Keyence Area" + "\t" + "Keyence Surface Area" + "\n"
	currentFile.write(line)
	for filename in os.listdir(directory):
		print(filename + " filename")
		imageInfoList = grab_image_data(filename)
	    	if len(imageInfoList) == 4:
			areaInMicrons = manipulate_image(filename, imageInfoList)
			dataLine = str(imageInfoList[0]) + "\t" + str(imageInfoList[1]) + "\t" + str(areaInMicrons) + "\t" + str(imageInfoList[2]) + "\t" + str(imageInfoList[3])
			currentFile.write(dataLine + "\n")
	currentFile.close()





images_in_directory(args["directory"])

