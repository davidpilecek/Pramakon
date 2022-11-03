import numpy as np
import cv2 as cv
import config as conf
import camera_func as cfu

cap = cv.VideoCapture(0)

if not cap.isOpened():
    raise IOError("Cannot open webcam")

T = conf.threshold

frame_draw = []

kernel = np.ones((3,3),np.uint8)

angle = 0

ret = None

cX, cY = [0, 0]

while True:

    direction = 0

    _, frameOrig = cap.read()

    if(type(frameOrig) == type(None)):
        pass
    else:
        frame = cv.resize(frameOrig, (200, 200))
        height, width = frame.shape[:2]
        area = 200*200
        ret, T_final = cfu.balance_pic(frame, area, T)
 
    try:
       angle, image_draw = cfu.contours_calibrate(frame, ret, height, width)

    except Exception as e:    
        print("No contours")
         
          
    angle = round(angle)

    dev, way = cfu.deviance(angle)

    try:
        cv.imshow("main", image_draw_obj)
        print(size)
    except Exception as e:
        print(str(e))    

    if cv.waitKey(1) == ord('q'):
        break
cap.release()
cv.destroyAllWindows()

