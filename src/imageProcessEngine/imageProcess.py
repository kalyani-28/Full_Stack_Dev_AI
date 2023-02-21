import imageProcessEngine.Image as Image
import imageProcessEngine.mapping as mapping

import sys

def getElements(imgPath):
    from imageProcessEngine.yolo import infer
    return infer.run(imgPath)

def getLabels(imgPath):
    from imageProcessEngine.htr import textSegment
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
