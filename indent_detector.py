# Jackie Loven
# 14 March 2017
# Thanks Odell for the advice!

import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, 
	help="path to the input image")
args = vars(ap.parse_args())
image = cv2.imread(args["image"])

# 1. Convert to grayscale
grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 2. Simple Gaussian blur
# window size 7 x 7, exact
gaussianBlurImage = cv2.GaussianBlur(grayImage, (7, 7), 0)

# 3. Open, close, open image








cv2.waitKey(0)
cv2.destroyAllWindows()