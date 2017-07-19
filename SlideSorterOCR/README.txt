index.html is a webix application that displays fox image data in a datatable format. 
It implements ocr via a python virtual environment (run on flask python module via run.py) on images selected
and displays the output on the same web application.

In order to run you will need to create a flask micro enviornment: 
	$ sudo apt-get install python-virtualenv (if you don't have virtualenv and are using python 2 versions)
	$ pip install virtualenv 
	$ virtualenv env

The virtual environment will need to have these packages to run properly:
	flask
	flask_cors
	PIL/Pillow
	pytesseract
	tesseract-ocr (important!)

index.html is set-up to work with bower installed jquery and webix libraries but can be switched to work with cdn.
