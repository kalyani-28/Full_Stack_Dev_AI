import os
import io
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
import cv2 as cv
import numpy as np
# import pandas as pd


def mergeBox(box1, box2):

    x1 = min(box1[0], box2[0])
    y1 = min(box1[1], box2[1])
    x2 = max(box1[2], box2[2])
    y2 = max(box1[3], box2[3])

    newbox = list((x1, y1, x2, y2))
    return newbox


def mergeCordinates(cordinates):

    spread = 30
    gap = 200
    i = 1
    while i < len(cordinates):
        j = i+1
        while j < len(cordinates):
            if((cordinates[i][1]-spread < cordinates[j][1] and cordinates[i][3]+spread > cordinates[j][1]) or (cordinates[i][1]-spread < cordinates[j][3] and cordinates[i][3]+spread > cordinates[j][3])):
                if(abs(cordinates[i][2]-cordinates[j][0])<=gap or abs(cordinates[i][0]-cordinates[j][2])<=gap):
                    newBox = mergeBox(cordinates[i], cordinates[j])
                    cordinates[i][0], cordinates[i][1] = newBox[0], newBox[1]
                    cordinates[i][2], cordinates[i][3] = newBox[2], newBox[3]
                    del cordinates[j]
                    j = j-1
            j += 1
        i += 1

    return cordinates


def getCordinates(folder_in, image_in ):
    # important data used
    key = r'C:\Users\ianst\PycharmProjects\pythonProject\projectcourse-343000-75d1307c8740.json'

    # set GOOGLE_APPLICATION_CREDENTIALS to location of json key for access to Google API
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = key
    client = vision_v1.ImageAnnotatorClient()
    # path to folder with photo
    FOLDER_PATH = folder_in
    # name of photo
    IMAGE_FILE = image_in
    FILE_PATH = os.path.join(FOLDER_PATH, IMAGE_FILE)

    img = cv.imread(FILE_PATH)

    with io.open(FILE_PATH, 'rb') as image_file:
        content = image_file.read()

    image = vision_v1.types.Image(content=content)
    # returns json with data about writing
    response = client.document_text_detection(image=image)

    text_annotations = response.text_annotations

    cordinates = list(())

    for text in text_annotations:
        bound = text.bounding_poly.vertices
        x1, y1, x2, y2 = bound[0].x, bound[0].y, bound[2].x, bound[2].y
        cordinates.append(list((x1, y1, x2, y2)))

    return cordinates


def main():
    cordinates = getCordinates(r'C:\Users\ianst\PycharmProjects\pythonProject\Images', 'test4.jpg')
    mergedCordinates = mergeCordinates(cordinates)
    img = cv.imread(r'C:\Users\ianst\PycharmProjects\pythonProject\Images\test4.jpg')
    for i in range(1, len(mergedCordinates), 1):
        x1, y1, x2, y2 = mergedCordinates[i][0], mergedCordinates[i][1], mergedCordinates[i][2], mergedCordinates[i][3]
        cv.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)

    cv.imwrite(r'C:\Users\ianst\PycharmProjects\pythonProject\Images\image.jpg', img)



if __name__ == "__main__":
    main()
