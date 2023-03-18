from time import sleep
from time import time
import cv2 as cv
import camera_func as cfu
from config import *
from shutil import rmtree
from os import mkdir
import threading
from drive import *

robot = Robot(LEFT_MOTOR_PIN, RIGHT_MOTOR_PIN)
servoX = Servo(X_SERVO_PIN)
servoY = Servo(Y_SERVO_PIN)

servoX.setAngle(SERVOX_POS)
servoY.setAngle(SERVOY_POS)
#servoX.stopServo()
#servoY.stopServo()
cap = cv.VideoCapture(0)

#variables
dire = 0
angle = 0
ret = None
cX, cY = [125, 125]
index = 0
try_line = True
selection = FRAME_SELECT
line_found = True
line_count = 0
obj_in_line = False
prev_obj_in_line = False
centered = False
angleX = 0
angleY = 0
image_draw = None
area = HEIGHT_OF_IMAGE * WIDTH_OF_IMAGE
cent_last = False
saved_pic = False
do_aim = True
contour = []

if(UPLOAD):
    rmtree(PATH_PIC_PI)
    mkdir(PATH_PIC_PI)

def save_picture():
    global saved_pic
    global index
    global servoX
    global servoY
    global cent_last
    sleep(2)
    print("checking if saved")
    if(saved_pic):
        print("alr saved")
    else:
        print("saving pic")
        print(f"{cX}, {cY}")
        path, index = cfu.save_pic(index, frameOrig, PATH_PIC_PI)
        print(path)
        saved_pic = 1
        servoX.setAngle(SERVOX_POS)
        servoY.setAngle(SERVOY_POS)
        cent_last = False
if not cap.isOpened():
    raise IOError("Cannot open webcam")

while True:
    #print(f"do_aim:{do_aim}")
    #print(f"in_line:{obj_in_line}")
    #print(f"saved pic: {saved_pic}")
    #print(servoX.getAngle())
    _, frameOrig = cap.read()

    if(type(frameOrig) == type(None)):
        pass
    else:
        img_hsv, img_bw, image_draw = cfu.prep_pic(frameOrig)
        mask_obj = cv.inRange(img_hsv, GREEN_HSV_RANGE[0], GREEN_HSV_RANGE[1])
        mask_line = cfu.crop_img_line_color(img_bw, selection)

        cv.rectangle(image_draw, (CENTER_X - CENTER_TOLERANCE, CENTER_Y - CENTER_TOLERANCE), (CENTER_X + CENTER_TOLERANCE, CENTER_Y + CENTER_TOLERANCE), (0, 0, 255), 2) 
        cv.line(image_draw, (0,int(SEEK_OBJECT * HEIGHT_OF_IMAGE-30)), (WIDTH_OF_IMAGE, int(SEEK_OBJECT * HEIGHT_OF_IMAGE-30)), (255,255,255), 3)
        cv.line(image_draw, (0,int(SEEK_OBJECT * HEIGHT_OF_IMAGE+30)), (WIDTH_OF_IMAGE, int(SEEK_OBJECT * HEIGHT_OF_IMAGE+30)), (255,255,255), 3)

    try:
            contours, hierarchy = cv.findContours(mask_obj, cv.RETR_EXTERNAL ,cv.CHAIN_APPROX_NONE)
            contour = max(contours, key = cv.contourArea)
            x,y,w,h = cv.boundingRect(contour)
            M = cv.moments(contour)

            if(w > WIDTH_OF_IMAGE/8) and (h > HEIGHT_OF_IMAGE/8) and (cv.contourArea(contour) > area/150) :

                if(M["m10"] !=0 and M["m01"] !=0 and M["m00"] !=0):
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    string = str(cX) + " " + str(cY)
                    color = (255, 0, 255)

                    if(cY>= SEEK_OBJECT * HEIGHT_OF_IMAGE-30 and cY<= SEEK_OBJECT * HEIGHT_OF_IMAGE+30):
                        color = (255, 255, 0)
                        obj_in_line = True
                        curr_cont = (cX, cY) 
                    else:
                        obj_in_line = False
                        prev_obj_in_line = False

                    cv.rectangle(image_draw, (x,y), (x+w,y+h), color, 5)
                    cv.putText(image_draw, string, (x, y-10), cv.FONT_HERSHEY_TRIPLEX, 0.5, (0, 0, 255))
            else:
                print("no obj in frame")
                saved_pic = False
                obj_in_line = False
                do_aim = True
                prev_obj_in_line = False
                centered = False
                cent_last = False

    except Exception as e:
             contours = []

    if(obj_in_line == True and prev_obj_in_line == False):
        prev_obj_in_line = True

    if(obj_in_line and do_aim):
       print(f"cX {cX}")
       print(f"cY {cY}") 
       centered, angleX, angleY = cfu.aim_camera_obj(servoX, servoY, cX, cY)

    if(centered and not cent_last):
        do_aim = False
        cent_last = True
        timer = threading.Timer(2.0, save_picture)
        timer.start()

    #show feed
    try:
        cv.imshow("draw", image_draw)
    except Exception as e:
        print(str(e))
    if cv.waitKey(1) == ord('q'):
        break
cap.release()
cv.destroyAllWindows()
servoX.reset(servoX, SERVOX_POS)
servoY.reset(servoY, SERVOY_POS)
#servoX.stopServo()
#servoY.stopServo()
