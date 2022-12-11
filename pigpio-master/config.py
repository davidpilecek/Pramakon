import numpy as np
import cv2 as cv

servoX_pos = 110
servoY_pos = 75

frame_select= 60

#PWM values
pwmMin = 50
pwmMax = 80
frequency = 25

#height and width of image
height = 200
width = 200

centerY = round(height / 2)
centerX = round(width / 2)

pathPC = r"C:\Users\David\Documents\git\OpenCVNew\video.mp4"
pathPi = r"/home/pi/Desktop/video.mp4"

path_pic = r"/home/pi/Desktop/cvPics/"

blue = np.array([[80,20,100], [135,255,255]])

green = np.array([[45, 50, 100], [95, 255, 255]])
tol = 50

ang_tol = 10

step = 1

#RPi pin config
leftMot = 19
rightMot = 13
servoPinX = 12
servoPinY = 18

basePwm = (pwmMin + pwmMax) / 2

#values for brightness balancing
increment = 8
threshold = 120
threshold_max = 250
threshold_min = 50
th_iterations = 15
white_min=20
white_max=50

if __name__ == "__main__":
    while True:
        image = np.zeros((500, 500, 3), np.uint8)
        image[:] = (90, 60, 100)
      
        im_conv = cv.cvtColor(image, cv.COLOR_HSV2BGR)

        #cv.imshow("image", image)
        cv.imshow("cvt", im_conv)
        if cv.waitKey(1) == ord('q'):
            break
