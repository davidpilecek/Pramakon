import numpy as np
import cv2 as cv
import time
import camera_func as cfu
from config import *

height = 250
width = 250

cap = cv.VideoCapture(0)

if not cap.isOpened():
    raise IOError("Cannot open webcam")

while True:

    _, frame_orig = cap.read()
    if(type(frame_orig) == type(None) or _ == False):
        pass

    frame = cv.resize(frame_orig, (250, 250))

    blurred = cv.GaussianBlur(frame, (7, 7), 0)

    frame_hsv = cv.cvtColor(blurred, cv.COLOR_BGR2HSV)
    
    mask_obj = cv.inRange(frame_hsv, GREEN_HSV_RANGE[0], GREEN_HSV_RANGE[1])

    frame_bw = cv.cvtColor(blurred, cv.COLOR_BGR2GRAY) 

    mask = cv.adaptiveThreshold(frame_bw, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 91, 20)
   
    mask_del = mask
    #mask_del = cv.bitwise_xor(mask, mask_obj)

    crop_selection = 100/(100 - 60)

    height_1 = height/crop_selection

    vertices = [(0, height_1), (0, height),(width, height), (width, height_1)]
    vertices = np.array([vertices], np.int32)

    #create pure black frame size of image
    mask_black = np.zeros_like(mask_del)
    
    match_mask_color = [255, 255, 255]

    cv.fillPoly(mask_black, vertices, match_mask_color)

    masked_image = cv.bitwise_and(mask_del, mask_black)     
    frame_bw = cv.cvtColor(frame_bw, cv.COLOR_GRAY2BGR)

    contours, hierarchy = cv.findContours(masked_image, cv.RETR_TREE ,cv.CHAIN_APPROX_NONE)
    if(len(contours) > 0):
    	contour = max(contours, key = cv.contourArea)
    	cv.drawContours(frame_bw, [contour], -1, (0, 255, 0), -1)

    try:
        cv.imshow("masked_image", frame_bw)
        cv.imshow("mask_obj", mask_obj)
        cv.imshow("frame", frame_orig)
      
    except Exception as e:
        print(str(e))

    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()

