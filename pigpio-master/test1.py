
from time import sleep
import time
import cv2 as cv
import numpy as np

import camera_func as cfu
import config as conf
import drive as dr

robot = dr.Robot(conf.leftMot, conf.rightMot)
servoX = dr.Servo(conf.servoPinX)
servoY = dr.Servo(conf.servoPinY)

servoX.setAngle(conf.servoX_pos)
servoY.setAngle(conf.servoY_pos)
servoX.stopServo()
servoY.stopServo()

cap = cv.VideoCapture(0)
if not cap.isOpened():
    raise IOError("Cannot open webcam")
T = conf.threshold
frame_draw = []
angle = 0
ret = None
cX, cY = [0, 0]
index = 0
last_time = 0

dir = 0


while True:
    currAngleX = servoX.getAngle()
    currAngleY = servoY.getAngle()

    _, frameOrig = cap.read()

    if(type(frameOrig) == type(None)):
        pass
    else:
        blurred, height, width = cfu.prep_pic(frameOrig)
        ret, area = cfu.crop_img_line_color(blurred, height, width, conf.blue)
        mask_obj = cfu.obj_mask(blurred, conf.red)
               
    try:
        angle, img_draw = cfu.contours_line(img_draw, ret, height, width)
    except Exception as e:
        robot.stop()
        print("No contour")
        servoY.setAngle(conf.servoY_pos + 20)
        if(dir == -1):
            servoX.setAngle(conf.servoX_pos - 10)
            last_time = time.time()
            if(time.time() - last_time >= 0.5):
                servoX.setAngle(conf.servoX_pos)
                servoY.setAngle(conf.servoY_pos)
                
        elif(dir == 1):
            servoX.setAngle(conf.servoX_pos + 10)
            last_time = time.time()
            if(time.time() - last_time >= 0.5):
                servoX.setAngle(conf.servoX_pos)
                servoY.setAngle(conf.servoY_pos)
                

    if angle == 90:
        robot.straight(conf.basePwm)
        dir = 0
    elif angle > 90:
        dev = angle - 90
        #turn Right
        dir = -1
    elif angle < 90:
        dev = 90 - angle
        #turn Left
        dir = 1
    
    if dev + conf.basePwm > conf.pwmMax:
        if dir == 1:
            robot.moveL(conf.basePwm)
        elif dir == -1:
            robot.moveR(conf.basePwm)
    else:
        if dir == 1:
        #moving slightly left
            robot.moveBoth(conf.basePwm - dev, conf.basePwm + dev)

        elif dir == -1:
        #moving slightly right
            robot.moveBoth(conf.basePwm + dev, conf.basePwm - dev)

    try:
        cv.imshow("main", img_draw)
    except Exception as e:
        print(str(e))    

    if cv.waitKey(1) == ord('q'):
        break
robot.stop()
cap.release()
cv.destroyAllWindows()
