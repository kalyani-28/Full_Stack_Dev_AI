import cv2 as cv

# size of kernel
kernel_size = 15

img = cv.imread('test2.jpg')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# make paper black and writing white
invert = cv.bitwise_not(gray)

# dilate and then erode to remove line imperfections
dilated = cv.dilate(invert, cv.getStructuringElement(cv.MORPH_RECT, (kernel_size, kernel_size)))
eroded = cv.erode(dilated, cv.getStructuringElement(cv.MORPH_RECT, (kernel_size, kernel_size)))

# revert to original color
clean = cv.bitwise_not(eroded)

cv.imwrite('test.jpg', clean)
