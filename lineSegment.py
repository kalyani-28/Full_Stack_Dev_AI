import cv2 as cv
import numpy as np

minLineLength = 50
maxLineGap = 50

# read image
img = cv.imread('computer_drawn_lines1.png')
# convert to gray picture
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# find edges
edges = cv.Canny(gray, 50, 150, apertureSize=3)

# given edges use houghLines to find lines
lines = cv.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=minLineLength, maxLineGap=maxLineGap)
# add the lines to original img
for line in lines:
    x1, y1, x2, y2 = line[0]
    cv.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

# write out edges and img with lines detected
cv.imwrite('edges.jpg', edges)
cv.imwrite('houghlines4.jpg', img)

