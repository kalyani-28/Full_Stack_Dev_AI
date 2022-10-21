import cv2 as cv
import numpy as np
from .textBoxFinder import textBoxFinder
from .handwriting import getLabels


def merge(box, label):
    x1 = min(box[0], label[0])
    y1 = min(box[1], label[1])
    x2 = max(box[0] + box[2], label[2])
    y2 = max(box[1] + box[3], label[3])

    newbox = list((x1, y1, x2, y2, label[4]))
    return newbox


def matchLabelBox(boxes, label):
    labels = label.copy()
    del labels[0]
    matched = list(())
    spread = 50
    i = 0
    while i < len(boxes):
        j = 0
        while j < len(labels):
            if (boxes[i][1] - spread < labels[j][1] and boxes[i][3] + boxes[i][1] + spread > labels[j][3]) or (
                    labels[j][1] - spread < boxes[i][1] and labels[j][3] + spread > boxes[i][3] + boxes[i][1]):
                newBox = merge(boxes[i], labels[j])
                matched.append(
                    list((newBox[0], newBox[1], newBox[2], newBox[3], newBox[4])))
                del labels[j]
                break
            j += 1
        i += 1

    return matched


def labelArea(label):
    x1, y1, x2, y2, _ = label
    area = abs(x2 - x1) * abs(y2 - y1)
    return area


def getTextbox_Labels(file_in):

    # get text boxes
    nparr = np.fromstring(file_in, np.uint8)
    img = cv.imdecode(nparr, cv.IMREAD_COLOR)
    imgXLen = img.shape[1]
    # get labels
    labels = getLabels(nparr, imgXLen)
    # find area of largest label

    biggestLabel = max(labels[1:], key=lambda l: labelArea(l))
    biggestLabelArea = labelArea(biggestLabel)

    # get text boxes
    boxFinder = textBoxFinder(img, biggestLabelArea)
    boxes = boxFinder.getTextBoxes()

    # match labels to textboxes
    matched = matchLabelBox(boxes, labels)

    return matched
