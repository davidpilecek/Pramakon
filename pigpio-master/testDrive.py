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

frame_draw = []
angle = 0
ret = None
cX, cY = [0, 0]
index = 0
last_time = 0
try_line = True
selection = conf.crop_selection
line_found = 0
do_drive = False

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

    if(try_line == False):
        print("NOT TRYING LINE")
        pass
    else:
        try:
            angle, image_draw = cfu.contours_line(frameOrig, ret, height, width)
            print("FOUND LINE")
            line_found = 1
            do_drive = True
        except Exception as e:
            print("No line")
            line_found = 0
            try_line = False

    if (line_found == 0):
         print("stopping bot")
         do_drive = False
         try_line = True

#         last_time = time.time()
#         servoY.setAngle(conf.servoY_pos)
        #if (dir == -1):
        #    print("looking right")
       #     servoX.setAngle(currAngleX + 20)
      #  elif (dir == 1):
     #       print("looking left")
    #        servoX.setAngle(currAngleX - 20)
#         if(time.time() - last_time >= 5):
#             servoX.setAngle(conf.servoX_pos)
#             servoY.setAngle(conf.servoY_pos)
#             print("returned")

    dev, dir = cfu.deviance(angle)

    if(do_drive == True):
        if dev + conf.basePwm > conf.pwmMax:
            if dir == 1:
                robot.moveL(conf.basePwm)
            elif dir == -1:
                robot.moveR(conf.basePwm)

        else:
            last_direction = cfu.steer(conf.basePwm, dev, dir, robot)
    else:
            robot.stop()
    try:
        cv.imshow("main", image_draw)

    except Exception as e:
        print("no image to print")    
        robot.stop()
    if cv.waitKey(1) == ord('q'):
        break

robot.stop()    
cap.release()
cv.destroyAllWindows()
