#find object of specific color, get as close to it as possible and take picture of it, then aim back on the white track and drive along
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

index = 0

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
        angle, image_draw = cfu.contours_line(frameOrig, ret, height, width)
        angle_obj, image_draw_obj = cfu.contours_obj(image_draw, mask_blue, height, width)

    except Exception as e:    
         print(e)
         sleep(1)
         
          
    angle = round(angle)

    dev, way = cfu.deviance(angle)
    

    try:
        cv.imshow("main", image_draw_obj)
        print(angle)
    except Exception as e:
        print(str(e))    

    if cv.waitKey(1) == ord('q'):
        break
cap.release()
cv.destroyAllWindows()

