from time import sleep
import time
import cv2 as cv
import numpy as np
import threading
import camera_func as cfu
import config as conf
import drive as dr

servoX = dr.Servo(conf.servoPinX)
servoY = dr.Servo(conf.servoPinY)

servoX.stopServo()
servoY.stopServo()
cap = cv.VideoCapture(0)

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
obj_in_line = False
prev_obj_in_line = False
centered = False
last_cont = []

def res_servo(servoX, servoY):
    global selection
    selection = conf.frame_select
    servoX.setAngle(conf.servoX_pos)
    servoY.setAngle(conf.servoY_pos)
    print("reset servo")

image_draw = None

if not cap.isOpened():
    raise IOError("Cannot open webcam")

res_servo(servoX, servoY)

while True:
    print("centered: ")
    print(centered)
    currAngleX = servoX.getAngle()
    currAngleY = servoY.getAngle()
    _, frameOrig = cap.read()

    if(type(frameOrig) == type(None)):
        pass
    else:
        blurred, height, width = cfu.prep_pic(frameOrig)
        
        mask_obj = cfu.obj_mask(blurred, conf.green)
  
    try:
        contours, hierarchy = cv.findContours(mask_obj, cv.RETR_EXTERNAL ,cv.CHAIN_APPROX_NONE)

        for contour in contours:
            M = cv.moments(contour)
            if(M["m10"] !=0 and M["m01"] !=0 and M["m00"] !=0):
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                string = str(cX) + " " + str(cY)
                x,y,w,h = cv.boundingRect(contour)
                if(w > conf.width/30) and (h > conf.height/30):
                    color = (255, 0, 255)
                    
                    
                    if(y>= 0.66 * conf.height-10 and y<= 0.66 * conf.height+10):
                        color = (255, 255, 0)
                        obj_in_line = True                            

                    cv.rectangle(blurred, (x,y), (x+w,y+h), color, 5)
                    cv.putText(blurred, string, (x, y-10), cv.FONT_HERSHEY_TRIPLEX, 0.5, (0, 0, 255) )
    
    except Exception as e:
        print("cannot find object")
    if(obj_in_line == True):
        centered = cfu.aim_camera_obj(servoX, servoY, cX, cY, currAngleX, currAngleY)
        if (centered == True):
           path, index = cfu.save_pic(index, frameOrig, conf.path_pic_Pi)
           obj_in_line = False
           res_servo(servoX, servoY)
           print(path)

    try:
         cv.imshow("main", blurred)
         cv.imshow("mask", mask_obj)
    except Exception as e:
        print(str(e))
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()

