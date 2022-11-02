import numpy as np
import cv2 as cv
import config as conf
import camera_funct as cfu
import drive as dr
from time import sleep

robot = dr.Robot(conf.leftMot, conf.rightMot)

cap = cv.VideoCapture(0)

if not cap.isOpened():
    raise IOError("Cannot open webcam")

T = conf.threshold

frame_draw = []

kernel = np.ones((5,5),np.uint8)

angle = 0

ret = None

cX, cY = [0, 0]

while True:

    direction = 0

    _, frame = cap.read()

    if(type(frame) == type(None) or _ == False):
        pass
    else:
        blurred, height, width = cfu.prep_pic(frame)
        
        crop, area = cfu.crop_img(blurred, height, width)
        ret = cfu.balance_pic(crop, area, T)

    try:
        angle, image_draw = cfu.contours_line(blurred, ret, height, width)
        
    except Exception as e:
         robot.stop()
         print("No contours")
         sleep(1)
        
    angle = round(angle)
    #print(angle)

    dev, way = cfu.deviance(angle)

    if dev + conf.basePwm > conf.pwmMax:
        if way == 1:
           
            robot.moveL(conf.basePwm)
        elif way == -1:
            
            robot.moveR(conf.basePwm)
    else:
        cfu.steer(conf.basePwm, dev, way, robot)
    try:
        #print("showingImg")
        #cv.imshow("blank", np.zeros_like(image_draw))
        cv.imshow("window", image_draw)
    except Exception as e:
        print(str(e))
        robot.stop()
        
    if cv.waitKey(1) == ord('q'):
        break
robot.stop()
cap.release()
cv.destroyAllWindows()
