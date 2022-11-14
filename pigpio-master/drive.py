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
        self.pi.set_servo_pulsewidth(self.servoPin, self.dutyCycle)
        
    def getAngle(self):
        self.currDutyCycle = self.pi.get_servo_pulsewidth(self.servoPin)
        self.currAngle = (self.currDutyCycle / 1000 - 1) * 180
        currAngle = self.currAngle
        return currAngle
    def stopServo(self):
        sleep(0.2)
        self.pi.set_servo_pulsewidth(self.servoPin, 0)

                

def test(ServoX, ServoY):
   ServoX.setAngle(120)
   ServoY.setAngle(120)
   angx = ServoX.getAngle()
   angy = ServoY.getAngle()
   
   
   return angx, angy

if __name__ == "__main__":
    ServoX = Servo(conf.servoPinX)
    ServoY = Servo(conf.servoPinY)
    angx, angy = test(ServoX, ServoY)
    print(angx, angy)

