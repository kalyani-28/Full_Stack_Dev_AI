from math import sqrt
import sys
import imageProcessEngine.Image as Image

def getDistance(point1, point2) -> int:
    return sqrt(pow(point2[0] - point1[0], 2) + pow(point2[1] - point1[1], 2))
    
def skipRulesInputText(element, label):
    return not label["xmin"] < round(element["xmax"]) or not label["ymin"] < round(element["ymax"])
def naiveMapping(img: Image) -> dict:
    elements = img.elements.copy()
    labels = img.labels.copy()

    mapping = {}

    for ind, i in enumerate(elements):
        element = elements[i]
        elementMidpoint = elements[i]["midpoint"]
        
        result = sys.maxsize
        index = ""

        for j in labels:
            label = labels[j]
            labelMidpoint = labels[j]["midpoint"]

            distance = getDistance(elementMidpoint, labelMidpoint)

            if (skipRulesInputText(element, label)):
                continue

            if (distance < result):
                result = distance
                index = j

        mapping[ind] = {}   
        if (img.elements[i]["name"] == "input-text"):
            mapping[ind]["type"] = "text"
        
        mapping[ind]["label"] = labels[index]["word"]
        
        del labels[index]

    return mapping

def modelMapping(img: Image) -> dict:
    return {}

# todo: add mapping between cd srimg.labels and img.elements
def mapper(img: Image) -> dict:
    return naiveMapping(img)

if __name__ == "__main__":
    elements = {
        "0": {
            "xmin": 269.7411499023,
            "ymin": 36.2162208557,
            "xmax": 511.3893737793,
            "ymax": 99.0652389526,
            "confidence": 0.9062408209,
            "class": 0,
            "name": "input-text"
        },
        "1": {
            "xmin": 266.3895263672,
            "ymin": 108.9644775391,
            "xmax": 518.9926147461,
            "ymax": 167.3574371338,
            "confidence": 0.8980023265,
            "class": 0,
            "name": "input-text"
        }
    }

    labels = {
        "0": {
            "xmin": 14,
            "ymin": 39,
            "xmax": 211,
            "ymax": 82,
            "path": "/home/bensuth/school/project-course/Full_Stack_Dev_AI/src/imageProcessEngine/results/ROI0.png",
            "word": "username"
        },
        "1": {
            "xmin": 15,
            "ymin": 99,
            "xmax": 195,
            "ymax": 170,
            "path": "/home/bensuth/school/project-course/Full_Stack_Dev_AI/src/imageProcessEngine/results/ROI1.png",
            "word": "passwond"
        },
        "3": {
            "xmin": 309,
            "ymin": 189,
            "xmax": 465,
            "ymax": 235,
            "path": "/home/bensuth/school/project-course/Full_Stack_Dev_AI/src/imageProcessEngine/results/ROI3.png",
            "word": "Remember"
        },
        "4": {
            "xmin": 489,
            "ymin": 202,
            "xmax": 541,
            "ymax": 237,
            "path": "/home/bensuth/school/project-course/Full_Stack_Dev_AI/src/imageProcessEngine/results/ROI4.png",
            "word": "me"
        }
    }

    img = Image.Image("/", elements, labels)
    img.setMapping(mapper(img))
    img.prettyPrint()