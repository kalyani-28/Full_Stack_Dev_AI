import sys
import json

import imageProcessEngine.htr.src.convexHull as convexHull
from imageProcessEngine.htr.src.main import initHTR

import re
regex = ".*\w+.*"

def processImage(imgFile):
    images = convexHull.findTextLabels(imgFile)
    result = {}

    for key in images:
        image = images.get(key)
        imgPath = image.get("path")
        sys.argv = [sys.argv[0], "--img_file", imgPath]
        word, _ = initHTR()

        if (re.search(regex, word) is not None):
            image["word"] = word
            result[key] = image

    return result

if __name__ == '__main__':
    # provide image file as cli argument
    imgFile = sys.argv[1]
    processImage(imgFile)