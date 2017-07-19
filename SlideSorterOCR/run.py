#!env/bin/python
from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask import Response
import json
# from flask import request
import urllib
import imghdr
from PIL import Image
import pytesseract
import os.path
import os

# from pytesseract import *
#from PIL import Image
# CORS(app)


app = Flask(__name__)
CORS(app)
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/')
def index():
    user = {'imageURL': 'Miguel'} #fake user
    return Response(json.dumps(user))
    #this converts user into a json object

@app.route('/getImage')
def getImage():
	#url used for debugging: http://i.cdn.cnn.com/cnn/.element/img/4.0/subscription/Fareed_SubscriptionHub.jpg
	#*urls with & have problems, seem to cut off the passed parameter url at the first occurance of &
	user = {'imageURL': request.args.get('imageURL'), 'imageFlag': False, 'sampleOutput': None}
	tempFile = 'tempImage.jpg'
	urllib.urlretrieve(user['imageURL'], tempFile)
	
	if imghdr.what(tempFile) == 'jpeg': #if true then run ocr
		user['imageFlag'] = True
		tempImage = Image.open(os.path.abspath(tempFile))
		text = pytesseract.image_to_string(tempImage)
		# text = os.path.abspath(im)
		# text = pytesseract.image_to_string(im)
		user['sampleOutput'] = text
		os.remove(tempFile) #delete the temporary file 
# 		# cors = CORS(im)
# 		# CORS(app)
# 		# CORS(im)
# 		# text = image_to_string(im) #runs OCR
# 	# user['imageURL'] = 'test'
# 	# if imghdr.what('/home/jc/Dropbox/Gutman_Lab/githubProjects/OCR2QR_jc/sample.png') == 'png':
# 	# 	userURL['imageURL'] = 'true'
# 	# else: 
# 	# 	userURL['imageURL'] = 'false'

	return Response(json.dumps(user))

app.run(debug=True)