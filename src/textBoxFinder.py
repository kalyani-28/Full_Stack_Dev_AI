import cv2
from imageHelper import segmentImage


class textBoxFinder:

    def __init__(self, img) -> None:
        """Construct with original cv2 image as argument"""
        self.img = img

    def getTextBoxes(self) -> list:
        """returns a list of rectangles for each textBox"""
        segmentedImg = segmentImage(self.img)
        contours = self.getContours(segmentedImg)
        approxContours = self.approximateContours(contours)
        hulls = self.getHulls(approxContours)
        textBoxes, _ = self.filterTextBoxes(hulls)
        textBoundingBoxes = self.boundingBox(textBoxes)
        return textBoundingBoxes

    def getContours(self, img):
        """get contours in an image"""
        # find edges
        edges = cv2.Canny(img, 50, 150)

        # find external contours
        contours, hierarchy = cv2.findContours(
            edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        return contours

    def approximateContours(self, contours: list):
        """Smoothen contours"""
        res = []
        for contour in contours:
            perimeter = cv2.arcLength(contour, True)
            epsilon = 0.02 * perimeter
            approximatedShape = cv2.approxPolyDP(contour, epsilon, True)
            res.append(approximatedShape)

        return res

    def getHulls(self, contours: list):
        """get convex hull for each contour"""
        return [cv2.convexHull(c, False) for c in contours]

    def filterTextBoxes(self, hulls: list):
        """Partition convex hulls into text labels and text boxes"""
        MIN_AREA = 1000
        textBoxes = []
        other = []
        for hull in hulls:
            if cv2.contourArea(hull) > MIN_AREA:
                textBoxes.append(hull)
            else:
                other.append(hull)

        return (textBoxes, other)

    def boundingBox(self, contours: list):
        """Get bounding box for each contour"""
        return [cv2.boundingRect(c) for c in contours]
