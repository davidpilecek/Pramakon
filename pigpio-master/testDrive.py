from time import sleep
import cv2 as cv
import numpy as np
import camera_func as cfu
import config as conf
import drive as dr

robot = dr.Robot(conf.leftMot, conf.rightMot)
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
try_line = True
selection = conf.frame_select
line_found = True
line_count = 0
obj_in_line = False
prev_obj_in_line = False
centered = False
last_cont = ()
curr_cont = ()
orig = False
save_last = True
angleX = 0
angleY = 0


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
    currAngleX = servoX.getAngle()
    currAngleY = servoY.getAngle()
    _, frameOrig = cap.read()

    if(type(frameOrig) == type(None)):
        pass
    else:
        blurred, height, width = cfu.prep_pic(frameOrig)
        ret, area = cfu.crop_img_line_color(blurred, height, width, conf.blue, selection)
        mask_obj = cfu.obj_mask(blurred, conf.green)
  
    if(try_line == False):
        pass
    else:
        try:
            angle, image_draw = cfu.contours_line(blurred, ret, height, width)
            line_found = True
            line_count += 1
        except Exception as e:
            line_found = False
            res_servo(servoX, servoY)
    if (line_found == False  and try_line == True):
         try_line = False
         search_seq(servoX, servoY, dire)
         sleep(0.3)
         res_servo(servoX, servoY)

    try:
        contours, hierarchy = cv.findContours(mask_obj, cv.RETR_EXTERNAL ,cv.CHAIN_APPROX_NONE)

        for contour in contours:
            M = cv.moments(contour)
            if(M["m10"] !=0 and M["m01"] !=0 and M["m00"] !=0):
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                string = str(cX) + " " + str(cY)
                x,y,w,h = cv.boundingRect(contour)
                if(w > conf.width/20) and (h > conf.height/20):
                    color = (255, 0, 255)
                    obj_in_line = False
                    
                    if(y>= 0.66 * conf.height-10 and y<= 0.66 * conf.height+10):
                        color = (255, 255, 0)
                        obj_in_line = True
                        curr_cont = (cX, cY)                           
                            
                    else:
                        prev_obj_in_line = False
                    cv.rectangle(image_draw, (x,y), (x+w,y+h), color, 5)
                    cv.putText(image_draw, string, (x, y-10), cv.FONT_HERSHEY_TRIPLEX, 0.5, (0, 0, 255) )

    except Exception as e:
        print("cannot find object")

    if(obj_in_line == True and prev_obj_in_line == False):
        robot.stop()
        orig = cfu.check_orig(curr_cont, last_cont)
        prev_obj_in_line = True
        print("in line")
        print(last_cont)
        print(curr_cont)
    
    if(orig):
        #print("orig, centering")
        if(save_last):
            last_cont = (cX, cY)
            save_last = False
            print("saved last cont")
        centered, angleX, angleY = cfu.aim_camera_obj(servoX, servoY, cX, cY, currAngleX, currAngleY)
    if (centered and orig):
                servoX.setAngle(angleX)
                servoY.setAngle(angleY)
                sleep(0.5)
                path, index = cfu.save_pic(index, frameOrig, conf.path_pic_Pi)
                print(path)                    
                res_servo(servoX, servoY)
                obj_in_line = False
                centered = False
                orig = False
                save_last = True

    dev, dire = cfu.deviance(angle)

    if dev + conf.basePwm > conf.pwmMax:
        if dire == 1:
            robot.moveL(conf.basePwm)
        elif dire == -1:
            robot.moveR(conf.basePwm)
    else:
            cfu.steer(conf.basePwm, dev, dire, robot)
    
    cv.rectangle(image_draw, (conf.centerX - conf.tol, conf.centerY - conf.tol), (conf.centerX + conf.tol, conf.centerY + conf.tol), (0, 0, 255), 2) 
    try:

        cv.imshow("main", image_draw)
    except Exception as e:
        robot.stop()
    if cv.waitKey(1) == ord('q'):
        break

res_servo(servoX, servoY)
robot.stop()
cap.release()
cv.destroyAllWindows()
