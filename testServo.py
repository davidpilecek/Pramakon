from time import sleep

import config as conf
import drive as dr

ServoX = dr.Servo(conf.servoPinX)
ServoY = dr.Servo(conf.servoPinY)

ServoX.setAngle(90)
ServoY.setAngle(90)




