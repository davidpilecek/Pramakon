from time import sleep

import RPi.GPIO as GPIO

import pigpio

import config as conf

GPIO.setmode(GPIO.BOARD)

class Robot():
    def __init__(self, leftMot, rightMot):
        GPIO.setwarnings(False)
        self.leftMot = leftMot
        self.rightMot = rightMot
        GPIO.setup(leftMot,GPIO.OUT)
        GPIO.setup(rightMot,GPIO.OUT)
        self.pwmL = GPIO.PWM(self.leftMot,conf.frequency)
        self.pwmL.start(0)
        self.pwmR = GPIO.PWM(self.rightMot,conf.frequency)
        self.pwmR.start(0)
    def straight(self, speed):
        self.pwmL.ChangeDutyCycle(speed)
        self.pwmR.ChangeDutyCycle(speed)
    def moveBoth(self, speedL, speedR):
        self.pwmL.ChangeDutyCycle(speedL)
        self.pwmR.ChangeDutyCycle(speedR) 
    def moveL(self, speed):
        self.pwmR.ChangeDutyCycle(speed)
        self.pwmL.ChangeDutyCycle(0)
    def moveR(self, speed):
        self.pwmR.ChangeDutyCycle(0)
        self.pwmL.ChangeDutyCycle(speed)
    def stop(self,time = 0):
        self.pwmL.ChangeDutyCycle(0)
        self.pwmR.ChangeDutyCycle(0)
        
class Servo():
    def __init__(self, servoPin):
        self.pi = pigpio.pi()
        self.servoPin = servoPin
    def setAngle(self, servoAngle):
        self.servoAngle = servoAngle
        self.dutyCycle = (self.servoAngle/180 + 1) * 1000
        self.pi.set_servo_pulsewidth(18, self.dutyCycle)
    def stopServo(self):
        sleep(0.2)
        self.pi.set_servo_pulsewidth(18, 0)

                

def test():
    
   return 0

if __name__ == "__main__":
    test()


