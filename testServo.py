from drive import *
from config import *
from time import sleep

servoX = Servo(X_SERVO_PIN)
servoX.setAngle(120)
servoY = Servo(Y_SERVO_PIN)
servoY.setAngle(120)
robot = Robot(12, 13)

sleep(1)

servoX.reset(servoX, SERVOX_POS)
servoY.reset(servoY, SERVOY_POS)
