from drive import Servo
from config import *
from time import sleep

servoX = Servo(X_SERVO_PIN)
servoX.setAngle(60)
servoY = Servo(Y_SERVO_PIN)
servoY.setAngle(150)

sleep(1)

servoX.reset(servoX, SERVOX_POS)
servoY.reset(servoY, SERVOY_POS)