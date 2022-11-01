import numpy as np
import cv2 as cv
import config as conf
import camera_func as cfu
#import drive as dr

#robot = dr.Robot(conf.leftMot, conf.rightMot)

cap = cv.VideoCapture(conf.path)

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
        #robot.stop()
        print("No contours")
    angle = round(angle)
    print(angle)

    dev, dir = cfu.deviance(angle)

    if dev + conf.basePwm > conf.pwmMax:
        if dir == 1:
            print("moving sharp left")
            #robot.moveL(conf.basePwm)
        elif dir == -1:
            print("moving sharp right")
            #robot.moveR(conf.basePwm)
    else:
        cfu.steer(conf.basePwm, dev, dir, None)
        
    cv.imshow("window", image_draw)

    if cv.waitKey(1) == ord('q'):
        #robot.stop()
        break

cap.release()
cv.destroyAllWindows()