# Jackie Loven
# 14 March 2017
# Thanks Odell for the advice!

import argparse
import cv2
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, 
	help="path to the input image")
args = vars(ap.parse_args())
image = cv2.imread(args["image"])

# 1. Convert to grayscale
grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

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
# https://goo.gl/OjnwZC for a good explanation








cv2.waitKey(0)
cv2.destroyAllWindows()