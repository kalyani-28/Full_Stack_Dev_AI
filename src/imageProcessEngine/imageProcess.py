from yolo import infer
import Image
import mapping

import sys

def run(imgPath):
    elements = infer.run(imgPath)

    # todo: add code to grab content from HTR
    img = Image.Image(imgPath, elements, {})

    img.setMapping(mapping.mapper(img))
    
    img.prettyPrint()
    return img

if __name__ == "__main__":
    imgPath = sys.argv[1]
    run(imgPath)
