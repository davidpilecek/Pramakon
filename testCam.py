import numpy as np
import cv2 as cv
import time
import camera_func as cfu
from config import *

height = 250
width = 250

cap = cv.VideoCapture(0)

if not cap.isOpened():
    raise IOError("Cannot open webcam")

while True:
    _, frame_orig = cap.read()
    if(type(frame_orig) == type(None) or _ == False):
        pass

    try:
        cv.imshow("frame", frame_orig)
      
    except Exception as e:
        print(str(e))

    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()

