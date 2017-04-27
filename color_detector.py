# Jackie Loven
# 20 April 2017
# Thanks Odell for the advice!

import argparse
import cv2
import numpy as np
import imutils
from imutils import contours

def display(img, name="img"):
    """Displays a window with an image.
    Press space while focussed on the window to move on."""
    cv2.imshow(name, img)
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
args = vars(ap.parse_args())
image = cv2.imread("images/" + args["image"])
size = args["size"]
imageCopy1 = image.copy()
imageCopy2 = image.copy()

#GBR
#BGR
#RGB
RED_MIN = np.array([40, 40, 200], np.uint8)
RED_MAX = np.array([120, 120, 250], np.uint8)
GREEN_MIN = np.array([60, 160, 80], np.uint8)
GREEN_MAX = np.array([130, 195, 140], np.uint8)

def grab_color(image, minimum, maximum):
	dst = cv2.inRange(image, minimum, maximum)
	opposite = cv2.countNonZero(dst)
	invertImage = cv2.bitwise_not(dst)
	return invertImage

invertImage1 = grab_color(imageCopy1, RED_MIN, RED_MAX)
invertImage2 = grab_color(imageCopy2, GREEN_MIN, GREEN_MAX)

kernel = np.ones((7, 7), np.uint8)

def erode_dilate_canny_blur(image, kernel):
	erodeImage = cv2.erode(image, kernel, iterations = 1)
	dilateImage = cv2.dilate(erodeImage, kernel, iterations = 1)
	cannyImage = auto_canny(dilateImage)
	blurImage = cv2.GaussianBlur(cannyImage, (3, 3), 0)
	return blurImage


editImage1 = erode_dilate_canny_blur(invertImage1, kernel)
editImage2 = erode_dilate_canny_blur(invertImage2, kernel)

def find_contours(image, imageToDrawOn):
	cnts = cv2.findContours(image, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	(cnts, _) = contours.sort_contours(cnts)
	relevantContour = cnts[0]
	cv2.drawContours(imageToDrawOn, [relevantContour], 0, (0, 255, 127), 2)
	return relevantContour

relevantContour1 = find_contours(editImage1, imageCopy1)
relevantContour2 = find_contours(editImage2, imageCopy1)

def find_rect(image, cnt):
	rect = cv2.minAreaRect(cnt)
	box = cv2.cv.BoxPoints(rect)
	box = np.int0(box)
	cv2.drawContours(image,[box],0,(255, 0, 0),2)

find_rect(imageCopy1, relevantContour1)
x, y, w, h = cv2.boundingRect(relevantContour2)



#print('Indent area is ' + cv2.contourArea(cnts[0]))
display(imageCopy1, "width is " + str(w))


