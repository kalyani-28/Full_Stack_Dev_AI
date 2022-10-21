import os
import numpy as np
import io
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
import cv2 as cv


def mergeBox(box1, box2):

    x1 = min(box1[0], box2[0])
    y1 = min(box1[1], box2[1])
    x2 = max(box1[2], box2[2])
    y2 = max(box1[3], box2[3])

    string = ""

    if(box1[0] < box2[0]):
        string = box1[4] + " " + box2[4]
    else:
        string = box2[4] + " " + box1[4]

    newbox = list((x1, y1, x2, y2, string))
    return newbox


def mergeCordinates(cordinates, xLen):
    spread = 30
    gap = xLen / 10
    i = 1
    while i < len(cordinates):
        j = i+1
        while j < len(cordinates):
            if((cordinates[i][1]-spread < cordinates[j][1] and cordinates[i][3]+spread > cordinates[j][1])
               or (cordinates[i][1]-spread < cordinates[j][3] and cordinates[i][3]+spread > cordinates[j][3])):
                if(abs(cordinates[i][2]-cordinates[j][0]) <= gap or abs(cordinates[i][0]-cordinates[j][2]) <= gap):
                    newBox = mergeBox(cordinates[i], cordinates[j])
                    cordinates[i][0], cordinates[i][1] = newBox[0], newBox[1]
                    cordinates[i][2], cordinates[i][3] = newBox[2], newBox[3]
                    cordinates[i][4] = newBox[4]
                    del cordinates[j]
                    j = j-1
            j += 1
        i += 1

    return cordinates


def getCordinates(nparr):
    # important data used

    # set GOOGLE_APPLICATION_CREDENTIALS to location of json key for access to Google API
    client = vision_v1.ImageAnnotatorClient()

    # with io.open(folder_in, 'rb') as image_file:
    #content = image_file.read()

    content = nparr.tobytes()
    image = vision_v1.types.Image(content=content)
    # returns json with data about writing
    response = client.document_text_detection(image=image)
    text_annotations = response.text_annotations

    cordinates = []

    for text in text_annotations:
        bound = text.bounding_poly.vertices
        x1, y1, x2, y2 = bound[0].x, bound[0].y, bound[2].x, bound[2].y
        cordinates.append([x1, y1, x2, y2, text.description])

    return cordinates


def getLabels(nparr, imgXLen):
    # nparr: image file as np array
    cordinates = getCordinates(nparr)
    print("coordinates:", cordinates)
    print("xlen:", imgXLen)
    mergedCordinates = mergeCordinates(cordinates, imgXLen)

    return mergedCordinates
