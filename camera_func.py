import numpy as np
import cv2 as cv
import config as conf

def crop_img_line(img, height, width):

    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    height_1 = height/conf.crop_selection

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
    frame = cv.resize(src, (200, 200))
    height, width = frame.shape[:2]

    blurred = cv.GaussianBlur(frame, (15, 15), 0)

    return blurred, height, width

def balance_pic(image, area, T):
    ret = None
    direction = 0

    for i in range(0, conf.th_iterations):
        
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
            T += conf.increment
            direction = 1
        elif perc < conf.white_min:
            if T < conf.threshold_min:
                break
            if  direction == 1:
                ret = gray
                break

            T -= conf.increment
            direction = -1
        else:
            ret = gray
            break
    return ret, T

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
        #print("moving slightly left")
        robot.moveBoth(basePwm - dev, basePwm + dev)

    elif way == -1:
        #print("moving slightly right")
        robot.moveBoth(basePwm + dev, basePwm - dev)
    else:
        #print("moving straight")
        robot.straight(basePwm)

def contours_line(frameOrig, mask, height, width):

    image_draw = cv.resize(frameOrig, [200, 200])

    contours, hierarchy = cv.findContours(mask, cv.RETR_TREE ,cv.CHAIN_APPROX_NONE)

    contour = max(contours, key = cv.contourArea, default=0)

    cv.drawContours(image_draw, contour, -1, (0, 255, 0), 5)

    height, width = image_draw.shape[:2]

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

    cv.circle(image_draw, (cX, cY), 10, (255, 255, 0), -1)

    if cX > int(width / 2):
             angle = 180 - np.degrees(np.arctan((height - cY) / (cX - int(width / 2))))

    elif cX < int(width / 2):
             angle = np.degrees(np.arctan((height - cY) / (int(width / 2) - cX )))
    else:
         cX, cY = [0, 0]
         angle = 90

    
    average_angle = (ang_vector*1/3 + angle*2/3)

    cv.putText(image_draw, str(round(average_angle)),(50, 50), cv.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    return average_angle, image_draw


def save_pic(index, image):

    
    path = r"C:\Users\David\Pictures\opencv\testpic" + str(index) + r".jpg"
    cv.imwrite(path, image)
    
    return path

def contours_obj(img_draw, mask, height, width):

    contours, hierarchy = cv.findContours(mask, cv.RETR_TREE ,cv.CHAIN_APPROX_NONE)

    contour = max(contours, key = cv.contourArea, default=0)

    cv.drawContours(img_draw, contour, -1, (0, 0, 255), 5)
    
    if len(contours)>0:
        M = cv.moments(contour)
        if(M["m10"] !=0 and M["m01"] !=0 and M["m00"] !=0):
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
    else:
        pass

    if cX > int(width / 2):
             obj_angle = 180 - np.degrees(np.arctan((height - cY) / (cX - int(width / 2))))

    elif cX < int(width / 2):
             obj_angle = np.degrees(np.arctan((height - cY) / (int(width / 2) - cX )))
    else:
         cX, cY = [0, 0]
         obj_angle = 90

    return obj_angle, img_draw

def contours_calibrate(frameOrig, mask, height, width):

    image_draw = cv.resize(frameOrig, [height, width])

    contours, hierarchy = cv.findContours(mask, cv.RETR_TREE ,cv.CHAIN_APPROX_NONE)

    contour = max(contours, key = cv.contourArea, default=0)

    rect = cv.minAreaRect(contour)
    size = np.array(rect[1])
    box = cv.boxPoints(rect)
    box = np.int0(box)
    cv.drawContours(image_draw, [box], 0, (0, 255, 0), 5)

    return image_draw, size

def obj_mask(src, color):

    frame = cv.resize(src, (200, 200))

    blurred = cv.GaussianBlur(frame, (15, 15), 0)

    hsvImg = cv.cvtColor(blurred, cv.COLOR_BGR2HSV)

    mask = cv.inRange(hsvImg, color[0], color[1])

    return mask