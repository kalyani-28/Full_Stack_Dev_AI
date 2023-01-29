import json

class Image:
    def __init__(self, imgPath, elements, labels) -> None:
        self.imgPath = imgPath
        self.labels = labels
        self.elements = elements
        self.mapping = {}

    def prettyPrint(self) -> None:
        print("Image Path: " + self.imgPath)
        print(json.dumps(self.elements, indent=4))
        print(json.dumps(self.labels, indent=4))
        print(json.dumps(self.mapping, indent=4))

    def setMapping(self, mapping):
        self.mapping = mapping