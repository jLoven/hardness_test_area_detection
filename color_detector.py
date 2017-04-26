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
imageCopy = image.copy()
display(imageCopy)

#GBR
#RGB
RED_MIN = np.array([40, 40, 200], np.uint8)
RED_MAX = np.array([120, 120, 250], np.uint8)
GREEN_MIN = np.array([175, 75, 90], np.uint8)
GREEN_MAX = np.array([195, 130, 140], np.uint8)

#display(imageCopy)
dst = cv2.inRange(imageCopy, RED_MIN, RED_MAX)
no_red = cv2.countNonZero(dst)
invertImage = cv2.bitwise_not(dst)
#display(invertImage)

dst2 = cv2.inRange(imageCopy, GREEN_MIN, GREEN_MAX)
no_green = cv2.countNonZero(dst2)
invertImage2 = cv2.bitwise_not(dst2)

kernel = np.ones((7, 7), np.uint8)
erodeImage1 = cv2.erode(invertImage, kernel, iterations = 1)
erodeImage2 = cv2.erode(invertImage2, kernel, iterations = 1)
#display(erodeImage1, "erode1")
dilateImage1 = cv2.dilate(erodeImage1, kernel, iterations = 1)
dilateImage2 = cv2.dilate(erodeImage2, kernel, iterations = 1)
display(dilateImage1, "dilate1")
display(dilateImage2, "dilate2")

cannyImage = auto_canny(dilateImage1)
cannyImage2 = auto_canny(dilateImage2)
blurredImage1 = cv2.GaussianBlur(cannyImage, (3, 3), 0)
blurredImage2 = cv2.GaussianBlur(cannyImage2, (3, 3), 0)
#display(blurredImage1)


# Find contours:
cnts = cv2.findContours(blurredImage1, 
	cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
cnts2 = cv2.findContours(blurredImage2, 
	cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
cnts2 = cnts2[0] if imutils.is_cv2() else cnts2[1]
(cnts, _) = contours.sort_contours(cnts)
(cnts2, _) = contours.sort_contours(cnts2)
relevantContour = cnts[0]
relevantContour2 = cnts2[0]
cv2.drawContours(imageCopy, [relevantContour], 0, (0, 255, 127), 2)
cv2.drawContours(imageCopy, [relevantContour2], 0, (0, 255, 127), 2)

rect = cv2.minAreaRect(relevantContour)
rect2 = cv2.minAreaRect(relevantContour2)
box = cv2.cv.BoxPoints(rect)
box2 = cv2.cv.BoxPoints(rect2)
box = np.int0(box)
box2 = np.int0(box2)
cv2.drawContours(imageCopy,[box],0,(255, 0, 0),2)
cv2.drawContours(imageCopy,[box2],0,(255, 255, 0),2)

#print('Indent area is ' + cv2.contourArea(cnts[0]))
display(imageCopy)


