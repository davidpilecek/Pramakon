
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

servoX.setAngle(110)
servoY.setAngle(110)
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
    try:
        obj_angle, img_draw, obj_x, obj_y = cfu.contours_obj(frameOrig, mask_obj)
    except Exception as e:
        print("No object contour")
    
    if angle == 90:
        robot.straight(conf.basePwm)
    elif angle > 90:
        dev = angle - 90
        #turn Right
        way = -1
    elif angle < 90:
        dev = 90 - angle
        #turn Left
        way = 1
    

    if dev + conf.basePwm > conf.pwmMax:
        if way == 1:
            robot.moveL(conf.basePwm)
            servoX.setAngle(currAngleX + 20)
            last_time = time.time()
            if(time.time() - last_time >= 0.2):
                servoX.setAngle(currAngleX - 20)
                last_time = time.time()
        elif way == -1:
            robot.moveR(conf.basePwm)
            servoX.setAngle(currAngleX - 20)
            last_time = time.time()
            if(time.time() - last_time >= 0.5):
                servoX.setAngle(currAngleX + 20)
                last_time = time.time()
    else:
        if way == 1:
        #moving slightly left
            robot.moveBoth(conf.basePwm - dev, conf.basePwm + dev)

        elif way == -1:
        #moving slightly right
            robot.moveBoth(conf.basePwm + dev, conf.basePwm - dev)
            
    #shift camera at center of path
    if(angle > 90 + conf.ang_tol):
          servoX.setAngle(currAngleX - conf.step)
    elif(angle < 90 - conf.ang_tol):
          servoX.setAngle(currAngleX + conf.step)

    # if(condition to take pic of object):
    #     robot.stop()
    #     cfu.aim_camera_obj(servoX, servoY, obj_x, obj_y, currAngleX, currAngleY)
    #     if(obj_x == conf.centerX and obj_y == conf.centerY):
    #         cfu.save_pic(index, img_draw)
    #     servoX.setAngle(110)
    #     servoY.setAngle(110)
    #     robot.straight(conf.pwmMin)
    #     sleep(0.5)

    try:
        cv.imshow("main", img_draw)
    except Exception as e:
        print(str(e))    

    if cv.waitKey(1) == ord('q'):
        break
robot.stop()
cap.release()
cv.destroyAllWindows()
