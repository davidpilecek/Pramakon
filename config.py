import numpy as np
import cv2 as cv

DEBUG = 1

SERVOX_POS = 110
SERVOY_POS = 85

UPLOAD=True

DO_DRIVE = True

KP=0.7
KI=0
KD=0.12

FRAME_SELECT= 60

#point of frame at which we seek the presence of object
SEEK_OBJECT = 0.8

#PWM values
PWM_MIN = 52
PWM_MAX = 70
PWM_FREQUENCY = 25

#height and width of image
HEIGHT_OF_IMAGE = 250
WIDTH_OF_IMAGE = 250

CENTER_Y = round(HEIGHT_OF_IMAGE / 2)
CENTER_X = round(WIDTH_OF_IMAGE / 2)

PATH_PIC = r"C:\Users\David\Desktop\cvPics\img"
PATH_PIC_PI = r"/home/pi/Documents/Pramakon/unclassified_pics/img"

BLUE_HSV_RANGE = np.array([[95,55,35], [135,255,255]])
GREEN_HSV_RANGE = np.array([[40, 30, 40], [100, 255, 255]])

CENTER_TOLERANCE = 10

ANGLE_TOLERANCE = 10

SERVO_STEP = 1

#RPi pin config
LEFT_MOTOR_PIN = 19
RIGHT_MOTOR_PIN = 13
X_SERVO_PIN = 12
Y_SERVO_PIN = 18

BASE_PWM = (PWM_MIN + PWM_MAX) / 2

if __name__ == "__main__":
    color = (40, 50, 50)
    print(color)
    while True:
        image = np.zeros((500, 500, 3), np.uint8)
        image[:] = color
        
        im_conv = cv.cvtColor(image, cv.COLOR_HSV2BGR)

        #cv.imshow("image", image)
        cv.imshow("cvt", im_conv)
        if cv.waitKey(1) == ord('q'):
            break
