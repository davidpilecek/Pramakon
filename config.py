import numpy as np

#voltage = 4.5 V

#ZKUSIT DRIVER NAPAJET PRIMO Z POWERBANKY



path = r"C:\Users\David\Documents\git\OpenCVNew\video.mp4"

lower_blue = np.array([90, 60, 70])
upper_blue = np.array([128, 255, 255])

blue = [lower_blue, upper_blue]

leftMot = 33
rightMot = 35

pwmMin = 30

pwmMax = 100

basePwm = (pwmMin + pwmMax) / 2

frequency = 25

pwm = 60

threshold = 120

threshold_max = 255

threshold_min = 40

th_iterations = 10

white_min=4

white_max=30
