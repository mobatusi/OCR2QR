from flask import Flask,render_template, Response
import cv2
#import webcam.py

class Camera(object):
  def __init__(self):
    self.cap = cv2.VideoCapture(0)

  def get_frame(self):
    ret, frame = self.cap.read()
    cv2.imwrite('stream.jpg',frame)
    return open('stream.jpg', 'rb').read()

app = Flask(__name__)

#@app.route("/")
#def index():
#	return "Flask App!"

#@app.route("/hello/<string.name>")
@app.route("/") 
def index():
#	return render_template('layout.html')
	return render_template('index.html')

def gen(camera):
  while True:
    frame = camera.get_frame()
    yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + frame
           + b'\r\n')

@app.route ('/video_feed')
def video_feed():
  return Response(gen(Camera()),
    mimetype='multipart/x-mixed-replace;boundary=frame')

@app.route('/my-link')
def my_link():
	print 'I got clicked!'
	
	return 'Click.' 

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
