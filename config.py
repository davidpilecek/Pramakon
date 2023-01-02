import numpy as np
import cv2 as cv

DEBUG = 1

servoX_pos = 110
servoY_pos = 85

p=0.7
i=0
d=0.12

frame_select= 65

#point of frame at which we seek the presence of object
seek_line = 0.7

#PWM values
pwmMin = 52
pwmMax = 70
frequency = 25

#height and width of image
height = 200
width = 200

centerY = round(height / 2)
centerX = round(width / 2)

path_pic = r"C:\Users\David\Desktop\cvPics\img"
path_pic_Pi = r"/home/pi/Desktop/cvPics/img"

blue = np.array([[95,70,80], [135,255,255]])
green = np.array([[40, 80, 90], [95, 255, 255]])

tol = 10

ang_tol = 10

step = 1

#RPi pin config
leftMot = 19
rightMot = 13
servoPinX = 12
servoPinY = 18

basePwm = (pwmMin + pwmMax) / 2

if __name__ == "__main__":
    color = (40, 80, 90)
    print(color)
    while True:
        image = np.zeros((500, 500, 3), np.uint8)
        image[:] = color
        
        im_conv = cv.cvtColor(image, cv.COLOR_HSV2BGR)

        #cv.imshow("image", image)
        cv.imshow("cvt", im_conv)
        if cv.waitKey(1) == ord('q'):
            break