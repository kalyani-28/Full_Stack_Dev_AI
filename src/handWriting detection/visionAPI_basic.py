import os
import io
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
# import pandas as pd

# set GOOGLE_APPLICATION_CREDENTIALS to location of json key for access to Google API
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\ianst\PycharmProjects\pythonProject\projectcourse-343000-75d1307c8740.json'
client = vision_v1.ImageAnnotatorClient()
# path to folder with photo
FOLDER_PATH = r'C:\Users\ianst\PycharmProjects\pythonProject\Images'
# name of photo
IMAGE_FILE = 'test3.jpg'
FILE_PATH = os.path.join(FOLDER_PATH, IMAGE_FILE)

with io.open(FILE_PATH, 'rb') as image_file:
    content = image_file.read()

image = vision_v1.types.Image(content=content)
# returns json with data about writing
response = client.document_text_detection(image=image)

print(response)
