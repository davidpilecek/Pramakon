import numpy as np

crop_selection = 1.5

#height and width of image
height = 200
width = 200

centerY = height / 2
centerX = width / 2


path = r"C:\Users\David\Documents\git\OpenCVNew\video.mp4"

blue = np.array([[80,50,50], [130,255,255]])

red = np.array([[170, 70, 50], [180, 255, 255]])

leftMot = 33
rightMot = 35

servoPinX = 32
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

#size of 10 mm in pixels
size_of_cm = 100

#approximate size of detected object in mm [x, y]
size_of_obj = [100, 100]

#desired approximate distance of robot from detected object in mm
distance_from_obj = 500

