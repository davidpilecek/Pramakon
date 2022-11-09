#!/usr/bin/env python

import sys
from time import sleep
import drive as dr

angleY = 90
angleX = 90

ServoY = dr.Servo(12)
ServoX = dr.Servo(18)

ServoX.setAngle(angleX)
ServoY.setAngle(angleY)
ServoX.stopServo()
ServoY.stopServo()



