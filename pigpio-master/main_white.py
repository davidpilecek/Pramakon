from time import sleep

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

kernel = np.ones((3,3),np.uint8)

angle = 0

ret = None

cX, cY = [0, 0]

while True:

    direction = 0

    _, frame = cap.read()

    if(type(frame) == type(None)):
        pass
    else:
        blurred, height, width = cfu.prep_pic(frame)
        crop, area = cfu.crop_img_line(blurred, height, width)
        ret, T_final = cfu.balance_pic(crop, area, T)
 
    try:
        angle, image_draw = cfu.contours_line(blurred, ret, height, width)

    except Exception as e:

         print("No contours")
         robot.stop()
         sleep(1)
         
    angle = round(angle)

    dev, way = cfu.deviance(angle)
    
    if dev + conf.basePwm > conf.pwmMax:
        if way == 1:
            robot.moveL(conf.basePwm)
        elif way == -1:
            robot.moveR(conf.basePwm)
    else:
        cfu.steer(conf.basePwm, dev, way, robot)

    try:
        cv.imshow("img",image_draw )
        print(T_final)
    except Exception as e:
        print(str(e))
    

    if cv.waitKey(1) == ord('q'):
        break
robot.stop()
cap.release()
cv.destroyAllWindows()

