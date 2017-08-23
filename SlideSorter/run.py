#!ocr2qr_env/bin/python
from flask import Flask, request, Response
from flask_cors import CORS #, cross_origin
import json
import urllib
import imghdr
from PIL import Image
from pytesseract import image_to_string
# from os import path, remove
# import girder_client
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

# def runOCR(pathURL,thresh,cropParams2):
# 	urllib.urlretrieve(pathURL, 'temp.jpg')

# 	if imghdr.what('temp.jpg') != None: 
# 		#Separate RGB arrays
# 		img = Image.open(file('temp.jpg', 'rb'))
# 		img = img.crop(cropParams2)
# 		R, G, B = img.convert('RGB').split()
# 		r = R.load()
# 		g = G.load()
# 		b = B.load()
# 		w, h = img.size
# 		# Convert non-black pixels to white
# 		for i in range(w):
# 			for j in range(h):
# 				if(r[i, j] > thresh or g[i, j] > thresh or b[i, j] > thresh):
# 					r[i, j] = 255 # Just change R channel

#         # Merge just the R channel as all channels
# 		img = Image.merge('RGB', (R, R, R))
# 		img.save('temp.jpg')
# 		img = Image.open('temp.jpg')
# 		remove('temp.jpg') #remove the file
# 		text = image_to_string(img) #perform ocr on the tailored image
# 		# #do regex to remove any unwanted spaces or strange characters
# 		text = re.sub('([^0-9a-zA-Z\:\s\/])+','', text)
# 		text = re.sub('\.',' ', text)
# 		text = re.sub('(\s{1,}|\n)',' ',text)
# 		text =re.sub(r'.(?i)*Fox', 'Fox', text)
# 		if  text[0:3] != 'Fox':
# 			text = re.sub(r'.(?i)*Col', 'Col', text)
# 		return text
# 	else:
# 		return False

@app.route('/runOCR')
def runOCR():
	#*urls with & have problems, seem to cut off the passed parameter url at the first occurance of &
	output = ''
	thresh = 95 #the threshold for the black and white conversion
	# cropParams = [70,0,425,300]
	imagePath = request.args.get('imagePath')
	# urllib.urlretrieve(currentURL, 'temp.jpg')
	if imghdr.what(imagePath) != None:
		img = Image.open(file(imagePath, 'rb'))
		# img = img.crop(cropParams)
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
		return text		
	else: 
		# print 'fail'
		return ''


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


def foxRegex(output):
	noRegexMatch = {'BrainID':None,'Hemi':None,'Column':None,'Section':None,'Stain':None,'StainDate':None}
	sampleRegex = '(?P<BrainID>Fox ?\d ?\d?( )?(?i)(u|t|a))? ?(?P<Hemi>(?i)(LH M|LH F|LH Cau|LHF|Cau))?.* ?(?i)(Cd|Co|Col) ?(?P<Column>(0|1|2|3|4|5|6|7|9)) (?i)(3|8|s) ?(?P<Section>\d{1,3}b?).*(?P<Stain>(?i)(ss|Slver|Silver|lesl|AVP)).* (?P<StainDate>(\d\d?\/\d\d?\/1(6|7)|\d\d?\/\/?1(6|7)))'
	re_ADRC_SlideSet = re.compile(sampleRegex)
	m = re_ADRC_SlideSet.search(output)

	if m:
		noRegexMatch = m.groupdict()
		noRegexMatch = cleanFoxMetaDataOutput(noRegexMatch) 

	return Response(json.dumps(noRegexMatch))	

@app.route('/runRegex')
def runRegex():
	schemaKey = request.args.get('schema')

	if schemaKey == 'fox':
		return foxRegex(request.args.get('ocr_output'))
	else:
		return None

@app.route('/getGroups')
def getGroups():
	print request.args.get('schema')
	if request.args.get('schema') == 'fox':
		temp = {'1':'BrainID', '2':'Hemi', '3':'Column', '4':'Section','5':'Stain','6':'StainDate'}		
		return Response(json.dumps(temp))
	elif request.args.get('schema') == 'fox2':
		temp = {'1':'Column','2':'Hemi'}
		return Response(json.dumps(temp))
	else:
		return 'no match'

app.run(debug=True)
