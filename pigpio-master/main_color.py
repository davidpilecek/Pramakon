from time import sleep

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
last_direction = 0
selection = conf.crop_selection

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

    except Exception as e:
        robot.stop()
        print("Trying to find line")
        sleep(1)
        
    try:
        obj_angle, img_draw, obj_x, obj_y = cfu.contours_obj(image_draw, mask_obj)
        print("object found")
    except Exception as e:
        print("cannot find object")
        if image_draw.all() != None:
             img_draw = image_draw
    dev, way = cfu.deviance(angle)

    if dev + conf.basePwm > conf.pwmMax:
        if way == 1:
            robot.moveL(conf.basePwm)
            last_direction = 1
        elif way == -1:
            robot.moveR(conf.basePwm)
            last_direction = -1
    else:
        last_direction = cfu.steer(conf.basePwm, dev, way, robot)

    try:
        cv.imshow("main", img_draw)

    except Exception as e:
        print(str(e))    

    if cv.waitKey(1) == ord('q'):
        break
robot.stop()    
cap.release()
cv.destroyAllWindows()
