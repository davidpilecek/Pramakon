import cv2 as cv
import numpy as np
from config import *
from time import sleep
from subprocess import run as srun
import os

def upload_pics_to_drive(dir_name = "/home/pi/Documents/Pramakon/unclassified_pics/", dir_id = "1PxzpWymlOXXaXND_W88hRYUJkKNvxSS2"):
    command = "./gdrive list -q \"'1PxzpWymlOXXaXND_W88hRYUJkKNvxSS2' in parents\" --no-header --max 0| cut -d\" \" -f1 - | xargs -L 1 ./gdrive delete -r"
    srun(command,shell=True)

    _, _, files = next(os.walk(dir_name))
    num_of_pics = len(files)

    for index in range(0, num_of_pics):
        result = srun(["./gdrive", "upload", f"{dir_name}img{index}.jpg", "-p", dir_id])

    return result.returncode

if __name__ == "__main__":
    upload_pics_to_drive()

def check_orig(curr_cont, last_cont):
    cX, cY = curr_cont[:2]
    if(last_cont == ()): return True
    elif(cX <= last_cont[0] + 50 and  cX >= last_cont[0] - 50 and  cY <= last_cont[1] + 50 and cY >= last_cont[1] - 50):
        return False
    else: return True

def contours_line(frame_resized, mask):
    image_draw = frame_resized
    contours, hierarchy = cv.findContours(mask, cv.RETR_TREE ,cv.CHAIN_APPROX_NONE)

    contour = max(contours, key = cv.contourArea, default=0)

    cv.drawContours(image_draw, [contour], -1, (0, 255, 0), -1)

    [vx,vy,x,y] = cv.fitLine(contour, cv.DIST_L2,0,0.01,0.01)
    
    lefty = int((-x*vy/vx) + y)
    righty = int(((HEIGHT_OF_IMAGE-x)*vy/vx)+y)

    vy = float(vy)
    vx = float(vx)

    cv.line(image_draw,(HEIGHT_OF_IMAGE-1,righty),(0,lefty),(0,255,255),5)

    if 0<vy<1:
        ang_vector = np.degrees(np.arctan(vy/vx))

    elif -1<vy<0:
        ang_vector = 180 - np.degrees(np.arctan(np.abs(vy)/vx))

    else:
        ang_vector = 90

    if len(contours)>0:
        M = cv.moments(contour)
        if(M["m10"] !=0 and M["m01"] !=0 and M["m00"] !=0):
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
    else:
        pass

    cv.circle(image_draw, (cX, cY), 10, (255, 255, 0), -1)

    if cX > int(WIDTH_OF_IMAGE / 2):
             x_pos = 180 - np.degrees(np.arctan((HEIGHT_OF_IMAGE - cY) / (cX - int(WIDTH_OF_IMAGE / 2))))

    elif cX < int(WIDTH_OF_IMAGE / 2):
             x_pos = np.degrees(np.arctan((HEIGHT_OF_IMAGE - cY) / (int(WIDTH_OF_IMAGE / 2) - cX )))
    else:
         cX, cY = [0, 0]
         x_pos = 90

    average_angle = (ang_vector*0.35 + x_pos*0.65)

    average_angle = round(average_angle)

    cv.putText(image_draw, str(round(average_angle)),(50, 50), cv.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    return average_angle, image_draw

def crop_img_line_color(img, sel, mask_obj):

    mask = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 91, 20)

    #mask_del = cv.bitwise_xor(mask, mask_obj)

    crop_selection = 100/(100 - 60)

    height_1 = HEIGHT_OF_IMAGE/crop_selection

    vertices = [(0, height_1), (0, HEIGHT_OF_IMAGE),(WIDTH_OF_IMAGE, HEIGHT_OF_IMAGE), (WIDTH_OF_IMAGE, height_1)]
    vertices = np.array([vertices], np.int32)

    #create pure black frame size of image
    mask_black = np.zeros_like(mask)
    
    match_mask_color = [255, 255, 255]

    cv.fillPoly(mask_black, vertices, match_mask_color)

    masked_image = cv.bitwise_and(mask, mask_black)
    return masked_image

def prep_pic(src):
    frame = cv.resize(src, (HEIGHT_OF_IMAGE, WIDTH_OF_IMAGE))

    blurred = cv.GaussianBlur(frame, (7, 7), 0)

    blurred_hsv = cv.cvtColor(blurred, cv.COLOR_BGR2HSV)

    blurred_bw = cv.cvtColor(blurred, cv.COLOR_BGR2GRAY)

    return blurred_hsv,blurred_bw, frame

