import sys
from typing import List
import cv2
from cv2 import LINE_AA
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


def getContours(img):
    """get contours in an image"""
    # find edges
    edges = cv2.Canny(img, 50, 150)

    # find external contours
    contours, hierarchy = cv2.findContours(
        edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    return contours


def approximateContours(contours: List):
    """Smoothen contours"""
    res = []
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        epsilon = 0.02 * perimeter
        approximatedShape = cv2.approxPolyDP(contour, epsilon, True)
        res.append(approximatedShape)

    return res


def getHulls(contours: List):
    """get convex hull for each contour"""
    return [cv2.convexHull(c, False) for c in contours]


def filterTextBoxes(hulls: List):
    """Partition convex hulls into text labels and text boxes"""
    MIN_AREA = 1000
    textBoxes = []
    other = []
    for hull in hulls:
        if cv2.contourArea(hull) > MIN_AREA:
            textBoxes.append(hull)
        else:
            other.append(hull)

    return (textBoxes, other)


def boundingBox(contours: List):
    """Get bounding box for each contour"""
    return [cv2.boundingRect(c) for c in contours]


if __name__ == "__main__":
    # provide image file as cli argument
    imgFile = sys.argv[1]
    # read image
    img = cv2.imread(imgFile)

    # segment image
    segmentedImg = segmentImage(img)

    # find contours in image
    contours = getContours(segmentedImg)
    # approximage the contours to smoothen lines
    approxContours = approximateContours(contours)

    # find convex hull of approximated contours
    hulls = getHulls(approxContours)

    # find hulls containing text boxes and text labels
    textBoxes, textLabels = filterTextBoxes(hulls)

    # find bounding box of text boxes
    textBoxBounds = boundingBox(textBoxes)

    # write images
    cv2.imwrite("results/convexHull_step0.png", img)
    cv2.imwrite("results/convexHull_step1.png", segmentedImg)

    # write image containing contours
    contoursImg = img.copy()
    cv2.drawContours(contoursImg, contours, -1, (0, 255, 0),
                     thickness=2, lineType=cv2.LINE_AA)
    cv2.imwrite("results/convexHull_step2.png", contoursImg)

    # write image containing convex hulls
    convexHullImg = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    cv2.drawContours(convexHullImg, hulls, -1, (255, 255, 255),
                     thickness=1, lineType=cv2.LINE_AA)
    cv2.imwrite("results/convexHull_final.png", convexHullImg)

    # write image containing text boxes
    textBoxesImg = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    cv2.drawContours(textBoxesImg, textBoxes, -1, (0, 255, 0),
                     thickness=1, lineType=cv2.LINE_AA)
    cv2.imwrite("results/convexHull_textBoxes.png", textBoxesImg)

    # write image containing text labels
    textLabelsImg = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    cv2.drawContours(textLabelsImg, textLabels, -1,
                     (255, 0, 0), thickness=1, lineType=cv2.LINE_AA)
    cv2.imwrite("results/convexHull_textLabels.png", textLabelsImg)

    # write image containing text labels and text boxes
    textLabelsBoxesImg = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    cv2.drawContours(textLabelsBoxesImg, textLabels, -1,
                     (255, 0, 0), thickness=1, lineType=cv2.LINE_AA)
    cv2.drawContours(textLabelsBoxesImg, textBoxes, -1,
                     (0, 255, 0), thickness=1, lineType=cv2.LINE_AA)
    cv2.imwrite("results/convexHull_textLabelsBoxes.png", textLabelsImg)

    # write image containing bounding box for text boxes
    textBoxBoundingImg = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    for box in textBoxBounds:
        x, y, w, h = box
        cv2.rectangle(textBoxBoundingImg, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.imwrite("results/convexHull_textBoxBoundingBox.png",
                textBoxBoundingImg)

    print(textBoxBounds)
   #  cv2.imwrite("results/convexHull_boundingTextBoxes", textBoxBoundingImg)
