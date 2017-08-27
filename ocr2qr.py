#!/usr/bin/python

import os
import pytesseract
import ctypes
import gc
import pprint
import qrcode
import scipy

from PIL import Image
from pytesseract import *
from picamera import PiCamera
from time import sleep
from skimage import filters
#from qrcode import *

# take a picture via the webcam. Eventually we will switch to using the pi camera

#os.system("fswebcam -S 20 --no-banner -r 640x480 image.tif")
#mImgFile = "image.tif"

camera = PiCamera()
camera.resolution = (2592, 1944)#Mac resolution allowed
#camera.resolution = (64, 64)# Min resolution allowed
#You can alter the brightness setting, which can be set from 0 to 100. The default is 50.


camera.framerate = 15
camera.start_preview()
for i in range(100):
    camera.annotate_text = "Brightness: %s" % i
    camera.brightness = i
    sleep(0.1)
    #sleep(5)

for i in range(100):
    camera.annotate_text = "Contrast: %s" % i
    camera.contrast = i
    sleep(0.1)
camera.capture('/home/pi/Documents/Projects/OCR2QR/image.jpg')
camera.stop_preview()
mImgFile = "image.jpg"

# Opening and reading the image
# converting the image to grayscale
im = Image.open(mImgFile).convert('L')

# im is converted to an ndarray
im_array = scipy.misc.fromimage(im)

# Perform Otsu's thresholding
thresh = filters.threshold_otsu(im_array)

# pixels with intensity greater than 
# threshold are kept
im_thresh = im_array > thresh

# im_thresh is converted from ndarray to image 
im_thresh = scipy.misc.toimage(im_thresh)

text = image_to_string(im_thresh)

print (text)
output = open("output", "w")
output.write(text)
output.close()
#im.show()

#qr = QRCode(version=20, error_correction=ERROR_CORRECT_L)
img = qrcode.make(text)
#qr.make() #Generate the QRCode itself

#im = qr.make_image()

#TO Save it
img.save("QRCode.png")
img.show()


