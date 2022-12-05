import numpy as np
import cv2 as cv
import config as conf
import camera_func as cfu
from time import sleep

cap = cv.VideoCapture(conf.path)

if not cap.isOpened():
    raise IOError("Cannot open webcam")

T = conf.threshold

frame_draw = []

kernel = np.ones((3,3),np.uint8)

angle = 0

ret = None

cX, cY = [0, 0]

while True:

    direction = 0

    _, frameOrig = cap.read()

    if(type(frameOrig) == type(None)):
        pass
    else:
        blurred, height, width = cfu.prep_pic(frameOrig)
        mask_blue = cfu.obj_mask(frameOrig, conf.blue)
        crop, area = cfu.crop_img_line(blurred, height, width)
        ret, T_final = cfu.balance_pic(crop, area, T)
 
    try:
        image_show, size = cfu.contours_calibrate(frameOrig, ret, height, width)

    except Exception as e:    
         print("No contours")
         sleep(1)
        
    sizeavg = round(sum(size[:2])/2)

    try:
        cv.imshow("main", image_show)
        print("average size of 50 mm from 1 m distance: ", sizeavg)
    except Exception as e:
        print(str(e))    

    if cv.waitKey(1) == ord('q'):
        break
cap.release()
cv.destroyAllWindows()

