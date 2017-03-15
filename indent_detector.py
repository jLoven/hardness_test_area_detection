# Jackie Loven
# 14 March 2017
# Thanks Odell for the advice!

import argparse
import cv2
import numpy as np
import imutils
from imutils import contours

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, 
	help="path to the input image")
args = vars(ap.parse_args())
image = cv2.imread(args["image"])
imageCopy = image.copy()

# 1. Convert to grayscale
grayImage = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2GRAY)

# 2. Simple Gaussian blur
# window size 7 x 7, exact
gaussianBlurImage1 = cv2.GaussianBlur(grayImage, (3, 3), 0)

# 3. Open (erode), close (dilate), open image
# https://goo.gl/nm8BXX for opening and closing docs
# https://goo.gl/RUhy32 for why you need to do uint8
kernel = np.ones((7, 7), np.uint8)
erodeImage1 = cv2.erode(gaussianBlurImage1, kernel, iterations = 1)
dilateImage1 = cv2.dilate(erodeImage1, kernel, iterations = 1)
erodeImage2 = cv2.erode(dilateImage1, kernel, iterations = 1)

# 4. CLAHE (Contrast Limited Adaptive Histogram Equalization)
# https://goo.gl/OjnwZC for a good explanation, it improves contrast
clahe = cv2.createCLAHE(clipLimit = 4.0, tileGridSize=(8,8))
claheImage = clahe.apply(erodeImage2)

# 5. Open, close
kernel2 = np.ones((3, 3), np.uint8)
erodeImage3 = cv2.erode(claheImage, kernel2, iterations = 1)
dilateImage2 = cv2.dilate(erodeImage3, kernel2, iterations = 1)

# 6. Adaptive Gaussian thresholding
adaptiveGaussianThresholdImage = cv2.adaptiveThreshold(dilateImage2, 
	255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

# 7. Open, close
erodeImage4 = cv2.erode(adaptiveGaussianThresholdImage, kernel2, iterations = 1)
kernel3 = np.ones((5, 5), np.uint8)
dilateImage3 = cv2.dilate(erodeImage4, kernel3, 
	iterations = 1)

# 8. Canny edge detection
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

cannyImage = auto_canny(erodeImage4)

# 9. Gaussian blur
gaussianBlurImage2 = cv2.GaussianBlur(cannyImage, (3, 3), 0)

# 10. Contour search using perimeter and area
cnts = cv2.findContours(gaussianBlurImage2, 
	cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
(cnts, _) = contours.sort_contours(cnts)
large_contours = []
for cont in cnts:
	if cv2.contourArea(cont) > 20 and cv2.arcLength(cont, True) > 30:
		large_contours.append(cont)

large_contours.sort(key=lambda x: (8 - (cv2.contourArea(x) / 
	cv2.arcLength(x, True))) ** 2, reverse=False)
cv2.drawContours(imageCopy,[large_contours[0]], 0, (0, 255, 127), 2)

cv2.imshow("Image", imageCopy)
cv2.waitKey(0)
cv2.destroyAllWindows()
