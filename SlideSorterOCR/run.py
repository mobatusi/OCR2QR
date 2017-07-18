#!flask/bin/python
from flask import Flask
from flask_cors import CORS, cross_origin
from flask import Response
import json
from flask import request
import urllib
import imghdr
from PIL import Image
from pytesseract import *
import os.path
# from pytesseract import *
#from PIL import Image
# CORS(app)


app = Flask(__name__)
CORS(app)
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/')
@app.route('/index')
def index():
    user = {'imageURL': 'Miguel'} #fake user
    return Response(json.dumps(user))
    #this converts user into a json object

@app.route('/getImage')
def getImage():
	user = {'imageURL': request.args.get('imageURL'), 'imageFlag': False, 'sampleOutput': False}
	# urllib.urlretrieve(user['imageURL'], "sample.png")
	urllib.urlretrieve(request.args.get('imageURL'), "sample.png")
	
	#check if file is a png image
	if imghdr.what('sample.png') == 'png': #if true then run ocr
		# print "hello"
		user['imageFlag'] = os.path.isfile('sample.png')
		# user['imageURL'] = True
		im = Image.open('sample.png')

		text = image_to_string(Image.open('sample.png'))
	# 	user['sampleOutput'] = text
		# cors = CORS(im)
		# CORS(app)
		# CORS(im)
		# text = image_to_string(im) #runs OCR
	# user['imageURL'] = 'test'
	# if imghdr.what('/home/jc/Dropbox/Gutman_Lab/githubProjects/OCR2QR_jc/sample.png') == 'png':
	# 	userURL['imageURL'] = 'true'
	# else: 
	# 	userURL['imageURL'] = 'false'

	return Response(json.dumps(user))

app.run(debug=True)