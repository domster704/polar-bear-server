import cv2
import jsonpickle
import numpy as np
from flask import Flask, request, Response, jsonify
from Detector import Detector

app = Flask(__name__)
detector = None


@app.route('/api/detectBear', methods=['POST'])
def detect():
	global detector
	nparr = np.frombuffer(request.data, np.uint8)
	img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

	detector = Detector(img)
	detector.doDetect()

	newImg = detector.getImgAfterDetection()

	_, img_encoded = cv2.imencode('.jpg', newImg)

	response_pickled = jsonpickle.decode(jsonpickle.encode(img_encoded)).tobytes()

	return Response(response=response_pickled, status=200, mimetype=None)


@app.route('/api/getStatus', methods=['GET'])
def getStatus():
	if detector is not None and isinstance(detector, Detector):
		return jsonify(detector.isBearExisted())
	else:
		return jsonify("Вы ещё не просканировали фото")


@app.route("/", methods=['GET'])
def config():
	return "<h1>Polar Bear Detector</h1>"


app.run(host="0.0.0.0", port=80)
