import numpy as np
import cv2 as cv
import config as conf
import camera_func as cfu
import drive as dr
from time import sleep


robot = dr.Robot(conf.leftMot, conf.rightMot)

T = conf.threshold

frame_draw = []

kernel = np.ones((3,3),np.uint8)

angle = 0

ret = None

cX, cY = [0, 0]

cap = cv.VideoCapture(0)

sleep(2)

if not cap.isOpened():
    raise IOError("Cannot open webcam")

while True:

    direction = 0

    _, frame = cap.read()

    if(type(frame) == type(None) or _ == False):
        pass
    else:
        mask = cfu.prep_pic_obj(frame, conf.blue)
        height, width, blurred = cfu.prep_pic(frame)
        crop, area = cfu.crop_img(blurred, height, width)
        ret = cfu.balance_pic(crop, area, T)

    mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
    contours, hierarchy= cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    contour = max(contours, key = cv.contourArea, default = 0)

    try:
        angle, image_draw = cfu.contours_line(blurred, ret, height, width)
        frame_draw = cv.drawContours(cv.cvtColor(mask, cv.COLOR_GRAY2BGR), contour, -1, [0, 0, 255], 5)     





    except Exception as e:
        robot.stop()
        print("No contours")
    angle = round(angle)
    print(angle)

    if(angle <= conf.r_max and angle>= conf.l_max):
        robot.move(conf.pwm)
    elif(angle > conf.r_max):
        robot.moveL(conf.pwm)
    elif(angle < conf.l_max):
        robot.moveR(conf.pwm)

    if cv.waitKey(1) == ord('q'):
        robot.stop()
        break

cap.release()
cv.destroyAllWindows()