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
import color_detector_methods

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

images_in_directory(args["directory"])

