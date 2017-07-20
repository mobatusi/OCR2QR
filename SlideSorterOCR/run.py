#!env/bin/python
from flask import Flask, request
from flask_cors import CORS #, cross_origin
from flask import Response
import json
import urllib
import imghdr
from PIL import Image
from pytesseract import image_to_string
from os import path, remove
import girder_client

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "OCR is ready to run!"

@app.route('/getImage')
def getImage():
	#*urls with & have problems, seem to cut off the passed parameter url at the first occurance of &
	user = {'sampleOutput': ''}
	tempFile = 'tempImage.jpg'
	urllib.urlretrieve(request.args.get('imageURL'), tempFile)
	
	if imghdr.what(tempFile) == 'jpeg': #if true then run ocr
		tempImage = Image.open(path.abspath(tempFile))
		text = image_to_string(tempImage)
		user['sampleOutput'] = text
		remove(tempFile) #delete the temporary file 

	return Response(json.dumps(user))

@app.route('/getMetadata')
def getMetadata():
	user2 = {'metadata':'no metadata present'}
	#select appropriate API url. For fox image data it is candygram version 1
	API_URL = "http://candygram.neurology.emory.edu:8080/api/v1"
	#sign-in to the client using user & password
	gc = girder_client.GirderClient(apiUrl=API_URL)
	gc.authenticate(username="admin", password="password")
	temp = request.args.get('imageID')
	temp = "item/" + temp
	user2['metadata'] = temp
	item = gc.get(user2['metadata'])
	if item.has_key('meta'):
		item = item["meta"]
	else:
		item = {'bad_ocr_output':None}
	user2['metadata'] = item
	return Response(json.dumps(user2['metadata']))

@app.route('/updateMetadata')
def updateMetadata():
	#select appropriate API url. For fox image data it is candygram version 1
	API_URL = "http://candygram.neurology.emory.edu:8080/api/v1"
	#sign-in to the client using user & password
	gc = girder_client.GirderClient(apiUrl=API_URL)
	gc.authenticate(username="admin", password="password")
	temp = request.args.get('imageID')
	temp = "item/" + temp + "/metadata"
	print temp
	item = gc.put(temp, json={"bad_ocr_output":request.args.get('ocr_output')})
	return "Metadata was saved!"


app.run(debug=True)