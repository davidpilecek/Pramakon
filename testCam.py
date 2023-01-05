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

# used to record the time when we processed last frame
prev_frame_time = 0
 
# used to record the time at which we processed current frame
new_frame_time = 0
fps_count = []

while True:

    _, frame_orig = cap.read()
    if(type(frame_orig) == type(None) or _ == False):
        pass

    frame = cv.resize(frame_orig, (250, 250))

    blurred = cv.GaussianBlur(frame, (7, 7), 0)

    frame_hsv = cv.cvtColor(blurred, cv.COLOR_BGR2HSV)
    
    mask_obj = cv.inRange(frame_hsv, GREEN_HSV_RANGE[0], GREEN_HSV_RANGE[1])

    frame_bw = cv.cvtColor(blurred, cv.COLOR_BGR2GRAY) 

    crop_selection = 100/(100 - 60)

    height_1 = height/crop_selection

    vertices = [(0, height_1), (0, height),(width, height), (width, height_1)]
    vertices = np.array([vertices], np.int32)

    #create pure black frame size of image
    mask_black = np.zeros_like(frame_bw)
    
    match_mask_color = [255, 255, 255]

    cv.fillPoly(mask_black, vertices, match_mask_color)

    #cv.fillPoly(mask_white, vertices, match_mask_color)   
    mask_white = cv.bitwise_not(mask_black)

    masked_image = cv.bitwise_and(frame_bw, mask_black)
    masked_image = cv.bitwise_or(masked_image, mask_white)
   
    _, mask = cv.threshold(masked_image,100, 255, cv.THRESH_BINARY_INV)
    
    mask = cv.bitwise_xor(mask, mask_obj)

    contours, hierarchy = cv.findContours(mask, cv.RETR_TREE ,cv.CHAIN_APPROX_NONE)

    contour = max(contours, key = cv.contourArea, default=0)
    
    frame_bw = cv.cvtColor(frame_bw, cv.COLOR_GRAY2BGR)
    cv.drawContours(frame_bw, [contour], -1, (0, 255, 0), 5)

    try:
        cv.imshow("window", mask_obj)
        cv.imshow("mask", frame_bw)
        cv.imshow("mask_line", mask)
      
    except Exception as e:
        print(str(e))

    if cv.waitKey(1) == ord('q'):
        break

cap.release()
print(mask_white)
cv.destroyAllWindows()

