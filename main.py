from time import sleep
import cv2 as cv
import camera_func as cfu
from config import *
from drive import *
from simple_pid import PID
from shutil import rmtree
from os import mkdir
import threading

#definice PID
pid = PID(KP, KI, KD, setpoint = 90)
pid.output_limits = (-45, 45)
pid.sample_time = 0.01

#vytvoreni objektu robotu a servomotoru
robot = Robot(LEFT_MOTOR_PIN, RIGHT_MOTOR_PIN)
servoX = Servo(X_SERVO_PIN)
servoY = Servo(Y_SERVO_PIN)

#zachyceni snimku kamery
cap = cv.VideoCapture(0)

#promenne
dire = 0
angle = 0
ret = None
cX, cY = [125, 125]
index = 0
selection = FRAME_SELECT
line_count = 0
angleX = 0
angleY = 0
image_draw = None
area = HEIGHT_OF_IMAGE * WIDTH_OF_IMAGE
contour = []

#binarni promenne, kontrola stavu chuze programu
OBJ_IN_LINE = False
PREV_OBJ_IN_LINE = False
CENT_LAST = False
SAVED_PIC = False
CENTERED = False
DO_AIM = True
TRY_LINE = True
LINE_FOUND = True
MAY_STOP = True

#funkce pro vyhledani trate v pripade ztraty
def search_seq(servoX, servoY, dire):
    robot.stop()
    global TRY_LINE
    global line_count
    line_count = 0
    servoY.setAngle(SERVOY_POS + 20)
    if (dire == -1):
        servoX.setAngle(SERVOX_POS - 40)
    elif(dire == 1):
        servoX.setAngle(SERVOX_POS + 40)
    sleep(0.5)
    TRY_LINE = True

#funkce pro ulozeni fotografie
def save_picture():
    global SAVED_PIC
    global index
    global servoX
    global servoY
    global CENT_LAST
    global DO_DRIVE
    global TRY_LINE
    print("checking if saved")
    if(SAVED_PIC):
        print("alr saved")
    else:
        print("saving pic")
        print(f"{cX}, {cY}")
        path, index = cfu.save_pic(index, frameOrig, PATH_PIC_PI)
        print(path)
        SAVED_PIC = 1
        print("resetting")
        curr = round(servoX.getAngle())

#        if(curr > SERVOX_POS):
 #           for j in range(curr-SERVOX_POS):
  #              servoX.setAngle(curr - j)
   #             sleep(0.02)
    #    else:
     #       for i in range(abs(curr-SERVOX_POS)):
      #          servoX.setAngle(curr + i)
       #         sleep(0.02)
        print("reset")
        servoY.setAngle(SERVOY_POS)
        CENT_LAST = False
    DO_DRIVE = True
    TRY_LINE = True
#vychozi nastaveni servomotoru
servoX.setAngle(SERVOX_POS)
servoY.setAngle(SERVOY_POS)

if not cap.isOpened():
    raise IOError("Cannot open webcam")

if(UPLOAD):
    rmtree(PATH_PIC_PI) 
    mkdir(PATH_PIC_PI)

