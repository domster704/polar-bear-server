import cv2
import numpy as np


class Detector:
	IMG_SIZE = 900
	W, H = 7360, 4912
	ASPECT_RATIO = W / H
	NEW_SIDE_SIZE = 1100

	def __init__(self, img):
		self.img = img
		self._valueAverage = 0

		self._bgrImg = None
		self._mask = None
		self._imgWithRec = self.img.copy()

		self._densityListWithCoord = []

		self._isBearExistedOnPhoto = None

	@staticmethod
	def _mapSV(value):
		return int(100 * (value / 255))

	def doDetect(self):
		hsvImg = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
		hue = hsvImg[:, :, 0]
		saturation = hsvImg[:, :, 1]
		value = hsvImg[:, :, 2]

		self._countAverageSaturation(value)
		self._createBGRImg(hue, saturation, value)
		self._createMask()
		self._setRectangleOnImg(self._getMaxDensityIndex())

	def _countAverageSaturation(self, value):
		count = 0
		for i in range(0, value.shape[0], 115):
			for j in range(0, value.shape[1], 307):
				self._valueAverage += value[i][j]
				count += 1

		self._valueAverage = self._mapSV(self._valueAverage / count) / 50

	def _createBGRImg(self, hue, saturation, value):
		h_new = np.mod(hue - 150, 255).astype(np.uint8)
		s_new = np.mod(saturation + 50, 255).astype(np.uint8)
		self._bgrImg = cv2.cvtColor(cv2.merge([h_new, s_new, value]), cv2.COLOR_HSV2BGR)

	def _createMask(self):
		dark = (int(96 * self._valueAverage), int(58 * self._valueAverage), int(93 * self._valueAverage))
		light = (int(125 * self._valueAverage), int(82 * self._valueAverage), int(122 * self._valueAverage))
		mask = cv2.inRange(self._bgrImg, dark, light)

		self._mask = cv2.resize(mask.copy(),
								(int(Detector.NEW_SIDE_SIZE * Detector.ASPECT_RATIO), Detector.NEW_SIDE_SIZE))

	def _setRectangleOnImg(self, maxDensityIndex):
		if not maxDensityIndex:
			self._isBearExistedOnPhoto = False
			return
		print(self._densityListWithCoord[maxDensityIndex][0])
		if 9 < self._densityListWithCoord[maxDensityIndex][0] < 16:
			lineSize = 100
			position = self._densityListWithCoord[maxDensityIndex][1]
			y = int(position[0] * (Detector.H / Detector.NEW_SIDE_SIZE)) - lineSize // 2
			x = int(position[1] * (Detector.W / (Detector.NEW_SIDE_SIZE * Detector.ASPECT_RATIO))) - lineSize // 2

			w = h = lineSize

			cv2.rectangle(self._imgWithRec, (x, y), (x + w, y + h), (0, 0, 255), 10)
			cv2.imwrite('BearConverted.JPG', self._imgWithRec)
			self._isBearExistedOnPhoto = True
		else:
			self._isBearExistedOnPhoto = False

	def _getMaxDensityIndex(self):
		density = self._calculatePixelDensity()
		try:
			return density.index(max(density))
		except:
			return False

	def _calculatePixelDensity(self):
		density = []
		radius = 5
		for i in range(self._mask.shape[0]):
			for j in range(self._mask.shape[1]):
				if self._mask[i][j] != 0:
					if i < radius or i > self._mask.shape[0] - radius:
						pass
					elif j < radius or j > self._mask.shape[1] - radius:
						pass
					else:
						testImg = self._mask[i - radius:i + radius, j - radius:j + radius]
						countUnit = 0
						for k in testImg:
							for l in k:
								if l != 0:
									countUnit += 1
						self._densityListWithCoord.append([countUnit, (i, j)])
						density.append(countUnit)
		# sum1 = 0
		# for i in self._densityListWithCoord:
		# 	sum1 += i[0]
		# print(sum1)
		return density

	def isBearExisted(self):
		return self._isBearExistedOnPhoto

	def getImgAfterDetection(self):
		return self._imgWithRec


if __name__ == "__main__":
	img = cv2.imread("Bear.jpg")
	detector = Detector(img)
	detector.doDetect()
