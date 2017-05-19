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
from color_detector_methods import display, auto_canny, grab_image_data, grab_color, erode_dilate_canny_blur, canny_image, find_contours


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

def distance_formula(point1, point2):
	x1, y1 = point1
	x2, y2 = point2
	distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
	return distance

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
	# check out template matching at some point: http://docs.opencv.org/24
	# /doc/tutorials/imgproc/histograms/template_matching/template_matching.html
	#epsilon = 0.1 * cv2.arcLength(relevantContour1, True)
	#approx = cv2.approxPolyDP(relevantContour1, epsilon, True)
	#cv2.drawContours(imageCopy1, [approx], 0, (0, 0, 255), 2)

	# Grab all pixels inside contour. find extrema. draw a four sided shape.
	# For every pixel in the bounding box: 
	x, y, w, h = cv2.boundingRect(relevantContour1)
	centerPoint = (x + w / 2, y + h / 2)
	w1, w2 = centerPoint
	e1, e2 = centerPoint
	n1, n2 = centerPoint
	s1, s2 = centerPoint
	for i in range(x - 10, x + w + 10):
		for j in range (y - 10, y + h + 10):
			distanceSign = cv2.pointPolygonTest(relevantContour1, (i, j), False)
			if distanceSign > -1:
				if i > e1:
					e1 = i
					e2 = j
				if i < w1:
					w1 = i
					w2 = j
				if j > n2:
					n1 = i
					n2 = j
				if j < s2:
					s1 = i
					s2 = j
	n2 = n2 + 0
	s2 = s2 - 0
	e1 = e1 + 0
	w1 = w1 - 0
	north = (n1, n2)
	south = (s1, s2)
	east = (e1, e2)
	west = (w1, w2)
	# draw this shape in red:
	cv2.line(imageCopy1, north, east, (0, 0, 255), 2)
	cv2.line(imageCopy1, south, east, (0, 0, 255), 2)
	cv2.line(imageCopy1, south, west, (0, 0, 255), 2)
	cv2.line(imageCopy1, north, west, (0, 0, 255), 2)
	x, y, w, h = cv2.boundingRect(relevantContour2)
	pixelsPerMetric = float(size) / float(w)
	contourArea = cv2.contourArea(relevantContour1)
	areaInMicrons = contourArea * pixelsPerMetric * pixelsPerMetric
	# get box area
	avgDiagonal = (distance_formula(north, south) + distance_formula(east, west)) / 2
	areaOfBox = (avgDiagonal ** 2) * 0.5
	boxArea = areaOfBox * (pixelsPerMetric ** 2)
	# save image somewhere
	cv2.imwrite("generated_images/" + args["sample"] + "_square" + "/" + str(imageInfoList[0]) + "_" 
		+ str(imageInfoList[1]) + "_square.png", imageCopy1)
	return [areaInMicrons, boxArea]

def images_in_directory(directory):
	directoryName = os.path.expanduser("~/opencv-2.4.9/samples/python2/hardness_test/generated_images/") + args["sample"] + "_square"
	if os.path.exists(directoryName):
		shutil.rmtree(directoryName)
	os.makedirs(directoryName)
	generatedImageDirectoryName = os.path.expanduser("~/opencv-2.4.9/samples/python2/hardness_test/generated_images/") + args["sample"] + "_square"
	if os.path.exists(generatedImageDirectoryName):
		shutil.rmtree(generatedImageDirectoryName)
	os.makedirs(generatedImageDirectoryName)

	currentFile = open("generated_files/" + args["sample"] + "_square.txt", "w")
	line = "Load" + "\t" + "Indent Number" + "\t" + "My Area" + "\t" + "Keyence Area" + "\t" + "Keyence Surface Area" + "\t" + "My Box Area" + "\n"
	currentFile.write(line)
	for filename in os.listdir(directory):
		print(filename + " filename")
		imageInfoList = grab_image_data(filename)
	    	if len(imageInfoList) == 4:
			[areaInMicrons, boxArea] = manipulate_image(filename, imageInfoList)
			dataLine = str(imageInfoList[0]) + "\t" + str(imageInfoList[1]) + "\t" + str(areaInMicrons) + "\t" + str(imageInfoList[2]) + "\t" + str(imageInfoList[3]) + "\t" + str(boxArea)
			currentFile.write(dataLine + "\n")
	currentFile.close()


images_in_directory(args["directory"])

