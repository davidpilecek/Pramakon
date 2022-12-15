import cv2 as cv
import numpy as np
import config as conf

def check_orig(last_cont):
    global cX, cY
    if(cX <= last_cont[0] + 10 and  cX >= last_cont[0] - 10 and  cY <= last_cont[1] + 10 and cY >= last_cont[1] - 10):
        return False
    else: return True

def contours_line(frameOrig, mask, height, width):

    image_draw = cv.resize(frameOrig, [height, width])

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
             x_pos = 180 - np.degrees(np.arctan((height - cY) / (cX - int(width / 2))))

    elif cX < int(width / 2):
             x_pos = np.degrees(np.arctan((height - cY) / (int(width / 2) - cX )))
    else:
         cX, cY = [0, 0]
         x_pos = 90

    average_angle = (ang_vector*0.4 + x_pos*0.6)

    average_angle = round(average_angle)

    cv.putText(image_draw, str(round(average_angle)),(50, 50), cv.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    return average_angle, image_draw

def crop_img_obj(img, w, h):

    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

#left column
    vertices_lc = [(0, 0.66*h), (0, h), (0.1*w, h), (0.1*w, 0.66*h)]
    vertices_lc = np.array([vertices_lc], np.int32)

#right column
    vertices_rc = [(0.9*w, 0.66*h), (0.9*w, h), (w, h), (w, 0.66*h)]
    vertices_rc = np.array([vertices_rc], np.int32)

#middle lower layer
    vertices_ll = [(0.1*w, 0.9*h), (0.1*w, h), (0.9*w, h), (0.9*w, 0.9*h)]
    vertices_ll = np.array([vertices_ll], np.int32)

    #create pure black frame size of image
    mask = np.zeros_like(img)

    match_mask_color = 255

    #create pure white frame in area of interest
    cv.fillPoly(mask, vertices_lc, match_mask_color)
    cv.fillPoly(mask, vertices_ll, match_mask_color)
    cv.fillPoly(mask, vertices_rc, match_mask_color)

    #return image with other area than AOI non-reactive to contour seeking algorithm
    masked_image = cv.bitwise_and(img, mask)

    return masked_image

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

    return mask, area

def crop_img_line_color(img, height, width, color, sel):

    crop_selection = 100/(100 - sel)

    height_1 = height/crop_selection

    vertices = [(0, height_1), (0, height),(width, height), (width, height_1)]
    vertices = np.array([vertices], np.int32)

    #create pure black frame size of image
    mask_black = np.zeros_like(img)

    match_mask_color = [255,255,255]

    area = round((height - height_1) * width)

    img = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    #create pure white frame in area of interest
    cv.fillPoly(mask_black, vertices, match_mask_color)

    #return image with other area than AOI non-reactive to contour seeking algorithm
    masked_image = cv.bitwise_and(img, mask_black)
    
    mask = cv.inRange(masked_image, color[0], color[1])

    return mask, area

def prep_pic(src):
    frame = cv.resize(src, (conf.height, conf.width))
    height, width = frame.shape[:2]

    blurred = cv.GaussianBlur(frame, (7, 7), 0)

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
    return way

def save_pic(index, image, path_pic):
    """Alway use original image as argument"""

    path = path_pic + str(index) + r".jpg"
   
    cv.imwrite(path, image)

    index +=1    

    return path, index

def contours_obj(img_draw, mask):

    cX, cY = [0, 0]
    contours, hierarchy = cv.findContours(mask, cv.RETR_EXTERNAL ,cv.CHAIN_APPROX_NONE)

    #contour = max(contours, key = cv.contourArea , default=0)
    # for contour in contours:
    #     cont_area = cv.contourArea(contour)

    for contour in contours:
        x,y,w,h = cv.boundingRect(contour)
        if(w > conf.width/20) and (h > conf.height/20):
            cv.rectangle(img_draw, (x,y), (x+w,y+h), (0,0,255), 5)

    if len(contours)>0:
        M = cv.moments(contour)
        if(M["m10"] !=0 and M["m01"] !=0 and M["m00"] !=0):
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
    else:
        pass
    
    if cX > int(conf.width / 2):
             obj_angle = 180 - np.degrees(np.arctan((conf.height - cY) / (cX - int(conf.width / 2))))

    elif cX < int(conf.width / 2):
             obj_angle = np.degrees(np.arctan((conf.height - cY) / (int(conf.width / 2) - cX )))
    else:
         cX, cY = [0, 0]
         obj_angle = 90

    obj_angle = round(obj_angle)

    return obj_angle, img_draw, cX, cY

def aim_camera_obj(servoX, servoY, obj_x, obj_y, currAngleX, currAngleY):
    cent_x = False
    cent_y = False
    if(obj_x > conf.centerX + conf.tol):
          servoX.setAngle(currAngleX - conf.step)
          cent_x = False
    elif(obj_x < conf.centerX - conf.tol):
          servoX.setAngle(currAngleX + conf.step)
          cent_x = False
    else:
        cent_x = True
    if(obj_y > conf.centerY + conf.tol):
          servoY.setAngle(currAngleY - conf.step)
          cent_y = False
    elif(obj_y < conf.centerY - conf.tol):
          servoY.setAngle(currAngleY + conf.step)
          cent_y = False
    else:
        cent_y = True
    if(cent_x and cent_y):
        return True
    else:
        return False

def obj_mask(src, color):

    hsvImg = cv.cvtColor(src, cv.COLOR_BGR2HSV)

    mask = cv.inRange(hsvImg, color[0], color[1])

    return mask
