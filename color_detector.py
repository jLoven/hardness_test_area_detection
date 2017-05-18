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

def display(img, name="img", size=1.0):
    	"""Displays a window with an image.
    	Press space while focussed on the window to move on."""
	small = cv2.resize(img, (0, 0), fx = size, fy = size)
	cv2.imshow(name, small)
    	cv2.waitKey(0)
    	cv2.destroyAllWindows()

# Following function is from https://goo.gl/E9F4m8 :
def auto_canny(image, sigma = 0.33):
	# compute the median of the single channel pixel intensities
	v = np.median(image)
	# apply automatic Canny edge detection using the computed median
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)
	# return the edged image
	return edged

ap = argparse.ArgumentParser()
ap.add_argument("-di", "--directory", required=True, 
	help="path to the input image")
ap.add_argument("-si", "--size", required=True, 
	help="size of scale bar in image")
ap.add_argument("-sa", "--sample", required=True, 
	help="sample composition")
args = vars(ap.parse_args())
size = args["size"]

def grab_image_data(path):
	imageName = os.path.split(path)[-1]
	name, ext = imageName.split(".png")
	listOfNums = name.split("_")
	emptyList = []
	if len(listOfNums) == 4:
		listOfNums[0] = int(listOfNums[0])
		listOfNums[1] = int(listOfNums[1])
		listOfNums[2] = float(listOfNums[2])
		listOfNums[3] = float(listOfNums[3])
		return listOfNums
	else: return emptyList

#BGR
#RGB
RED_MIN = np.array([0, 0, 209], np.uint8)
RED_MAX = np.array([136, 117, 255], np.uint8)
GREEN_MIN = np.array([52, 200, 38], np.uint8)
GREEN_MAX = np.array([115, 245, 110], np.uint8)

kernel = np.ones((7, 7), np.uint8)

def grab_color(image, minimum, maximum):
	dst = cv2.inRange(image, minimum, maximum)
	opposite = cv2.countNonZero(dst)
	invertImage = cv2.bitwise_not(dst)
	return invertImage

def erode_dilate_canny_blur(image, kernel):
	erodeImage = cv2.erode(image, kernel, iterations = 1)
	dilateImage = cv2.dilate(erodeImage, kernel, iterations = 1)
	cannyImage = auto_canny(dilateImage)
	blurImage = cv2.GaussianBlur(cannyImage, (3, 3), 0)
	return blurImage

def canny_image(image):
	cannyImage = auto_canny(image)
	return cannyImage

def find_contours(image, imageToDrawOn):
	cnts = cv2.findContours(image, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	(cnts, _) = contours.sort_contours(cnts)
	relevantContour = cnts[0]
	cv2.drawContours(imageToDrawOn, [relevantContour], 0, (0, 255, 127), 2)
	return relevantContour

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
	x, y, w, h = cv2.boundingRect(relevantContour2)
	pixelsPerMetric = float(size) / float(w)
	contourArea = cv2.contourArea(relevantContour1)
	areaInMicrons = contourArea * pixelsPerMetric * pixelsPerMetric
	# save image somewhere
	cv2.imwrite("generated_images/" + args["sample"] + "/" + str(imageInfoList[0]) + "_" 
		+ str(imageInfoList[1]) + ".png", imageCopy1)
	if (abs(areaInMicrons - imageInfoList[2]) / imageInfoList[2]) > 0.1:
		cv2.imwrite("generated_images/debug/" + args["sample"] + "_" + str(imageInfoList[0]) + "_" + str(imageInfoList[1]) + ".png", imageCopy1)
	# return area
	return areaInMicrons

def images_in_directory(directory):
	directoryName = os.path.expanduser("~/opencv-2.4.9/samples/python2/hardness_test/generated_images/") + args["sample"]
	directoryName2 = os.path.expanduser("~/opencv-2.4.9/samples/python2/hardness_test/generated_images/") + "debug"
	if os.path.exists(directoryName):
		shutil.rmtree(directoryName)
	if os.path.exists(directoryName2):
		shutil.rmtree(directoryName2)
	os.makedirs(directoryName)
	os.makedirs(directoryName2)

	currentFile = open("generated_files/" + args["sample"] + ".txt", "w")
	line = "Load" + "\t" + "Indent Number" + "\t" + "My Area" + "\t" + "Keyence Area" + "\t" + "Keyence Surface Area" + "\n"
	currentFile.write(line)
	for filename in os.listdir(directory):
		print(filename + " filename + B")
		imageInfoList = grab_image_data(filename)
	    	if len(imageInfoList) == 4:
			areaInMicrons = manipulate_image(filename, imageInfoList)
			dataLine = str(imageInfoList[0]) + "\t" + str(imageInfoList[1]) + "\t" + str(areaInMicrons) + "\t" + str(imageInfoList[2]) + "\t" + str(imageInfoList[3])
			currentFile.write(dataLine + "\n")
	currentFile.close()


#images_in_directory(args["directory"])

