cat testDrive.py 
from time import sleep
import time
import cv2 as cv
import numpy as np
import threading
import camera_func as cfu
import config as conf
import drive as dr

robot = dr.Robot(conf.leftMot, conf.rightMot)
servoX = dr.Servo(conf.servoPinX)
servoY = dr.Servo(conf.servoPinY)

servoX.stopServo()
servoY.stopServo()
cap = cv.VideoCapture(0)

cap.set(3, 200)
cap.set(4, 200)

dire = 0
frame_draw = []
angle = 0
ret = None
cX, cY = [0, 0]
index = 0
res = True
last_time = 0
try_line = True
selection = conf.frame_select
line_found = True
line_count = 0

def search_seq(servoX, servoY, dire):
    robot.stop()
    global try_line
    global line_count
    line_count = 0
    print("setting servos")
    servoY.setAngle(conf.servoY_pos + 20)
    selection = conf.frame_select + 50
    if (dire == -1):
        print("looking right")
        servoX.setAngle(conf.servoX_pos - 20)
    elif(dire == 1):
        print("looking left")
        servoX.setAngle(conf.servoX_pos + 20)
    sleep(0.2)
    try_line = True

def res_servo():
    global servoX
    global servoY
    global selection
    selection = conf.frame_select
    servoX.setAngle(conf.servoX_pos)
    servoY.setAngle(conf.servoY_pos)

image_draw = None

if not cap.isOpened():
    raise IOError("Cannot open webcam")

res_servo()

while True:
    currAngleX = servoX.getAngle()
    currAngleY = servoY.getAngle()

    _, frameOrig = cap.read()

    if(type(frameOrig) == type(None)):
        pass
    else:
        blurred, height, width = cfu.prep_pic(frameOrig)
        ret, area = cfu.crop_img_line_color(blurred, height, width, conf.blue, selection)
        mask_obj = cfu.obj_mask(blurred, conf.red)

    if(try_line == False):
        pass
    else:
        try:
            angle, image_draw = cfu.contours_line(frameOrig, ret, height, width)
            res_servo()
            line_found = True
            line_count += 1
        except Exception as e:
            line_found = False

    if (line_found == False  and try_line == True):
         try_line = False
         search_seq(servoX,servoY, dire)

    #if object is at about to disappear from the image, aim the camera at the center of the object, take picture 
    #of it, wait a second and then return servos to their original position
    # if (obj_y == conf.height):
    #     while obj_x != conf.centerX and obj_y != conf.centerY:
    #         cfu.aim_camera_obj(servoX, servoY, obj_x, obj_y, currAngleX, currAngleY)
    #         break
    #     sleep(0.5)
    #     pic_path, index = cfu.save_pic(index, frameOrig)
    #     sleep(0.5)
    #     res_servo()

    try:
        obj_angle, img_draw, obj_x, obj_y = cfu.contours_obj(image_draw, mask_obj)
    except Exception as e:
        print("cannot find object")
        img_draw = image_draw

    dev, dire = cfu.deviance(angle)

    if dev + conf.basePwm > conf.pwmMax:
        print("sharp")
        print(dev)
        if dire == 1:
            robot.moveL(conf.basePwm)
        elif dire == -1:
            robot.moveR(conf.basePwm)
    else:
            cfu.steer(conf.basePwm, dev, dire, robot)

    try:
         cv.imshow("main", img_draw)
    except Exception as e:
        robot.stop()
    if cv.waitKey(1) == ord('q'):
        break

robot.stop()
cap.release()
cv.destroyAllWindows()