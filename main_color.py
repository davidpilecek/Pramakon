from time import sleep
import cv2 as cv
import numpy as np
import camera_func as cfu
import config as conf
import drive as dr
from simple_pid import PID
import matplotlib.pyplot as plt

pid = PID(conf.p, conf.i, conf.d, setpoint = 90)
pid.output_limits = (-45, 45)
pid.sample_time = 0.01

#angles_graph = []
#devs_graph = []

robot = dr.Robot(conf.leftMot, conf.rightMot)
servoX = dr.Servo(conf.servoPinX)
servoY = dr.Servo(conf.servoPinY)

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
curr_time = 0

def search_seq(servoX, servoY, dire):
    robot.stop()
    global try_line
    global line_count
    line_count = 0
    print("setting servos")
    servoY.setAngle(conf.servoY_pos + 20)
    selection = conf.frame_select + 30
    if (dire == -1):
        print("looking right")
        servoX.setAngle(conf.servoX_pos - 40)
    elif(dire == 1):
        print("looking left")
        servoX.setAngle(conf.servoX_pos + 40)
    sleep(0.5)
    try_line = True

def res_servo(servoX, servoY):
    global selection
    global robot
    currX = round(servoX.getAngle())
    currY = round(servoY.getAngle())
    robot.stop()
    selection = conf.frame_select

    if(currX > conf.servoX_pos):
        for j in range(currX-conf.servoX_pos):
            servoX.setAngle(currX - j)
            sleep(0.02)
    else:
        for i in range(abs(currX-conf.servoX_pos)):
            servoX.setAngle(currX + i)
            sleep(0.02)
            
    if(currY > conf.servoY_pos):
        for j in range(currY-conf.servoY_pos):
            servoY.setAngle(currY - j)
            sleep(0.02)
    else:
        for i in range(abs(currY-conf.servoY_pos)):
            servoY.setAngle(currY + i)
            sleep(0.02)

image_draw = None

if not cap.isOpened():
    raise IOError("Cannot open webcam")

servoX.setAngle(conf.servoX_pos)
servoY.setAngle(conf.servoY_pos)

while True:
    
    currAngleX = round(servoX.getAngle())
    currAngleY = round(servoY.getAngle())

    _, frameOrig = cap.read()
    
    p, i, d = pid.components
    
    if(type(frameOrig) == type(None)):
        pass
    else:
        blurred, height, width = cfu.prep_pic(frameOrig)
        ret, area = cfu.crop_img_line_color(blurred, height, width, conf.blue, selection)
        mask_obj = cfu.obj_mask(blurred, conf.green)
  
    if(try_line == False):
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
         if(line_count > 1):
             try_line = False
             search_seq(servoX, servoY, dire)
         sleep(0.5)
         servoX.setAngle(conf.servoX_pos)
         servoY.setAngle(conf.servoY_pos)
<<<<<<< HEAD

=======
>>>>>>> 476e45d73054d92e089dd017875829bad7c28f86

    try:
        contours, hierarchy = cv.findContours(mask_obj, cv.RETR_EXTERNAL ,cv.CHAIN_APPROX_NONE)

        for contour in contours:
            x,y,w,h = cv.boundingRect(contour)
            M = cv.moments(contour)
            if(w > conf.width/10) and (h > conf.height/10):
                if(M["m10"] !=0 and M["m01"] !=0 and M["m00"] !=0):
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    string = str(cX) + " " + str(cY)
                    color = (255, 0, 255)
                    obj_in_line = False
                    if(cY>= conf.seek_line * conf.height-20 and cY<= conf.seek_line * conf.height+20):
                        color = (255, 255, 0)
                        obj_in_line = True
                        curr_cont = (cX, cY)                           
                            
                    else:
                        prev_obj_in_line = False
                    cv.rectangle(image_draw, (x,y), (x+w,y+h), color, 5)
                    cv.putText(image_draw, string, (x, y-10), cv.FONT_HERSHEY_TRIPLEX, 0.5, (0, 0, 255) )

<<<<<<< HEAD
    except Exception as e:
        res_servo(servoX, servoY)
        print("cannot find object")
        obj_in_line = False
        orig = False
        centered = False
        try_line = True

    if len(contours) == 0:
        res_servo(servoX, servoY)
        obj_in_line = False
        orig = False
        centered = False
        try_line = True

    if(obj_in_line == True and prev_obj_in_line == False):
        print("in line")
        orig = cfu.check_orig(curr_cont, last_cont)
        prev_obj_in_line = True

    if(orig):
        robot.stop()

