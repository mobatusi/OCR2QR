#!/usr/bin/python

import os
import pytesseract
import ctypes
import gc
import pprint

from PIL import Image
from pytesseract import image_to_string

#print "HAVE_LIBLEPT=",tesseract.isLibLept()
#print dir("tesseract")
#print tesseract.MAX_NUM_INT_FEATURES

os.system("fswebcam -S 20 --no-banner -r 640x480 image.tif")
mImgFile = "image.tif"

im = Image.open(mImgFile)
text = image_to_string(im)

print text
im.show()




