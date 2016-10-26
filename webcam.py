#!/usr/bin/python

import os
import pytesseract
import ctypes
import gc
import pprint
import qrcode

from PIL import Image
from pytesseract import *

#from qrcode import *

os.system("fswebcam -S 20 --no-banner -r 640x480 image.tif")
mImgFile = "image.tif"

im = Image.open(mImgFile)
text = image_to_string(im)

print text
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


