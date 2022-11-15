import drive as dr
import config as conf
from time import sleep

currAngle = 80

servoX = dr.Servo(conf.servoPinX)
servoX.setAngle(currAngle)
servoY = dr.Servo(conf.servoPinY)
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
    currAngle +=1
    sleep(0.005)
