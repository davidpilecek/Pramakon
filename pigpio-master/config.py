import numpy as np

crop_selection = 1.8

#height and width of image
height = 200
width = 200

centerY = round(height / 2)
centerX = round(width / 2)

pathPC = r"C:\Users\David\Documents\git\OpenCVNew\video.mp4"
pathPi = r"/home/pi/Desktop/video.mp4"

path_pic = r"/home/pi/Desktop/cvPics/"


blue = np.array([[85,80,100], [130,255,255]])

red = np.array([[170, 70, 50], [180, 255, 255]])

tol = 50

step = 1

#RPi pin config
leftMot = 19
rightMot = 13
servoPinX = 18
servoPinY = 12

#PWM values
pwmMin = 30
pwmMax = 70
basePwm = (pwmMin + pwmMax) / 2
frequency = 40

#values for brightness balancing
increment = 8
threshold = 150
threshold_max = 250
threshold_min = 50
th_iterations = 15
white_min=5
white_max=50
