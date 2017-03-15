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

# 1. Convert to grayscale
grayImage = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2GRAY)

# 2. Simple Gaussian blur
# window size 7 x 7, exact
gaussianBlurImage1 = cv2.GaussianBlur(grayImage, (7, 7), 0)

# 3. Open (erode), close (dilate), open image
# https://goo.gl/nm8BXX for opening and closing docs
# https://goo.gl/RUhy32 for why you need to do uint8
kernel = np.ones((5, 5), np.uint8)
erodeImage1 = cv2.erode(gaussianBlurImage1, kernel, iterations = 1)
dilateImage1 = cv2.dilate(erodeImage1, kernel, iterations = 1)
erodeImage2 = cv2.erode(dilateImage1, kernel, iterations = 1)

# 4. CLAHE (Contrast Limited Adaptive Histogram Equalization)
# https://goo.gl/OjnwZC for a good explanation, it improves contrast
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
claheImage = clahe.apply(erodeImage2)

# 5. Open, close
erodeImage3 = cv2.erode(claheImage, kernel, iterations = 1)
dilateImage2 = cv2.dilate(erodeImage3, kernel, iterations = 1)

# 6. Adaptive Gaussian thresholding
adaptiveGaussianThresholdImage = cv2.adaptiveThreshold(dilateImage2, 
	255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

# 7. Close, open
dilateImage3 = cv2.dilate(adaptiveGaussianThresholdImage, kernel, 
	iterations = 1)
erodeImage4 = cv2.erode(dilateImage3, kernel, iterations = 1)

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
gaussianBlurImage2 = cv2.GaussianBlur(cannyImage, (7, 7), 0)

# 10. Contour search using perimeter and area
contours = cv2.findContours(gaussianBlurImage2, 
	cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
(cnts, _) = contours.sort_contours(cnts)
for c in cnts:
	if cv2.contourArea(c) < 50:
		continue
	cv2.drawContours(image, [c], -1, (255, 192, 203), 3)

cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()