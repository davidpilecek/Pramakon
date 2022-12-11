from time import sleep
import time
import cv2 as cv
import numpy as np
import camera_func as cfu
import config as conf


cap = cv.VideoCapture(0)

cap.set(3, 200)
cap.set(4, 200)

dire = 0
frame_draw = []
angle = 0
ret = None
cX, cY = [0, 0]
index = 0
res = True
last_time = 0
try_line = True
selection = conf.frame_select
line_found = True
line_count = 0

image_draw = None

if not cap.isOpened():
    raise IOError("Cannot open webcam")

while True:
   
    _, frameOrig = cap.read()

    if(type(frameOrig) == type(None)):
        pass
    else:
        blurred, height, width = cfu.prep_pic(frameOrig)
        ret, area = cfu.crop_img_line_color(blurred, height, width, conf.blue, selection)
        mask_obj = cfu.obj_mask(blurred, conf.green)


    try:
        obj_angle, img_draw, obj_x, obj_y = cfu.contours_obj(blurred, mask_obj)
    except Exception as e:
        print("cannot find object")

    dev, dire = cfu.deviance(angle)
    
    try:
        cv.imshow("main", img_draw)
        cv.imshow("mask", mask_obj)
    except Exception as e:
        print(str(e))
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()