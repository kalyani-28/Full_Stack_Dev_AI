import os
import io
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
import cv2 as cv
# import pandas as pd

# important data used
key = r'C:\Users\ianst\PycharmProjects\pythonProject\projectcourse-343000-75d1307c8740.json'
folder_in = r'C:\Users\ianst\PycharmProjects\pythonProject\Images'
image_in = 'test1.jpg'
image_location_out = 'C:\\Users\\ianst\\PycharmProjects\\pythonProject\\Images\\image.jpg'

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

# print words detected
docText = response.full_text_annotation.text
print(docText)

text_annotations = response.text_annotations

for text in text_annotations:
    bound = text.bounding_poly.vertices
    x1, y1, x2, y2 = bound[0].x, bound[0].y, bound[2].x, bound[2].y
    cv.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)

cv.imwrite(image_location_out, img)
