from flask import Flask, send_from_directory, request, jsonify,send_file
import ssl
import qr_generation as qrg
import StringIO

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain('localhost.key.crt', 'localhost.key')

app = Flask(__name__)

app.debug = True


@app.route('/')
def serve_main():
    return app.send_static_file('index.html')

@app.route('/js/<path:path>')
def send_js(path):
	return send_from_directory('js',path)

@app.route('/css/<path:path>')
def send_css(path):
	return send_from_directory('css',path)


@app.route('/api/grab_snapshot', methods=['POST'])
def process_snapshot():
	print "HI DAVE"
	return "HI"

@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)


def serve_pil_image(pil_img):
    img_io = StringIO.StringIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')


@app.route('/api/image_utils/checkerboard')
def serve_img():
    img = qrg.make_checkerboard()
    return serve_pil_image(img)

@app.route('/api/image_utils/_get_checkers', methods=['POST','GET'])
def serve_checkerboard_img():
    img = qrg.make_checkerboard('green','blue')
    return serve_pil_image(img)



if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.1',ssl_context=context)
