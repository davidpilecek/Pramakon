from time import sleep
import cv2 as cv
import camera_func as cfu
from config import *
from drive import *
from simple_pid import PID
from shutil import rmtree
from os import mkdir
#create instance of PID controller
pid = PID(KP, KI, KD, setpoint = 90)
pid.output_limits = (-45, 45)
pid.sample_time = 0.01
#create objects of robot (motors) and servos
robot = Robot(LEFT_MOTOR_PIN, RIGHT_MOTOR_PIN)
servoX = Servo(X_SERVO_PIN)
servoY = Servo(Y_SERVO_PIN)
#capture webcam feed
cap = cv.VideoCapture(0)
#variables
dire = 0
angle = 0
ret = None
cX, cY = [0, 0]
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
#run in case driving track is lost
def search_seq(servoX, servoY, dire):
    robot.stop()
    global try_line
    global line_count
    line_count = 0
   
    servoY.setAngle(SERVOY_POS + 20)
    selection = FRAME_SELECT + 30
    if (dire == -1):
     
        servoX.setAngle(SERVOX_POS - 40)
    elif(dire == 1):
   
        servoX.setAngle(SERVOX_POS + 40)
    sleep(0.5)
    try_line = True

servoX.setAngle(SERVOX_POS)
servoY.setAngle(SERVOY_POS)

if not cap.isOpened():
    raise IOError("Cannot open webcam")

if(UPLOAD):
    rmtree(PATH_PIC_PI) 
    mkdir(PATH_PIC_PI)

#main loop where all of the magic happens
while True:
    _, frameOrig = cap.read()
    if(type(frameOrig) == type(None)):
        pass
    else:	
        img_hsv, img_bw, frame_resized = cfu.prep_pic(frameOrig)
        mask_obj = cv.inRange(img_hsv, GREEN_HSV_RANGE[0], GREEN_HSV_RANGE[1])
        mask_line = cfu.crop_img_line_color(img_bw, selection)

    if(try_line == False):
        image_draw = frame_resized
        robot.stop()
        pass
    
    else:
        try:
            angle, image_draw = cfu.contours_line(frame_resized, mask_line)
            line_found = True
            line_count += 1

        except Exception as e:
            line_found = False
            servoX.setAngle(SERVOX_POS)
            servoY.setAngle(SERVOY_POS)

    if (line_found == False  and try_line == True):
         if(line_count > 1):
             try_line = False
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
                    string = str(cX) + " " + str(cY)
                    color = (255, 0, 255)

                    if(cY>= SEEK_OBJECT * HEIGHT_OF_IMAGE-30 and cY<= SEEK_OBJECT * HEIGHT_OF_IMAGE+30):
                        color = (255, 255, 0)
                        obj_in_line = True
                        curr_cont = (cX, cY)
                                                    
                    else:
                        prev_obj_in_line = False

                    cv.rectangle(image_draw, (x,y), (x+w,y+h), color, 5)
                    cv.putText(image_draw, string, (x, y-10), cv.FONT_HERSHEY_TRIPLEX, 0.5, (0, 0, 255))

    except Exception as e:
             contours = []
             print(f"no object contour")

    if(obj_in_line == True and prev_obj_in_line == False):
        try_line = False
        prev_obj_in_line = True
        robot.stop()
        DO_DRIVE = False
        
    if(obj_in_line):
        centered, angleX, angleY = cfu.aim_camera_obj(servoX, servoY, cX, cY)

    if(centered):
                print("saving pic")
                robot.stop()
                servoX.setAngle(angleX)
                servoY.setAngle(angleY)
                sleep(0.5)
                path, index = cfu.save_pic(index, frameOrig, PATH_PIC_PI)
                print(path)
                sleep(0.5)    
                servoX.reset(servoX, SERVOX_POS) 
                servoY.reset(servoY, SERVOY_POS)
                robot.straight(40)
                sleep(0.2)
                DO_DRIVE = True                    
                obj_in_line = False
                centered = False
                try_line = True

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
    #drawing guidance stuff
    cv.rectangle(image_draw, (CENTER_X - CENTER_TOLERANCE, CENTER_Y - CENTER_TOLERANCE), (CENTER_X + CENTER_TOLERANCE, CENTER_Y + CENTER_TOLERANCE), (0, 0, 255), 2) 
    cv.line(image_draw, (0,int(SEEK_OBJECT * HEIGHT_OF_IMAGE-30)), (WIDTH_OF_IMAGE, int(SEEK_OBJECT * HEIGHT_OF_IMAGE-30)), (255,255,255), 3)
    cv.line(image_draw, (0,int(SEEK_OBJECT * HEIGHT_OF_IMAGE+30)), (WIDTH_OF_IMAGE, int(SEEK_OBJECT * HEIGHT_OF_IMAGE+30)), (255,255,255), 3)
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
