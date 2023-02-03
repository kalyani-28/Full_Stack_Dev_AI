import Image
import mapping

import sys

def getElements(imgPath):
    from yolo import infer
    return infer.run(imgPath)

def getLabels(imgPath):
    from htr import textSegment
    return textSegment.processImage(imgPath)

def run(imgPath):
    elements = getElements(imgPath)

    labels = getLabels(imgPath)

    img = Image.Image(imgPath, elements, labels)

    img.setMapping(mapping.mapper(img))
    
    img.prettyPrint()
    return img

if __name__ == "__main__":
    imgPath = sys.argv[1]
    run(imgPath)
