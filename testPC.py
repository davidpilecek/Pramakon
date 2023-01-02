from time import sleep
import cv2 as cv
import numpy as np
import camera_func as cfu
from config import *

cap = cv.VideoCapture(1)

dire = 0
frame_draw = []
angle = 0
ret = None
cX, cY = [0, 0]
index = 0
res = True
selection = FRAME_SELECT
line_count = 0
image_draw = None
obj_in_line = False
prev_obj_in_line = False
last_cont = ()
curr_cont = ()
orig = False
centered = False
contour_ID = 0

if not cap.isOpened():
    raise IOError("Cannot open webcam")

while True:
    _, frameOrig = cap.read()
    image_draw = cv.resize(frameOrig, (HEIGHT_OF_IMAGE, WIDTH_OF_IMAGE))

    if(type(frameOrig) == type(None)):
        pass
    else:
        img_hsv, height, width = cfu.prep_pic(frameOrig)
        mask = cfu.crop_img_line_color(img_hsv, HEIGHT_OF_IMAGE, WIDTH_OF_IMAGE, BLUE_HSV_RANGE, FRAME_SELECT)
        contours, hierarchy = cv.findContours(mask, cv.RETR_TREE ,cv.CHAIN_APPROX_NONE)

    contour = max(contours, key = cv.contourArea, default=0)
    try:
        cv.drawContours(image_draw, [contour], -1, (0, 255, 0), -1)
        [vx,vy,x,y] = cv.fitLine(contour, cv.DIST_L2,0,0.01,0.01)
    
        lefty = int((-x*vy/vx) + y)
        righty = int(((height-x)*vy/vx)+y)

        vy = float(vy)
        vx = float(vx)

        cv.line(image_draw,(height-1,righty),(0,lefty),(0,255,255),5)

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

        cv.circle(image_draw, (cX, cY), 10, (0, 0, 0), -1)

        if cX > int(width / 2):
             x_pos = 180 - np.degrees(np.arctan((height - cY) / (cX - int(width / 2))))

        elif cX < int(width / 2):
             x_pos = np.degrees(np.arctan((height - cY) / (int(width / 2) - cX )))
        else:
            cX, cY = [0, 0]
            x_pos = 90

        average_angle = (ang_vector*0.35 + x_pos*0.65)

        average_angle = round(average_angle)

        cv.putText(image_draw, str(round(average_angle)),(50, 50), cv.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    except:
        print(f"noroad")
    height, width = image_draw.shape[:2]

    

    try:
        cv.imshow("main", frameOrig)
        cv.imshow("mask",image_draw)

    except Exception as e:
        print(str(e))
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()