def deviation(ang):
    if ang == 90:
        return 0, 0
    elif ang > 90:
        dev = ang - 90
        #turn Right
        way = -1
    elif ang < 90:
        dev = 90 - ang
        #turn Left
        way = 1
    return dev, way

def steer(basePwm, dev, way, robot):

    if way == 1:
        #print("moving slightly left")
        robot.moveBoth(basePwm - dev, basePwm + dev)

    elif way == -1:
        #print("moving slightly right")
        robot.moveBoth(basePwm + dev, basePwm - dev)
    else:
        #print("moving straight")
        robot.straight(basePwm)
    return way

def save_pic(index, image, path_pic):
    """Alway use original image as argument"""

    path = path_pic + str(index) + r".jpg"
   
    cv.imwrite(path, image)

    index += 1    

    return path, index

def contours_obj(img_draw, mask):

    cX, cY = [0, 0]
    contours, hierarchy = cv.findContours(mask, cv.RETR_EXTERNAL ,cv.CHAIN_APPROX_NONE)

    for contour in contours:
        x,y,w,h = cv.boundingRect(contour)
        if(w > WIDTH_OF_IMAGE/20) and (h > HEIGHT_OF_IMAGE/20):
            cv.rectangle(img_draw, (x,y), (x+w,y+h), (0,0,255), 5)

    if len(contours)>0:
        M = cv.moments(contour)
        if(M["m10"] !=0 and M["m01"] !=0 and M["m00"] !=0):
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
    else:
        pass
    cv.circle(img_draw, (cX, cY), 5, (255, 0, 255), -1)
    if cX > int(WIDTH_OF_IMAGE / 2):
             obj_angle = 180 - np.degrees(np.arctan((HEIGHT_OF_IMAGE - cY) / (cX - int(WIDTH_OF_IMAGE / 2))))

    elif cX < int(WIDTH_OF_IMAGE / 2):
             obj_angle = np.degrees(np.arctan((HEIGHT_OF_IMAGE - cY) / (int(WIDTH_OF_IMAGE / 2) - cX )))
    else:
         cX, cY = [0, 0]
         obj_angle = 90

    obj_angle = round(obj_angle)

    return obj_angle, img_draw, cX, cY

def aim_camera_obj(servoX, servoY, obj_x, obj_y):
    currAngleX = servoX.getAngle()
    currAngleY = servoY.getAngle()
    print("aiming")
    sleep(0.1)
    cent_x = False
    cent_y = False
    if(obj_x > CENTER_X + CENTER_TOLERANCE):
          servoX.setAngle(currAngleX - SERVO_STEP)
          cent_x = False
    elif(obj_x < CENTER_X - CENTER_TOLERANCE):
          servoX.setAngle(currAngleX + SERVO_STEP)
          cent_x = False
    else:
        cent_x = True
        
    if(obj_y > CENTER_Y + CENTER_TOLERANCE):
          servoY.setAngle(currAngleY - SERVO_STEP)
          cent_y = False
    elif(obj_y < CENTER_Y - CENTER_TOLERANCE):
          servoY.setAngle(currAngleY + SERVO_STEP)
          cent_y = False
    else:
        cent_y = True
       
    if(cent_x and cent_y):
        servoX.stopServo()
        servoY.stopServo()
        return True, currAngleX, currAngleY
        print("aimed")
    else:
        return False, currAngleX, currAngleY
        print("not aimed")

def crop_img_obj(img, w, h):

    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    #left column
    vertices_lc = [(0, 0.66*h), (0, h), (0.1*w, h), (0.1*w, 0.66*h)]
    vertices_lc = np.array([vertices_lc], np.int32)

    #right column
    vertices_rc = [(0.9*w, 0.66*h), (0.9*w, h), (w, h), (w, 0.66*h)]
    vertices_rc = np.array([vertices_rc], np.int32)

    #middle lower layer
    vertices_ll = [(0.1*w, 0.9*h), (0.1*w, h), (0.9*w, h), (0.9*w, 0.9*h)]
    vertices_ll = np.array([vertices_ll], np.int32)

    #create pure black frame size of image
    mask = np.zeros_like(img)

    match_mask_color = 255

    #create pure white frame in area of interest
    cv.fillPoly(mask, vertices_lc, match_mask_color)
    cv.fillPoly(mask, vertices_ll, match_mask_color)
    cv.fillPoly(mask, vertices_rc, match_mask_color)

    #return image with other area than AOI non-reactive to contour seeking algorithm
    masked_image = cv.bitwise_and(img, mask)

    return masked_image
