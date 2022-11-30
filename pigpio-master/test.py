#find object of specific color, get as close to it as possible and take 
#picture of it, then aim back on the white track and drive along do NOT 
#get off the white track, once you have to turn the camera 90 degrees to 
#the left or right, that means it's as close as possible and therefore 
#you can take a pic of it.

#create line to center of contour of red object, once it reaches 0 or 180 with regard to the center of the screen, then turn the camera 
#to it so that the entire object is in the center of the frame and snap it


from time import sleep

import cv2 as cv
import numpy as np

import camera_func as cfu
import config as conf

cap = cv.VideoCapture(0)

if not cap.isOpened():
    raise IOError("Cannot open webcam")

T = conf.threshold

frame_draw = []

angle = 0

ret = None

cX, cY = [0, 0]

index = 0

go_aim = False

angle_obj = []

arr_empty = np.zeros([conf.height, conf.width], dtype=int)

sleep(0.5)
while True:

    direction = 0

    _, frameOrig = cap.read()

    if(type(frameOrig) == type(None)):
        pass
    else:
        blurred, height, width = cfu.prep_pic(frameOrig)
        mask_obj, hsvImg = cfu.obj_mask(frameOrig, conf.blue)
        crop, area = cfu.crop_img_line(blurred, height, width)
        ret, T_final = cfu.balance_pic(crop, area, T)
 
    try:
        angle, image_draw = cfu.contours_line(frameOrig, ret, height, width)
        
    except Exception as e:
         print("No line contours")
         sleep(1)
    
    if(not np.array_equal(mask_obj, arr_empty)):
        angle_obj, image_draw_obj, obj_x, obj_y = cfu.contours_obj(image_draw, mask_obj, height, width)
    else:
        angle_obj, image_draw_obj, obj_x, obj_y = [0, 0, 0, 0]
        print("No object contour")

    dev, way = cfu.deviance(angle)

    try:
        cv.imshow("main", hsvImg)
    except Exception as e:
        print(str(e))

    if cv.waitKey(1) == ord('q'):
        break
cap.release()
cv.destroyAllWindows()
