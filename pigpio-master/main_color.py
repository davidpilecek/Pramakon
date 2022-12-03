#find object of specific color, get as close to it as possible and take picture of it, then aim back on the track and drive along
#do NOT get off the track, once you have to turn the camera 90 degrees to the left or right, that means it's as close
#as possible and therefore you can take a pic of it.

#once the turn is so sharp it has to utilize only one wheel, tilt camera to that direction for one second, then return back


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
 
    try:
        angle, image_draw = cfu.contours_line(frameOrig, ret, height, width)

    except Exception as e:
        print("No contour")

    dev, way = cfu.deviance(angle)

    if dev + conf.basePwm > conf.pwmMax:
        if way == 1:
            robot.moveL(conf.basePwm)
            servoX.setAngle(currAngleX - 50)
            last_time = time.time()
            if(time.time() - last_time >= 0.5):
                servoX.setAngle(currAngleX + 50)
                last_time = time.time()
        elif way == -1:
            robot.moveR(conf.basePwm)
            servoX.setAngle(currAngleX + 50)
            last_time = time.time()
            if(time.time() - last_time >= 0.5):
                servoX.setAngle(currAngleX - 50)
                last_time = time.time()

    else:
        cfu.steer(conf.basePwm, dev, way, robot)

    try:
        cv.imshow("main", image_draw)
    except Exception as e:
        print(str(e))    

    if cv.waitKey(1) == ord('q'):
        break
cap.release()
cv.destroyAllWindows()
