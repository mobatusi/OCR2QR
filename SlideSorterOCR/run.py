#!env2/bin/python
from flask import Flask, request, Response
from flask_cors import CORS #, cross_origin
import json
import urllib
import imghdr
from PIL import Image
from pytesseract import image_to_string
# from os import path, remove
import girder_client
#Dolu updated OCR script, import new packages
# import ctypes
# import gc
# import scipy
# from skimage import filters
import re
# import json
# import time
# import pprint

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "The widget is ready to run!"

@app.route('/getImage')
def getImage():
	#*urls with & have problems, seem to cut off the passed parameter url at the first occurance of &
	user = {'sampleOutput': ''}
	thresh = 95 #the threshold for the black and white conversion
	cropParams = [70,0,425,300]
	currentURL = request.args.get('imageURL')[:len(request.args.get('imageURL'))-3]+'500'
	urllib.urlretrieve(currentURL, 'temp.jpg')
	if imghdr.what('temp.jpg') != None:
		img = Image.open(file('temp.jpg', 'rb'))
		img = img.crop(cropParams)
		R, G, B = img.convert('RGB').split()
		r = R.load()
		g = G.load()
		b = B.load()
		w, h = img.size
      	# Convert non-black pixels to white
	      	for i in range(w):
    	  		for j in range(h):
      				if (r[i, j] > thresh or g[i, j] > thresh or b[i, j] > thresh):
      					r[i, j] = 255 # Just change R channel

      				
		img = Image.merge('RGB', (R, R, R))
		img.save('temp.jpg')
		img = Image.open('temp.jpg')
      	 	# remove('temp.jpg') #remove the file
		text = image_to_string(img) #perform ocr on the tailored image
#		print text
      	 	#do regex to remove any unwanted spaces or strange characters

		text = re.sub('([^0-9a-zA-Z\:\s\/])+','', text)
		text = re.sub('\.',' ', text)
		text = re.sub('(\s{1,}|\n)',' ',text)
		text =re.sub(r'.(?i)*Fox', 'Fox', text)
		if  text[0:3] != 'Fox':
			text = re.sub(r'.(?i)*Col', 'Col', text)
        		# print 'This is the output after regex',text
		user['sampleOutput'] = text		
	else: 
		print 'fail'
		user['sampleOutput'] = None
	return Response(json.dumps(user))

@app.route('/getMetadata')
def getMetadata():
	user2 = {'metadata':'no metadata present'}
	#select appropriate API url. For fox image data it is candygram version 1
	API_URL = "http://candygram.neurology.emory.edu:8080/api/v1"
	#sign-in to the client using user & password
	gc = girder_client.GirderClient(apiUrl=API_URL)
	gc.authenticate(username="", password="")
	temp = request.args.get('imageID')
	# print 'The current image id is ',temp
	temp = "item/" + temp
	user2['metadata'] = temp
	item = gc.get(user2['metadata']) #this is giving an input like: item/'fjakdfj88989df'
	if item.has_key('meta'):
		item = item["meta"]
	else:
		item = {'ocr_output':None}
	user2['metadata'] = item
	return Response(json.dumps(user2['metadata']))

@app.route('/updateMetadata')
def updateMetadata():
	#select appropriate API url. For fox image data it is candygram version 1
	API_URL = "http://candygram.neurology.emory.edu:8080/api/v1"
	#sign-in to the client using user & password
	gc = girder_client.GirderClient(apiUrl=API_URL)
	gc.authenticate(username="", password="")
	temp = request.args.get('imageID')
	# temp = "item/" + temp + "/metadata"
	# print temp
	# item = gc.put(temp, json={"ocr_output":request.args.get('ocr_output')})
	gc.addMetadataToItem(temp,{'ocr_output':request.args.get('ocr_output')})

	return "Metadata was saved!"

@app.route('/updateMetadataGroup')
def updateMetadataGroup():
	imageID = request.args.get('imageID')
	textID = request.args.get('textID').split(',')
	# print len(textID)
	textValue = request.args.get('textValue').split(',')
	# print len(textValue)
	# print textValue
	# i = 0
	# for sld in textID:
	#select appropriate API url. For fox image data it is candygram version 1
	API_URL = "http://candygram.neurology.emory.edu:8080/api/v1"
	# #sign-in to the client using user & password
	gc = girder_client.GirderClient(apiUrl=API_URL)
	gc.authenticate(username="", password="")
	groups = gc.getItem(imageID)['meta']
	if groups.has_key('groups'):
		groups = groups['groups']
		i = 0
		for sld in textID:
			groups[sld] = textValue[i]
			gc.addMetadataToItem(imageID,{'groups':groups})
			i += 1
		# time.sleep(5)
		return "Metadata was saved!"
	else:
		return "This slide has no groups meta data currently"

def cleanFoxMetaDataOutput(dirtyOutput):
	if dirtyOutput['BrainID'] != None:
		dirtyOutput['BrainID'] = re.sub('\s','',dirtyOutput['BrainID']).upper() #remove any spaces from brain ID
		dirtyOutput['BrainID'] = re.sub('FOX','Fox',dirtyOutput['BrainID'])    
	if dirtyOutput['Hemi'] != None:
		dirtyOutput['Hemi'] = re.sub('(?i)LH','LH',dirtyOutput['Hemi'])
		dirtyOutput['Hemi'] = re.sub('(?i)Cau','Caudal',dirtyOutput['Hemi'])
		dirtyOutput['Hemi'] = re.sub('(?i)LH M','LH Mid',dirtyOutput['Hemi'])
		dirtyOutput['Hemi'] = re.sub('(?i)(LH F|LHF)','LH Frontal',dirtyOutput['Hemi'])
	dirtyOutput['Stain'] = re.sub('(?i)(AVP)','AVP 1:20k',dirtyOutput['Stain'])
	dirtyOutput['Stain'] = re.sub('(?i)(ss|lesl)','Nissl',dirtyOutput['Stain'])
	dirtyOutput['Stain'] = re.sub('(?i)(Slver|Silver)','Silver',dirtyOutput['Stain'])
	dirtyOutput['StainDate'] = re.sub('\/{1,}','/',dirtyOutput['StainDate'])
	dirtyOutput['StainDate'] = re.sub('\s','',dirtyOutput['StainDate'])
	return dirtyOutput


@app.route('/runRegex')
def runRegex():
	noRegexMatch = {'groups':{'BrainID':None,'Hemi':None,'Column':None,'Section':None,'Stain':None,'StainDate':None}}
	sampleRegex = '(?P<BrainID>Fox ?\d ?\d?( )?(?i)(u|t|a))? ?(?P<Hemi>(?i)(LH M|LH F|LH Cau|LHF|Cau))?.* ?(?i)(Cd|Co|Col) ?(?P<Column>(0|1|2|3|4|5|6|7|9)) (?i)(3|8|s) ?(?P<Section>\d{1,3}b?).*(?P<Stain>(?i)(ss|Slver|Silver|lesl|AVP)).* (?P<StainDate>(\d\d?\/\d\d?\/1(6|7)|\d\d?\/\/?1(6|7)))'
	re_ADRC_SlideSet = re.compile(sampleRegex)
	m = re_ADRC_SlideSet.search(request.args.get('ocr_output'))

	if m:
		noRegexMatch['groups'] = m.groupdict()
		noRegexMatch['groups'] = cleanFoxMetaDataOutput(noRegexMatch['groups']) 

	return Response(json.dumps(noRegexMatch))


app.run(debug=True)
