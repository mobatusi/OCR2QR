index.html is a webix application that displays fox image data in a datatable format. 
It implements ocr via a python virtual environment (run on flask python module via run.py) on images selected
and displays the output on the same web application.

Secondary funtion is that it allows interaction with the candygram API to update or add metadata to the slides.
The metadata fields are preset already and can be checked and updated freely. Metadata can be updated via
the text boxes present by clicking the associated button or pressing the enter key. Alternatively, the metadata
can be updated directly from individual cells in the datatable by double clicking, typing the change, then 
pressing enter. 

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
	imghdr
	girder_client

index.html is set-up to work with bower installed jquery and webix libraries but can be switched to work with cdn.

To run the widget appropriately:
	Initiate local host environment: python -m SimpleHTTPServer
		recommended to initiate it in the directory with index.html file
	Activate virtual environment: source env/bin/activate
	Run the flask environment in the activated virtual environment: python run.py
		make sure this runs on localhost 5000
	Run index.html on local host server (usually 8000): localhost:8000/index.html

Caveats: note that run.py is set to run with a virtual environment called env2 in the same folder as the files. 
		 This can be easily changed on the first line of run.py


