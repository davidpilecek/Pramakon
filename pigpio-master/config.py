import numpy as np

crop_selection = 1.5

#height and width of image
height = 400
width = 400

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
leftMot = 33
rightMot = 35

servoPinX = 18
servoPinY = 12

#PWM values
pwmMin = 25
pwmMax = 70
basePwm = (pwmMin + pwmMax) / 2
frequency = 30

#values for brightness balancing
increment = 8
threshold = 100
threshold_max = 200
threshold_min = 30
th_iterations = 15
white_min=2
white_max=30
