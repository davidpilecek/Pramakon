import cv2 as cv
import numpy as np

import camera_func as cfu

cap = cv.VideoCapture(0)

if not cap.isOpened():
    raise IOError("Cannot open webcam")


while True:

    _, frame = cap.read()

    if(type(frame) == type(None) or _ == False):
        pass

    frameShow, height, width = cfu.prep_pic(frame)


    try:      
        cv.imshow("window", frameShow)
    except Exception as e:
        print(str(e))
       
        
    if cv.waitKey(1) == ord('q'):
        
        break

cap.release()
cv.destroyAllWindows()

