import sys
from typing import List
import cv2
from cv2 import LINE_AA
import numpy as np
import json

path = 'results/ROI{0}.png'
filename = 'ROI.json'

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
    MIN_AREA = 3000
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

# given an image and a list of rectangles
# crop the image using each rectangle
# returns a json object with the rectangles and path to each cropped image
def getROI(img, rectangles: List):
    obj = {}
    image = img.copy()
    height, width, channels = image.shape
    
    # iterate through contours
    for i, c in enumerate(rectangles):
        x = c[0] if c[0] > 0 else 0
        y = c[1] if c[1] > 0 else 0
        w = c[2] if c[2] + x < width else width - x
        h = c[3] if c[3] + y < height else height - y

        # for each contour found, crop the image and save a copy based on bounding box
        ROI = image[y:y+h, x:x+w]
        cv2.imwrite(path.format(i), ROI)

        # each contour will be added to a dictionary
        tmp = {
            "xmin": x,
            "ymin": y,
            "xmax": x+w,
            "ymax": y+h,
            "path": path.format(i)
        }
        obj[i] = tmp

    return obj

# given an image and a list of rectangles
# merge rectangles that are close (both horizontally and vertically)
def mergeRects(img, rects):
    rectsUsed = []
    acceptedRects = []

    # merge threshold
    xThr = 30
    yThr = 30


    # add padding to final bounding boxes in case edge letters are cut
    xpadding = 10
    ypadding = 10

    minArea = 1000
    
    for _ in rects:
        rectsUsed.append(False)

    # debug
    # textLabelsImg = img.copy()
    # for rect in rects:
    #     cv2.rectangle(textLabelsImg, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (121, 11, 189), 2)
    # cv2.imwrite("results/convexHull_textLabelBoxes.png", textLabelsImg)

    def getXFromRect(item):
        return item[0]

    # sort by mininum x of each rectangle
    rects.sort(key = getXFromRect)

    # reference: https://stackoverflow.com/questions/55376338/how-to-join-nearby-bounding-boxes-in-opencv-python
    # Iterate all initial bounding rects
    for supIdx, supVal in enumerate(rects):
        if (rectsUsed[supIdx] == False):
            # Initialize current rect
            currxMin = supVal[0]
            currxMax = supVal[0] + supVal[2]
            curryMin = supVal[1]
            curryMax = supVal[1] + supVal[3]

            # This bounding rect is used
            rectsUsed[supIdx] = True

            # Iterate all initial bounding rects
            # starting from the next
            for subIdx, subVal in enumerate(rects[(supIdx+1):], start = (supIdx+1)):
                # Initialize merge candidate
                candxMin = subVal[0]
                candxMax = subVal[0] + subVal[2]
                candyMin = subVal[1]
                candyMax = subVal[1] + subVal[3]

                if (candyMax > curryMax + yThr):
                    continue

                if (candyMin < curryMin - yThr):
                    continue

                # Check if x distance between current rect
                # and merge candidate is small enough
                if (candxMin <= currxMax + xThr):

                    # Reset coordinates of current rect
                    currxMax = candxMax
                    curryMin = min(curryMin, candyMin)
                    curryMax = max(curryMax, candyMax)

                    # Merge candidate (bounding rect) is used
                    rectsUsed[subIdx] = True
                else:
                    break

            # No more merge candidates possible, accept current rect
            area = ((currxMax - currxMin) * (curryMax - curryMin))  
            if (area >= minArea):
                acceptedRects.append([currxMin - xpadding, curryMin - ypadding, currxMax - currxMin + xpadding, curryMax - curryMin + ypadding])
    return acceptedRects

def findAllLabels():
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

# returns json object containing each minimum bounding box of a word in the image
def findTextLabels(imgFile):
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
    _, textLabels = filterTextBoxes(hulls)

    # write image containing text labels
    # textLabelsImg = img.copy()
    # cv2.drawContours(textLabelsImg, textLabels, -1,
    #                  (255, 0, 0), thickness=1, lineType=cv2.LINE_AA)
    # cv2.imwrite("results/convexHull_textLabels.png", textLabelsImg)

    # find the minimum bounding box for each rectangle
    rects = []
    for contour in textLabels:
        rect = cv2.boundingRect(contour)
        rects.append(rect)

    # firstRound = mergeRects(img, rects)
    acceptedRects = mergeRects(img, rects)
    
    # debug
    textLabelsImg = img.copy()
    for rect in acceptedRects:
        result = cv2.rectangle(textLabelsImg, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (121, 11, 189), 2)
    cv2.imwrite("results/convexHull_results.png", result)

    # crop the image for each final rectangle
    obj = getROI(img, acceptedRects)
    print(json.dumps(obj, indent=4))

    return obj

if __name__ == "__main__":
    # provide image file as cli argument
    imgFile = sys.argv[1]
    findTextLabels(imgFile)