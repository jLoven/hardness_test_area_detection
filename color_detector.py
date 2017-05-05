# Jackie Loven
# 2 May 2017
# Thanks Odell for the advice!

import argparse
import cv2
import numpy as np
import imutils
from imutils import contours
import os

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
ap.add_argument("-i", "--image", required=True, 
	help="path to the input image")
ap.add_argument("-si", "--size", required=True, 
	help="size of scale bar in image")
ap.add_argument("-sa", "--sample", required=True, 
	help="sample composition")
args = vars(ap.parse_args())
#image = cv2.imread("images/" + args["image"])
image = cv2.imread(args["image"])
size = args["size"]
imageCopy1 = image.copy()
imageCopy2 = image.copy()

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
RED_MAX = np.array([136, 117, 253], np.uint8)
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
	display(imageToDrawOn, "", 0.25)
	return relevantContour

def find_rect(image, cnt):
	rect = cv2.minAreaRect(cnt)
	box = cv2.cv.BoxPoints(rect)
	box = np.int0(box)
	cv2.drawContours(image,[box],0,(255, 0, 0),2)

imageInfoList = grab_image_data(args["image"])
if len(imageInfoList) == 4:
	print("load: " + str(imageInfoList[0]) + " number: " + str(imageInfoList[1]) +
		" C.S. area: " + str(imageInfoList[2]) + " surface area: " + str(imageInfoList[3]))
	invertImage1 = grab_color(imageCopy1, RED_MIN, RED_MAX)
	display(invertImage1, "", 0.25)
	invertImage2 = grab_color(imageCopy2, GREEN_MIN, GREEN_MAX)
	display(invertImage2, "", 0.25)
	editImage1 = erode_dilate_canny_blur(invertImage2, kernel)
	display(editImage1, "", 0.25)
	editImage2 = canny_image(invertImage1)
	display(editImage2, "", 0.25)
	relevantContour1 = find_contours(editImage1, imageCopy1)
	relevantContour2 = find_contours(editImage2, imageCopy1)
	#find_rect(imageCopy1, relevantContour1)
	x, y, w, h = cv2.boundingRect(relevantContour2)
	pixelsPerMetric = float(size) / float(w)
	contourArea = cv2.contourArea(relevantContour1)
	areaInMicrons = contourArea * pixelsPerMetric * pixelsPerMetric

	cv2.imwrite("generated_images/" + args["sample"] + "_" + str(imageInfoList[1]) 
		+ ".png", imageCopy1)
	print("area: " + str(areaInMicrons))






