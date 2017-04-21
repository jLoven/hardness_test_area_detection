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
def auto_canny(image, sigma = 0.93):
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
args = vars(ap.parse_args())
image = cv2.imread("images/" + args["image"])
imageCopy = image.copy()

RED_MIN = np.array([57 - 5, 217 - 5, 50 - 5], np.uint8)
RED_MAX = np.array([57 + 5, 217 + 5, 50 + 5], np.uint8)

dst = cv2.inRange(imageCopy, RED_MIN, RED_MAX)
no_red = cv2.countNonZero(dst)
print('The number of red pixels is: ' + str(no_red))
display(dst)