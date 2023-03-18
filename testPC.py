from time import sleep
from time import time
import cv2 as cv
import camera_func as cfu
from config import *
from shutil import rmtree
from os import mkdir
import threading
#capture webcam feed
cap = cv.VideoCapture(0)
#variables
dire = 0
angle = 0
ret = None
cX, cY = [0, 0]
index = 0
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
cent_y = False
cent_x = False
saved_pic = 0
last_time = 0
cent_last = False

if(UPLOAD):
    rmtree(PATH_PIC_PI) 
    mkdir(PATH_PIC_PI)

def save_picture():
    global saved_pic
    global current_time
    global index
    sleep(2)
    if(not saved_pic):
        print("saving pic")
        print(f"{cX}, {cY}")
        path, index = cfu.save_pic(index, frameOrig, PATH_PIC_PI)
        print(path) 
        saved_pic = 1

if not cap.isOpened():
    raise IOError("Cannot open webcam")

#main loop where most of the magic happens
while True:
    current_time = round(time())
    print(current_time)
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
                        prev_obj_in_line = False

                    cv.rectangle(image_draw, (x,y), (x+w,y+h), color, 5)
                    cv.putText(image_draw, string, (x, y-10), cv.FONT_HERSHEY_TRIPLEX, 0.5, (0, 0, 255))
            else:
                print("no obj in frame")
                cent_last = 0
    except Exception as e:
             contours = []
             #print(f"no object contour")
             
    if(obj_in_line == True and prev_obj_in_line == False):
        prev_obj_in_line = True
        
    if(obj_in_line):

        if((cX > CENTER_X + CENTER_TOLERANCE) or (cX < CENTER_X - CENTER_TOLERANCE)): 
            cent_x = False
            #print("not centx")
        else:
            cent_x = True
        if((cY > CENTER_Y + CENTER_TOLERANCE) and (cY < CENTER_Y - CENTER_TOLERANCE)):
            cent_y = False
            #print("not centy")
        else:
            cent_y = True
        if cent_x and cent_y:
            centered = True
            print("c")
        else:
            centered = False
            print("not c")
            
    if(centered and not cent_last):
        timer = threading.Timer(2.0, save_picture)
        timer.start()
        saved_pic = 0
        cent_last = 1
    #show feed
    try:
        #cv.imshow("orig", frameOrig)
        cv.imshow("draw", image_draw)
    except Exception as e:
        print(str(e))
        
    if cv.waitKey(1) == ord('q'):
        break
#reset everything once program ends

cap.release()
cv.destroyAllWindows()
