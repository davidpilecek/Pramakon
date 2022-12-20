import drive as dr
import config as conf
from time import sleep

servoX = dr.Servo(conf.servoPinX)
servoX.setAngle(50)
servoY = dr.Servo(conf.servoPinY)
servoY.setAngle(50)

sleep(1)
currX = round(servoX.getAngle())
currY = round(servoY.getAngle())

def res_servo(servoX, servoY):
   
    if(currX > conf.servoX_pos):
        for j in range(currX-conf.servoX_pos):
            print(currX - j)
            servoX.setAngle(currX - j)
            sleep(0.02)
    else:
        for i in range(abs(currX-conf.servoX_pos)):
            print(currX + i)
            servoX.setAngle(currX + i)
            sleep(0.02)
            
    if(currY > conf.servoY_pos):
        for j in range(currY-conf.servoY_pos):
            print(currY - j)
            servoY.setAngle(currY - j)
            sleep(0.02)
    else:
        for i in range(abs(currY-conf.servoY_pos)):
            print(currY + i)
            servoY.setAngle(currY + i)
            sleep(0.02)

res_servo(servoX, servoY)
