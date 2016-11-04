#!/usr/bin/python

import os
import pytesseract
import ctypes
import gc
import pprint
import qrcode
import numpy as np
import argparse
import cv2
import imutils

#import pyocr
#import pyocr.builders
#import io

# import the necessary packages
from pyimagesearch.transform import four_point_transform
from pyimagesearch.transform import order_points
from skimage.filters import threshold_adaptive
from PIL import Image
from pytesseract import *
from picamera import PiCamera
from time import sleep

#from wand.imageimport Image

# construct the argument parser and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required = True,
#	help = "Path to the image to be scanned")
#args = vars(ap.parse_args())

# take a picture via the webcam. Eventually we will switch to using the pi camera
#os.system("fswebcam -S 20 --no-banner -r 640x480 image.tif")
#mImgFile = "image.tif"
camera = PiCamera()

camera.start_preview()
sleep(5)
mImgFile = camera.capture('/home/pi/Documents/Projects/OCR2QR/image.jpg')
camera.stop_preview()
#mImgFile = "image.jpg"

# load the image and compute the ratio of the old height
# to the new height, clone it, and resize it
#image = cv2.imread(args["image"])
image = cv2.imread(mImgFile)
ratio = image.shape[0] / 500.0
orig = image.copy()
image = imutils.resize(image, height = 500)

# convert the image to grayscale, blur it, and find edges
# in the image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(gray, 75, 200)

# show the original image and the edge detected image
print ("STEP 1: Edge Detection")
#cv2.imshow("Image", image)
#cv2.imshow("Edged", edged)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
cv2.imwrite("image_edged.jpg",edged)
cv2.destroyAllWindows()

# find the contours in the edged image, keeping only the
# largest ones, and initialize the screen contour
# check to see if we are using OpenCV 2.x
if imutils.is_cv2():
    (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]

# check to see if we are using OpenCV 3
elif imutils.is_cv3():
    (_,cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]

# loop over the contours
for c in cnts:
	# approximate the contour
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.04 * peri, True)

	# if our approximated contour has four points, then we
	# can assume that we have found our screen
	if len(approx) == 4:
		screenCnt = approx
		break
	    
# show the contour (outline) of the piece of paper
print ("STEP 2: Find contours of paper")
#cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
#cv2.imwrite("image_contours.jpg",image)
#cv2.imshow("Outline", image)
#cv2.waitKey(0)
#cv2.destroyAllWindows()



# apply the four point transform to obtain a top-down
# view of the original image
# warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)

#pts = np.array(eval("[(73, 239),(356, 117),(478,265),(185,443)]"),dtype = "float32")
pts = np.array(eval("[(101, 185), (393, 151), (479, 323), (187, 441)]"),dtype = "float32")
warped = four_point_transform(orig, pts)

# convert the warped image to grayscale, then threshold it
# to give it that 'black and white' paper effect
warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
warped = threshold_adaptive(warped, 251, offset = 10)
warped = warped.astype("uint8") * 255

# show the original and scanned images
print ("STEP 3: Apply perspective transform")
#cv2.imshow("Original", imutils.resize(orig, height = 650))
#cv2.imshow("Scanned", imutils.resize(warped, height = 650))
#cv2.waitKey(0)
cv2.imwrite("image_scanned.tif",warped)

# convert Image to text
#im = Image.open("image_scanned.tif")
im = Image.open("image.tif")
text = image_to_string(im)

print (text)
output = open("output", "w")
output.write(text)
output.close()


#Generate the QRCode itself#
img = qrcode.make(text)

# To Save it
img.save("QRCode.png")
img.show()
