import imageProcessEngine.Image as Image
import imageProcessEngine.mapping as mapping

import sys

# run yolo model
def getElements(imgPath):
    from imageProcessEngine.yolo import infer
    return infer.run(imgPath)

# run htr model 
def getLabels(imgPath):
    from imageProcessEngine.htr import textSegment
    return textSegment.processImage(imgPath)

def run(imgPath):
    elements = getElements(imgPath) # retreieve text boxes 

    labels = getLabels(imgPath) # retrieve text labels

    img = Image.Image(imgPath, elements, labels)

    img.setMapping(mapping.mapper(img)) ## associate text boxes with text labels
    
    img.prettyPrint() # debug 
    return img

if __name__ == "__main__":
    imgPath = sys.argv[1]
    run(imgPath)
