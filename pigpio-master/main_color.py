#find object of specific color, get as close to it as possible and take picture of it, then aim back on the white track and drive along
#do NOT get off the white track, once you have to turn the camera 90 degrees to the left or right, that means it's as close
#as possible and therefore you can take a pic of it.

#create line to center of contour of red object, once it reaches 0 or 180 with regard to the center of the screen, then turn the camera 
#to it so that the entire object is in the center of the frame and snap it


from time import sleep

import cv2 as cv
import numpy as np

import camera_func as cfu
import config as conf

cap = cv.VideoCapture(0)

if not cap.isOpened():
    raise IOError("Cannot open webcam")

T = conf.threshold

frame_draw = []

angle = 0

ret = None

cX, cY = [0, 0]

index = 0

while True:

    direction = 0

    _, frameOrig = cap.read()

    if(type(frameOrig) == type(None)):
        pass
    else:
        blurred, height, width = cfu.prep_pic(frameOrig)

        ret, area = cfu.crop_img_line_color(blurred, height, width, conf.blue)
 
    try:
        angle, image_draw = cfu.contours_line(frameOrig, ret, height, width)

    except Exception as e:
         print("No contours")
         sleep(1)
    angle = round(angle)

    dev, way = cfu.deviance(angle)

    try:
        cv.imshow("main", image_draw)
        cv.imshow("orig", blurred)
    except Exception as e:
        print(str(e))    

    if cv.waitKey(1) == ord('q'):
        break
cap.release()
cv.destroyAllWindows()