#hlavni smycka programu
while True:
    _, frameOrig = cap.read()
    if(type(frameOrig) == type(None)):
        pass
    else:	
        img_hsv, img_bw, frame_resized = cfu.prep_pic(frameOrig)
        mask_obj = cv.inRange(img_hsv, GREEN_HSV_RANGE[0], GREEN_HSV_RANGE[1])
        mask_line = cfu.crop_img_line_color(img_bw, selection)
       
        cv.rectangle(image_draw, (CENTER_X - CENTER_TOLERANCE, CENTER_Y - CENTER_TOLERANCE), (CENTER_X + CENTER_TOLERANCE, CENTER_Y + CENTER_TOLERANCE), (0, 0, 255), 2) 
        cv.line(image_draw, (0,int(SEEK_OBJECT * HEIGHT_OF_IMAGE-30)), (WIDTH_OF_IMAGE, int(SEEK_OBJECT * HEIGHT_OF_IMAGE-30)), (255,255,255), 3)
        cv.line(image_draw, (0,int(SEEK_OBJECT * HEIGHT_OF_IMAGE+30)), (WIDTH_OF_IMAGE, int(SEEK_OBJECT * HEIGHT_OF_IMAGE+30)), (255,255,255), 3)

    if(TRY_LINE == False):
        image_draw = frame_resized
        robot.stop()
        pass
    
    else:
        try:
            angle, image_draw = cfu.contours_line(frame_resized, mask_line)
            LINE_FOUND = True
            line_count += 1

        except Exception as e:
            LINE_FOUND = False
            servoX.setAngle(SERVOX_POS)
            servoY.setAngle(SERVOY_POS)

    if (LINE_FOUND == False  and TRY_LINE == True):
         if(line_count > 1):
             TRY_LINE = False
             search_seq(servoX, servoY, dire)
         sleep(0.5)
         servoX.setAngle(SERVOX_POS)
         servoY.setAngle(SERVOY_POS)

    try:
            contours, hierarchy = cv.findContours(mask_obj, cv.RETR_EXTERNAL ,cv.CHAIN_APPROX_NONE)
            contour = max(contours, key = cv.contourArea)
            x,y,w,h = cv.boundingRect(contour)
            M = cv.moments(contour)

            if(w > WIDTH_OF_IMAGE/8) and (h > HEIGHT_OF_IMAGE/8) and (cv.contourArea(contour) > area/150) :

                if(M["m10"] !=0 and M["m01"] !=0 and M["m00"] !=0):
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    color = (255, 0, 255)

                    if(cY>= SEEK_OBJECT * HEIGHT_OF_IMAGE-30 and cY<= SEEK_OBJECT * HEIGHT_OF_IMAGE+30):
                        color = (255, 255, 0)
                        OBJ_IN_LINE = True
                        curr_cont = (cX, cY)
                    else:
#                       OBJ_IN_LINE = False
                        PREV_OBJ_IN_LINE = False

                    cv.rectangle(image_draw, (x,y), (x+w,y+h), color, 5)
                    cv.putText(image_draw, str(f"{cX} {cY}"), (x, y-10), cv.FONT_HERSHEY_TRIPLEX, 0.5, (0, 0, 255))
            else:
                print("no obj in frame")
                SAVED_PIC = False
                OBJ_IN_LINE = False
                DO_AIM = True
                PREV_OBJ_IN_LINE = False
                CENTERED = False
                CENT_LAST = False
                MAY_STOP = True
    except Exception as e:
             contours = []

    if(OBJ_IN_LINE and not PREV_OBJ_IN_LINE and MAY_STOP):
        TRY_LINE = False
        PREV_OBJ_IN_LINE = True
        robot.stop()
        DO_DRIVE = False
        MAY_STOP = False

    if(OBJ_IN_LINE and DO_AIM):
        CENTERED, angleX, angleY = cfu.aim_camera_obj(servoX, servoY, cX, cY)

    if(CENTERED and not CENT_LAST):
                DO_AIM = False
                CENT_LAST = True
                timer = threading.Timer(2.0, save_picture)
                timer.start()

    _, dire = cfu.deviation(angle)
 
    #degree evaluation by PID controller
    dev = round(2*abs(pid(angle)))
    #driving decisions
    if(DO_DRIVE):
         if ((dev + BASE_PWM) > PWM_MAX):
                 if dire == 1:
                     robot.moveL(PWM_MIN)
                 elif dire == -1:
                     robot.moveR(PWM_MIN)
         else:
                 cfu.steer(BASE_PWM, dev, dire, robot)
     #show feed
    try:
        cv.imshow("orig", frameOrig)
        cv.imshow("draw", image_draw)
    except Exception as e:
        robot.stop()
        
    if cv.waitKey(1) == ord('q'):
        break
#reset everything once program ends
servoX.setAngle(SERVOX_POS)
servoY.setAngle(SERVOY_POS)
robot.stop()
cap.release()
cv.destroyAllWindows()
