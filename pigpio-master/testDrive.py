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

image_draw = None

if not cap.isOpened():
    raise IOError("Cannot open webcam")
T = conf.threshold
frame_draw = []
angle = 0
ret = None
cX, cY = [0, 0]
index = 0
last_time = 0

selection = conf.crop_selection
line_found = 0
dir = 0

while True:
    currAngleX = servoX.getAngle()
    currAngleY = servoY.getAngle()
    direction = 0

    _, frameOrig = cap.read()

    if(type(frameOrig) == type(None)):
        pass
    else:
        blurred, height, width = cfu.prep_pic(frameOrig)
        ret, area = cfu.crop_img_line_color(blurred, height, width, conf.blue, selection)
        mask_obj = cfu.obj_mask(blurred, conf.red)

    try:
        angle, image_draw = cfu.contours_line(frameOrig, ret, height, width)
        line_found = 1

    except Exception as e:
        print("No line")
        line_found = 0

    if (line_found == 0):
        robot.stop()
        last_time = time.time()
        servoY.setAngle(conf.servoY_pos)
        if (dir == -1):
            print("looking right")
            servoX.setAngle(currAngleX + 20)
        elif (dir == 1):
            print("looking left")
            servoX.setAngle(currAngleX - 20)
        if(time.time() - last_time >= 5):
            servoX.setAngle(conf.servoX_pos)
            servoY.setAngle(conf.servoY_pos)
            print("returned")

    dev, dir = cfu.deviance(angle)

    if dev + conf.basePwm > conf.pwmMax:
        if dir == 1:
            robot.moveL(conf.basePwm)
        elif dir == -1:
            robot.moveR(conf.basePwm)

    else:
        last_direction = cfu.steer(conf.basePwm, dev, dir, robot)

    try:
        cv.imshow("main", image_draw)

    except Exception as e:
        print(str(e))    

    if cv.waitKey(1) == ord('q'):
        break
robot.stop()    
cap.release()
cv.destroyAllWindows()
