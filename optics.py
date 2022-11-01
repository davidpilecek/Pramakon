import numpy as np
import cv2 as cv
import config as conf
import camera_func as cfu
#import drive as dr

#robot = dr.Robot(conf.leftMot, conf.rightMot)

cap = cv.VideoCapture(0)

if not cap.isOpened():
    raise IOError("Cannot open webcam")

T = conf.threshold

angle = 0

ret = None

cX, cY = [0, 0]

while True:
    
    direction = 0

    _, frame = cap.read()
    


    if(type(frame) == type(None) or _ == False):
        pass
    else:
        height, width, blurred = cfu.prep_pic(frame)
        crop, area = cfu.crop_img(blurred, height, width)
        ret = cfu.balance_pic(crop, area, T)

    try:
        angle, image_draw = cfu.contours_line(blurred, ret, height, width)
             
        #cfu.decide(round(angle), robot)

        cv.imshow("window", ret)
        cv.imshow("orig", image_draw)
    

    except Exception as e:
        #robot.stop()
        print("No contours")


    if cv.waitKey(1) == ord('q'):
        #robot.stop()
        break

cap.release()
cv.destroyAllWindows()