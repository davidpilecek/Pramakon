import numpy as np
import cv2 as cv
import config as conf

def crop_img(img, height, width):
    height_1 = int(height/conf.crop_section)
    
    vertices = [(0, height_1), (0, height),(width , height), (width, height_1)]
    vertices = np.array([vertices], np.int32)

    #create pure black frame size of image
    mask = np.zeros_like(img)

    match_mask_color = 255

    area = round((height - height_1) * width)

    #create pure white frame in area of interest
    cv.fillPoly(mask, vertices, match_mask_color)

    #return image with other area than AOI non-reactive to contour seeking algorithm
    masked_image = cv.bitwise_and(img, mask)
    
    return masked_image, area

def prep_pic(src):
    frame = cv.resize(src, (conf.height, conf.width))
    height, width = frame.shape[:2]

    grayImg = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    blurred = cv.GaussianBlur(grayImg, (9, 9), 0)

    return blurred, height, width
   
def balance_pic(image, area, T):
    ret = None
    direction = 0
    
    for i in range(0, conf.th_iterations):
        print(T)
        rc, gray = cv.threshold(image, T, 255, cv.THRESH_BINARY)

        if (np.all(gray == 0)):
            pass

        nwh = cv.countNonZero(gray)

        perc = int(100 * nwh / area)
        
        if perc > conf.white_max:
            if T >= conf.threshold_max:
                ret = gray
                break
            if direction == -1:
                ret = gray
                break
            T += 10
            direction = 1
        elif perc < conf.white_min:
            if T < conf.threshold_min:
                break
            if  direction == 1:
                ret = gray
                break

            T -= 10
            direction = -1
        else:
            ret = gray
            break
    return ret      

def deviance(ang):
    if ang == 90:
        return 0, 0
    elif ang > 90:
        dev = ang - 90
        #turn Right
        way = -1
    elif ang < 90:
        dev = 90 - ang
        #turn Left
        way = 1 
    return dev, way

def steer(basePwm, dev, way, robot):
    
    if way == 1:
        
        robot.moveBoth(basePwm - dev, basePwm + dev)
        #print("\n", "moving slightly left")
        #print("left: ", basePwm - dev)
        #print("right: ",basePwm + dev)
    elif way == -1:
        
        robot.moveBoth(basePwm + dev, basePwm - dev)
        #print("\n", "moving slightly right")
        #print("left: ", basePwm + dev)
        #print("right: ",basePwm - dev)
    else:
        #print("moving straight")
        robot.straight(basePwm)


def contours_line(frame, mask, height, width):

    image_draw = frame

    contours, hierarchy = cv.findContours(mask, cv.RETR_TREE ,cv.CHAIN_APPROX_NONE)

    contour = max(contours, key = cv.contourArea, default=0)

    cv.drawContours(image_draw, contour, -1, (0, 255, 0), 5)

    if len(contours)>0:
        M = cv.moments(contour)
        if(M["m10"] !=0 and M["m01"] !=0 and M["m00"] !=0):
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
    else:
        pass
    
    cv.circle(image_draw, (cX, cY), 10, (255, 255, 0), -1)

    if cX > int(width / 2):
            angle = 180 - np.degrees(np.arctan((height - cY) / (cX - int(width / 2))))

    elif cX < int(width / 2):
            angle = np.degrees(np.arctan((height - cY) / (int(width / 2) - cX )))
    else:
        cX, cY = [0, 0]
        angle = 90

    cv.putText(image_draw, str(round(angle)),(50, 50), cv.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    return angle, image_draw

def prep_pic_obj(src, color):
    frame = cv.resize(src, (500, 500))

    hsvImg = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    mask = cv.inRange(hsvImg, color[0], color[1])

    return mask

def detect_object():
    return
