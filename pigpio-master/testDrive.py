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
servo_cent = False
servo_reset = False

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
    global robot
    #servo_centered = False
    robot.stop()
    selection = conf.frame_select
    while(servoX.getAngle() != conf.servoX_pos and servoY.getAngle() != conf.servoY_pos):
        if(servoX.getAngle() > conf.servoX_pos):
            sleep(0.01)
            servoX.setAngle(servoX.getAngle() - conf.step)
        if(servoX.getAngle() < conf.servoX_pos):
            sleep(0.01)
            servoX.setAngle(servoX.getAngle() + conf.step)
        if(servoY.getAngle() > conf.servoY_pos):
            sleep(0.01)
            servoY.setAngle(servoY.getAngle() - conf.step)
        if(servoY.getAngle() < conf.servoY_pos):
            sleep(0.01)
            servoY.setAngle(servoY.getAngle() + conf.step)
        
image_draw = None

if not cap.isOpened():
    raise IOError("Cannot open webcam")

servoX.setAngle(conf.servoX_pos)
servoY.setAngle(conf.servoY_pos)

while True:
    
    currAngleX = round(servoX.getAngle())
    currAngleY = round(servoY.getAngle())
    if(currAngleX == conf.servoX_pos and currAngleY == conf.servoY_pos):
        servo_cent = True
    else:
        servo_cent = False
    print(servo_cent)
    _, frameOrig = cap.read()

    if(type(frameOrig) == type(None)):
        pass
    else:
        blurred, height, width = cfu.prep_pic(frameOrig)
        ret, area = cfu.crop_img_line_color(blurred, height, width, conf.blue, selection)
        mask_obj = cfu.obj_mask(blurred, conf.green)
  
    if(try_line == False and servo_cent == False):
        image_draw = blurred
        robot.stop()
        pass
    
    else:
        try:
            angle, image_draw = cfu.contours_line(blurred, ret, height, width)
            line_found = True
            line_count += 1
        except Exception as e:
            line_found = False
            servoX.setAngle(conf.servoX_pos)
            servoY.setAngle(conf.servoY_pos)

            
    if (line_found == False  and try_line == True):
         try_line = False
         search_seq(servoX, servoY, dire)
         sleep(0.5)
         servoX.setAngle(conf.servoX_pos)
         servoY.setAngle(conf.servoY_pos)


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
                    
                    if(y>= 0.66 * conf.height-20 and y<= 0.66 * conf.height+20):
                        color = (255, 255, 0)
                        obj_in_line = True
                        curr_cont = (cX, cY)                           
                            
                    else:
                        prev_obj_in_line = False
                    cv.rectangle(image_draw, (x,y), (x+w,y+h), color, 5)
                    cv.putText(image_draw, string, (x, y-10), cv.FONT_HERSHEY_TRIPLEX, 0.5, (0, 0, 255) )

    except Exception as e:
        print("cannot find object")

    if(obj_in_line == True and prev_obj_in_line == False and servo_cent == True):
        
        #robot.stop()
        orig = cfu.check_orig(curr_cont, last_cont)
        prev_obj_in_line = True


    if(orig):
        print(" ")
        print("last object: " + str(last_cont))
        print("current object: " + str(curr_cont))
        try_line = False
        robot.stop()        
        if(save_last):
            last_cont = (cX, cY)
            save_last = False
            print("saved current cont")
        centered, angleX, angleY = cfu.aim_camera_obj(servoX, servoY, cX, cY, currAngleX, currAngleY)
        
    if (centered and orig):
                print("saving pic")
                robot.stop()
                servoX.setAngle(angleX)
                servoY.setAngle(angleY)
                sleep(0.2)
                path, index = cfu.save_pic(index, frameOrig, conf.path_pic_Pi)
                print(path)
                sleep(0.2)                               
                servoX.setAngle(conf.servoX_pos)
                servoY.setAngle(conf.servoY_pos)
                sleep(1)
                obj_in_line = False
                centered = False
                orig = False
                save_last = True            

    dev, dire = cfu.deviance(angle)
    if(servo_cent):
        if ((dev + conf.basePwm) > conf.pwmMax):
            if dire == 1:
                robot.moveL(conf.basePwm)
            elif dire == -1:
                robot.moveR(conf.basePwm)
        else:
            cfu.steer(conf.basePwm, dev, dire, robot)
    
    cv.rectangle(image_draw, (conf.centerX - conf.tol, conf.centerY - conf.tol), (conf.centerX + conf.tol, conf.centerY + conf.tol), (0, 0, 255), 2) 
    cv.line(image_draw, (0,int(0.66 * conf.height-20)), (conf.width, int(0.66 * conf.height-20)), (255,255,255), 3)
    cv.line(image_draw, (0,int(0.66 * conf.height+20)), (conf.width, int(0.66 * conf.height+20)), (255,255,255), 3)

    
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
