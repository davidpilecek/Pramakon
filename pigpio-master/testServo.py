import drive as dr
import config as conf
from time import sleep

currAngle = 100

servoX = dr.Servo(conf.servoPinX)
servoY = dr.Servo(conf.servoPinY)
servoX.setAngle(currAngle)
servoY.setAngle(currAngle)

sleep(1)

while True:
    print(currAngle)
    if(currAngle >= 180):
        servoX.stopServo()
        servoY.stopServo()
        break
    servoX.setAngle(currAngle)
    servoY.setAngle(currAngle)
    sleep(0.01)
    currAngle +=conf.step
