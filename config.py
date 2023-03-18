import numpy as np
import cv2 as cv

DEBUG = 1
UPLOAD=True
DO_DRIVE = True

SERVOX_POS = 80 
SERVOY_POS = 35
#PID constants
KP=0.7
KI=0
KD=0.12
#percentage of frame for finding track
FRAME_SELECT= 60
#point of frame at which we seek the presence of object
SEEK_OBJECT = 0.5

#PWM values
PWM_MIN = 40
PWM_MAX = 60
PWM_FREQUENCY = 25

#desired height and width of image
HEIGHT_OF_IMAGE = 250
WIDTH_OF_IMAGE = 250

CENTER_Y = round(HEIGHT_OF_IMAGE / 2)
CENTER_X = round(WIDTH_OF_IMAGE / 2)
CENTER_TOLERANCE = 30

PATH_PIC_PI = r"/home/pi/Pramakon/pics"
PATH_PIC_PC = r"C:\Users\david\Documents\Pramakon\pics"

BLUE_HSV_RANGE = np.array([[95,55,35], [135,255,255]])
GREEN_HSV_RANGE = np.array([[40, 50, 50], [80, 255, 255]])


ANGLE_TOLERANCE = 10

SERVO_STEP = 1

#RPi pin config
LEFT_MOTOR_PIN = 19
RIGHT_MOTOR_PIN = 13
X_SERVO_PIN = 12
Y_SERVO_PIN = 18

BASE_PWM = (PWM_MIN + PWM_MAX) / 2
