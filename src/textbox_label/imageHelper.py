import cv2
import numpy as np

def segmentImage(img):
	"""Binarize image"""
	# binarize image
	# convert to grayscale
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	# blur image
	blur = cv2.blur(gray, (3, 3))
	# threshold image
	_, thresh = cv2.threshold(blur, 150, 255, cv2.THRESH_BINARY)
	return blur
	return thresh
