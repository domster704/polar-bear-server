from flask import Flask, request, Response
import jsonpickle
import numpy as np
import cv2

app = Flask(__name__)


@app.route('/api/test', methods=['POST'])
def test():
	r = request
	# print(r.data)
	print(type(r.data))
	nparr = np.frombuffer(r.data, np.uint8)
	img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

	img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

	_, img_encoded = cv2.imencode('.jpg', img)
	# response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0])
	# 			}
	# response_pickled = jsonpickle.encode(response)

	response_pickled = jsonpickle.encode(img_encoded)
	# print(jsonpickle.decode(response_pickled).tobytes())
	response_pickled = jsonpickle.decode(response_pickled).tobytes()

	return Response(response=response_pickled, status=200, mimetype=None)


@app.route("/api/config", methods=['GET'])
def config():
	return "<h1>TEST</h1>"


app.run(host="0.0.0.0", port=5000)
