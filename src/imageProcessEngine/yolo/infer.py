import torch
import cv2

import sys
sys.path.append('..') # add parent directory to path to import configs

import json
import os

from configs.definitions import ROOT_DIR

modelPath = os.path.join(ROOT_DIR, 'yolo/model/best.pt')

# retrieve yolo model
# training instructions in main readme
def getModel():
    return torch.hub.load('ultralytics/yolov5', 'custom', modelPath)

# return objects detected by yolo in formated json
def run(imgFile):
    # run model
    model = getModel()
    im = imgFile
    results = model(im)

    # retrieve model output
    results.print()
    results.save()
    
    # parse output as json object
    parsed = json.loads(results.pandas().xyxy[0].to_json(orient ='index'))
    print(json.dumps(parsed, indent=4))

    return parsed

if __name__ == "__main__":
    imgFile = sys.argv[1]
    print(imgFile)
    run(imgFile)