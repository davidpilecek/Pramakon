import cv2 as cv
import numpy as np
import config as conf
import matplotlib.pyplot as plt

kernel = np.ones((7, 7), np.uint8)

index = 1

path = r'C:\Users\david\Desktop\leaf0.jpg'
path_save = r'C:\Users\david\Desktop\cvPics\img'+ str(index) + r'.jpg'

frame_orig = cv.imread(path)
frame_orig = cv.resize(frame_orig, (500, 500))
black_img = np.zeros_like(frame_orig)
white_img = cv.bitwise_not(black_img)

frame_hsv = cv.cvtColor(frame_orig, cv.COLOR_BGR2HSV)
mask_hsv = cv.inRange(frame_hsv, conf.green[0], conf.green[1])
print(mask_hsv)
contours, _ = cv.findContours(mask_hsv, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
contour = max(contours, key=cv.contourArea)

img_cont = cv.drawContours(white_img, [contour], -1, (0, 0, 0), -1)

green_part = cv.bitwise_or(frame_orig, img_cont)

x, y, w, h = cv.boundingRect(contour)

img_draw_cropped = green_part[y:y+h, x:x+w]

img_draw_cropped = cv.resize(img_draw_cropped, (192,192))

cv.imshow("final image", img_draw_cropped)
cv.waitKey(0)