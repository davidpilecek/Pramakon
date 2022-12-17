from time import sleep
import time
import cv2 as cv
import numpy as np
import camera_func as cfu
import config as conf

cap = cv.VideoCapture(0)

dire = 0
frame_draw = []
angle = 0
ret = None
cX, cY = [0, 0]
index = 0
res = True
selection = conf.frame_select
line_count = 0
image_draw = None
obj_in_line = False
prev_obj_in_line = False
last_cont = ()
curr_cont = ()
orig = False
center = False

def contours_obj(img_draw, mask):

    contours, hierarchy = cv.findContours(mask, cv.RETR_EXTERNAL ,cv.CHAIN_APPROX_NONE)

    for contour in contours:
        x,y,w,h = cv.boundingRect(contour)
        if(w > conf.width/15) and (h > conf.height/15):
            cv.rectangle(img_draw, (x,y), (x+w,y+h), (0,0,255), 5)
    
    for contour in contours:
        M = cv.moments(contour)
        if(M["m10"] !=0 and M["m01"] !=0 and M["m00"] !=0):
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            string = str(cX) + " " + str(cY)
            cv.putText(img_draw, string, (cX, cY), cv.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 255) )
    
    return img_draw, cX, cY

if not cap.isOpened():
    raise IOError("Cannot open webcam")

while True:
    _, frameOrig = cap.read()
    print(orig)
    if(type(frameOrig) == type(None)):
        pass
    else:
        blurred, height, width = cfu.prep_pic(frameOrig)
        ret, area = cfu.crop_img_line_color(blurred, height, width, conf.blue, selection)
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
                if(w > conf.width/20) and (h > conf.height/20):
                    color = (255, 0, 255)
                    obj_in_line = False
                    
                    if(y>= 0.66 * conf.height-5 and y<= 0.66 * conf.height+5):
                        color = (255, 255, 0)
                        obj_in_line = True
                        curr_cont = (cX, cY) 
                    else:
                        prev_obj_in_line = False
                    cv.rectangle(blurred, (x,y), (x+w,y+h), color, 5)
                    cv.putText(blurred, string, (x, y-10), cv.FONT_HERSHEY_TRIPLEX, 0.5, (0, 0, 255) )

    except Exception as e:
        print("cannot find object")
    
    if(obj_in_line == True and prev_obj_in_line == False):
        orig = cfu.check_orig(curr_cont, last_cont)
        print("in line")
        prev_obj_in_line = True
        center = True
        if(orig):
            print("orig, centering")
            last_cont = (cX, cY)
    if(center and orig and (cX < conf.centerX + conf.tol) and (cX>conf.centerX-conf.tol) and (cY < conf.centerY + conf.tol) and (cY>conf.centerY-conf.tol)):
            path, index = cfu.save_pic(index, frameOrig, r"C:\Users\david\Desktop\cvPics\img")
            print(path)    

    cv.rectangle(blurred, (conf.centerX - conf.tol, conf.centerY - conf.tol), (conf.centerX + conf.tol, conf.centerY + conf.tol), (0, 0, 255), 2)
    try:
        cv.imshow("main", blurred)
        cv.imshow("mask", mask_obj)
    except Exception as e:
        print(str(e))
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()