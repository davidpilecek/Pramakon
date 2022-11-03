import numpy as np

crop_selection = 1.5

height = 200
width = 200

path = r"C:\Users\David\Documents\git\OpenCVNew\video.mp4"

blue = np.array([[80,50,50], [130,255,255]])

leftMot = 33
rightMot = 35

pwmMin = 25

pwmMax = 70

basePwm = (pwmMin + pwmMax) / 2

frequency = 30

threshold = 100

increment = 8

threshold_max = 200

threshold_min = 30

th_iterations = 15

white_min=2

white_max=30

