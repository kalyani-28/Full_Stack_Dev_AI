import json
from typing import Dict, Tuple

def getMidPoint(x1, x2, y1, y2) -> Tuple[int, int]:
    midx = round((x1 + x2)/2)
    midy = round((y1 + y2)/2)
    return (midx, midy)

def processCoordinates(coordinates) -> Dict:
    for i in coordinates:
        coordinates[i]["midpoint"] = getMidPoint(coordinates[i]["xmin"],
                                                 coordinates[i]["xmax"], 
                                                 coordinates[i]["ymin"], 
                                                 coordinates[i]["ymax"])
    return coordinates

class Image:
    def __init__(self, imgPath, elements, labels) -> None:
        self.imgPath = imgPath
        self.labels = processCoordinates(labels)
        self.elements = processCoordinates(elements)
        self.mapping = {}

    def prettyPrint(self) -> None:
        print("Image Path: " + self.imgPath)
        print(json.dumps(self.elements, indent=4))
        print(json.dumps(self.labels, indent=4))
        print(json.dumps(self.mapping, indent=4))

    def setMapping(self, mapping):
        self.mapping = mapping