from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview()
sleep(15)
camera.capture('/home/pi/Documents/Projects/OCR2QR/image.jpg')
camera.stop_preview()
