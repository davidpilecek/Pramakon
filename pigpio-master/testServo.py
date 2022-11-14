import drive as dr
import config as conf
from time import sleep

currAngle = 80

servo = dr.Servo(conf.servoPinX)
servo.setAngle(currAngle)

sleep(1)

while True:
    print(currAngle)
    if(currAngle >= 180):
        servo.stopServo()
        break
    servo.setAngle(currAngle)
    currAngle +=1
    sleep(0.005)
