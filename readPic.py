import cv2 as cv
import numpy as np


path = r"C:\Users\David\Desktop\cvPics\img2.jpg"

frame = cv.imread(path)
frame = cv.resize(frame, (800, 800))
frameGray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
blurred = cv.GaussianBlur(frameGray, (99, 99), 0)
ret, mask = cv.threshold(frameGray, 50, 255, cv.THRESH_BINARY_INV)
masked = cv.bitwise_and(frame, frame, mask = mask)
contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
contour = max(contours, key = cv.contourArea, default=0)

mask = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)
black = np.zeros_like(mask)

frame2 = cv.drawContours(black, [contour], -1, (255, 255, 255), -1)

while True:


    cv.imshow("frame",frame2)



    if cv.waitKey(0) == ord('q'):
        break

cv.destroyAllWindows