=======
    try:
        contours, hierarchy = cv.findContours(mask_obj, cv.RETR_EXTERNAL ,cv.CHAIN_APPROX_NONE)

        for contour in contours:
            x,y,w,h = cv.boundingRect(contour)
            M = cv.moments(contour)
            if(w > conf.width/10) and (h > conf.height/10):
                if(M["m10"] !=0 and M["m01"] !=0 and M["m00"] !=0):
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    string = str(cX) + " " + str(cY)
                    color = (255, 0, 255)
                    obj_in_line = False
                    if(cY>= conf.seek_line * conf.height-20 and cY<= conf.seek_line * conf.height+20):
                        color = (255, 255, 0)
                        obj_in_line = True
                        curr_cont = (cX, cY)                           
                            
                    else:
                        prev_obj_in_line = False
                    cv.rectangle(image_draw, (x,y), (x+w,y+h), color, 5)
                    cv.putText(image_draw, string, (x, y-10), cv.FONT_HERSHEY_TRIPLEX, 0.5, (0, 0, 255) )

    except Exception as e:
        res_servo(servoX, servoY)
        print("cannot find object")

    if(obj_in_line == True and prev_obj_in_line == False):
        print("in line")
        orig = cfu.check_orig(curr_cont, last_cont)
        prev_obj_in_line = True

    if(orig):
        robot.stop()
        
>>>>>>> 476e45d73054d92e089dd017875829bad7c28f86
        if(save_last):
            print(" ")
            print("last object: " + str(last_cont))
            print("current object: " + str(curr_cont))
            last_cont = (cX, cY)
            save_last = False
            print("saved current cont")
        centered, angleX, angleY = cfu.aim_camera_obj(servoX, servoY, cX, cY)
        
    if (centered):
                try_line = False
                print("saving pic")
                robot.stop()
                servoX.setAngle(angleX)
                servoY.setAngle(angleY)
                sleep(0.5)
                path, index = cfu.save_pic(index, frameOrig, conf.path_pic_Pi)
                print(path)
                sleep(0.5)                               
                res_servo(servoX, servoY)
                obj_in_line = False
                centered = False
                orig = False
                save_last = True
                try_line = True

    angle_pid, dire = cfu.deviance(angle)
    
    
    #dev = angle_pid
    dev = round(2*abs(pid(angle)))
    
    #print("dev: " + str(dev))
    #print("angle: " + str(angle))
    #print("p: " + str(p))
    #print("i: " + str(i))
    #print("d: " + str(d))
    #print("      ")
    
    #angles_graph.append(angle)
    #devs_graph.append(dev)
    
    if ((dev + conf.basePwm) > conf.pwmMax):
            if dire == 1:
                robot.moveL(conf.pwmMin)
            elif dire == -1:
                robot.moveR(conf.pwmMin)
    else:
            cfu.steer(conf.basePwm, dev, dire, robot)
    
    cv.rectangle(image_draw, (conf.centerX - conf.tol, conf.centerY - conf.tol), (conf.centerX + conf.tol, conf.centerY + conf.tol), (0, 0, 255), 2) 
    cv.line(image_draw, (0,int(conf.seek_line * conf.height-20)), (conf.width, int(conf.seek_line * conf.height-20)), (255,255,255), 3)
    cv.line(image_draw, (0,int(conf.seek_line * conf.height+20)), (conf.width, int(conf.seek_line * conf.height+20)), (255,255,255), 3)

    try:
        cv.imshow("main", image_draw)
        #cv.imshow("original", frameOrig)
    except Exception as e:
        robot.stop()
    if cv.waitKey(1) == ord('q'):
        break

servoX = dr.Servo(conf.servoPinX)
servoY = dr.Servo(conf.servoPinY)
robot.stop()
cap.release()
cv.destroyAllWindows()
#plt.plot(angles_graph, label = "angles")
#plt.plot(devs_graph, label = "deviations")
#plt.legend()
<<<<<<< HEAD
#plt.show()
=======
#plt.show()
>>>>>>> 476e45d73054d92e089dd017875829bad7c28f86