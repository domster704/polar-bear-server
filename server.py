import cv2
import jsonpickle
import numpy as np
from flask import Flask, request, Response
from Detector import Detector

app = Flask(__name__)


@app.route('/api/detectBear', methods=['POST'])
def detect():
	nparr = np.frombuffer(request.data, np.uint8)
	img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

	detector = Detector(img)
	detector.doDetect()

	if detector.isBearExisted():
		newImg = detector.getImgAfterDetection()

		_, img_encoded = cv2.imencode('.jpg', newImg)

		response_pickled = jsonpickle.decode(jsonpickle.encode(img_encoded)).tobytes()

		return Response(response=response_pickled, status=200)
	else:
		return Response(status=204)


@app.route("/", methods=['GET'])
def config():
	return "<h1>Polar Bear Detector</h1>"


# app.run(host="0.0.0.0", port=80)
