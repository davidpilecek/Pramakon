import drive as dr
import config as conf
from time import sleep

servoX = dr.Servo(conf.servoPinX)
servoX.setAngle(60)
servoY = dr.Servo(conf.servoPinY)
servoY.setAngle(150)

sleep(1)

def res_servo(servoX, servoY):
    currX = round(servoX.getAngle())
    currY = round(servoY.getAngle())

    if(currX > conf.servoX_pos):
        for j in range(currX-conf.servoX_pos):
            servoX.setAngle(currX - j)
            sleep(0.02)
    else:
        for i in range(abs(currX-conf.servoX_pos)):
            servoX.setAngle(currX + i)
            sleep(0.02)
            
    if(currY > conf.servoY_pos):
        for j in range(currY-conf.servoY_pos):
            servoY.setAngle(currY - j)
            sleep(0.02)
    else:
        for i in range(abs(currY-conf.servoY_pos)):
            servoY.setAngle(currY + i)
            sleep(0.02)

res_servo(servoX, servoY)
