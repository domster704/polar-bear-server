import jsonpickle
import requests
import numpy as np
import cv2

addr = 'http://localhost:5000/api/test'

content_type = 'image/jpeg'
headers = {'content-type': content_type}

img = cv2.imread('xd.jpg')
_, img_encoded = cv2.imencode('.jpg', img)
response = requests.post(addr, data=img_encoded.tobytes(), headers=headers)

print(response.content)
# frame = jsonpickle.decode(response.text)
# frame = frame.tobytes()
# print(frame)
nparr = np.frombuffer(response.content, np.uint8)
img = cv2.imdecode(response.text, cv2.IMREAD_COLOR)

cv2.imwrite('xd2.jpg', img)

