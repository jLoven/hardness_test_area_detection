# Author: Odell Dotson
# www.github.com/odelldotson
# Code is provided as-is, with no promises.

import cv2
import copy


def display(img, name="img"):
    """Displays a window with an image.
    Press space while focussed on the window to move on."""
    cv2.imshow(name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def getFileByName(fileName,path="images/"):
    """ Read in an image by it's path. Default path is configurable."""
    read_file =  cv2.imread(path + fileName, cv2.IMREAD_UNCHANGED)
    if read_file is None:
        raise ValueError('Error in attempt to read file. Are you sure the file is there?')
    return read_file


def open_image(img, kernel_radius = 5, itera = 1):
    """Assumes image has black image on white background
    If that's not the case, opening => closing and closing => opening"""
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_radius,kernel_radius))
    return cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations=itera)


def close_image(img, kernel_radius = 5, itera = 1):
    """Assumes image has black image on white background
    If that's not the case, opening => closing and closing => opening"""
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_radius,kernel_radius))
    return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=itera)


# Toggle if you want to see the steps or not.
debug = True

img = getFileByName("1.jpg", "src/")
if debug: display(img)

image_copy = copy.deepcopy(img)

gray_image = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# Blur the grayscale iamge
gray_image = cv2.GaussianBlur(gray_image, (3,3), 0)
if debug: display(gray_image, "gray image blurred")

# http://docs.opencv.org/2.4/doc/tutorials/imgproc/opening_closing_hats/opening_closing_hats.html
# I use image opening and closing to provide noise reduction for feature extraction.
gray_image_closed = close_image(gray_image, kernel_radius = 7)
if debug: display(gray_image_closed, "gray image, openned")

gray_image_closed = open_image(gray_image, kernel_radius = 7)
if debug: display(gray_image_closed, "gray image, closed")

gray_image_closed = close_image(gray_image, kernel_radius = 7)
if debug: display(gray_image_closed, "gray image, openned")

# http://docs.opencv.org/3.1.0/d5/daf/tutorial_py_histogram_equalization.html
clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8,8))
gray_image_closed = clahe.apply(gray_image_closed)
display(gray_image_closed)


gray_image_closed = close_image(gray_image, kernel_radius = 3)
if debug: display(gray_image_closed, "gray image, openned")

gray_image_closed = open_image(gray_image, kernel_radius = 3)
if debug: display(gray_image_closed, "gray image, closed")


# Apply an adaptive gaussian treshold to the image
adaptive_thresholded = cv2.adaptiveThreshold(gray_image_closed,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
if debug: display(adaptive_thresholded, "adaptive thresholded")

# Now close the image, removing small areas of noise.
adaptive_thresholded_openned_c = open_image(adaptive_thresholded, kernel_radius = 3)
if debug: display(adaptive_thresholded_openned_c, "addy treshed closed!!")


# Now close the image, removing small areas of noise.
adaptive_thresholded_openned = close_image(adaptive_thresholded_openned_c, kernel_radius = 5)
if debug: display(adaptive_thresholded_openned, "addy treshed opened")

# Apply canny edge detection to isolate edges.
adaptive_thresholded_canny = cv2.Canny(adaptive_thresholded_openned, 50,150, apertureSize = 3)
if debug: display(adaptive_thresholded_canny, "addy threshed, canny")

# Blur the found thresholds.
adaptive_thresholded_canny_blur = cv2.GaussianBlur(adaptive_thresholded_canny, (3,3), 0)
if debug: display(adaptive_thresholded_canny_blur, "ady thresh canny blur")

# Now we find the contours we will be applying.
image, contours, other = cv2.findContours(adaptive_thresholded_canny_blur,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE) # Gather the contours
long_contours = [] # Create an array for the long edges to be held

# http://docs.opencv.org/trunk/dd/d49/tutorial_py_contour_features.html
for cnt in contours:
    # These constants are pretty meh.
    # They are upper and lower bounds for areas contained by and perimiter area of, contours.
    if 1000<cv2.contourArea(cnt) < 4000 and 200 < cv2.arcLength(cnt, True) < 500:
        long_contours.append(cnt) # Record any long contours
        if debug: print "area: ", cv2.contourArea(cnt)
        if debug: print "contour perimiter: ", cv2.arcLength(cnt, True)
        if debug: print "circ stat: ", cv2.minEnclosingCircle(cnt)

if debug: print "Long contours found: ", len(long_contours)

# the 8 below was experimentally determined.
# What we're doing here is looking for the ratio of area and perimiter to be 8.
# We're using squared error of the ratio between area and perimiter's difference from 8.
long_contours.sort(key=lambda x: (8 - (cv2.contourArea(x) / cv2.arcLength(x, True))) ** 2, reverse=False)

if debug: print "contours: "
if debug:
    for cnt in long_contours:
        print cv2.contourArea(cnt)

# Highlight the prism and display it.
cv2.drawContours(image_copy,[long_contours[0]],0,(0,255,127),2)
display(image_copy)
