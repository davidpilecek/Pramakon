import drive as dr
import config as conf
from time import sleep

servoX = dr.Servo(conf.servoPinX)
servoX.setAngle(60)
servoY = dr.Servo(conf.servoPinY)
servoY.setAngle(90)

sleep(1)

def res_servo(servoX, servoY):
   
    if(servoX.getAngle() > conf.servoX_pos):
        for j in range(servoX.getAngle()-conf.servoX_pos):
            print(servoX.getAngle() - j)
            sleep(0.02)
    else:
        for i in range(abs(servoX.getAngle()-conf.servoX_pos)):
            print(servoX.getAngle() + i)
            sleep(0.02)

res_servo(servoX, servoY)
