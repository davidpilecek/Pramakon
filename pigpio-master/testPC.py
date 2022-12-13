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

    if(type(frameOrig) == type(None)):
        pass
    else:
        blurred, height, width = cfu.prep_pic(frameOrig)
        ret, area = cfu.crop_img_line_color(blurred, height, width, conf.blue, selection)
        mask_obj = cfu.obj_mask(blurred, conf.green)
  
    try:
        angle, image_draw = cfu.contours_line(blurred, ret, height, width)
    except Exception as e:
        print("noline")
        
    try:
        #obj_angle, img_draw, obj_x, obj_y = cfu.contours_obj(image_draw, mask_obj)
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
                    obj_in_line = False
                    
                    if(y>= 0.66 * conf.height-5 and y<= 0.66 * conf.height+5):
                        color = (255, 255, 0)
                        obj_in_line = True
                    else:
                        prev_obj_in_line = False
                    cv.rectangle(image_draw, (x,y), (x+w,y+h), color, 5)
                    cv.putText(image_draw, string, (x, y-10), cv.FONT_HERSHEY_TRIPLEX, 0.5, (0, 0, 255) )

    except Exception as e:
        print("cannot find object")

    if(obj_in_line == True and prev_obj_in_line == False):
       prev_obj_in_line = True
       path, index = cfu.save_pic(index, frameOrig)
       print(path)
       
    try:
        cv.imshow("main", image_draw)
        cv.imshow("mask", mask_obj)
    except Exception as e:
        print(str(e))
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()