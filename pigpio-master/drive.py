from time import sleep

import pigpio

import config as conf

class Robot():
    def __init__(self, leftMot, rightMot):
        self.pi = pigpio.pi()
        self.leftMot = leftMot
        self.rightMot = rightMot
        self.pi.set_mode(self.leftMot, pigpio.OUTPUT)
        self.pi.set_mode(self.rightMot, pigpio.OUTPUT)
        self.pi.set_PWM_frequency(self.leftMot, conf.frequency)
        self.pi.set_PWM_frequency(self.rightMot, conf.frequency)
        self.pi.set_PWM_range(self.leftMot, 100)
        self.pi.set_PWM_range(self.rightMot, 100)
    def straight(self, speed):
        self.pi.set_PWM_dutycycle(self.leftMot, speed)
        self.pi.set_PWM_dutycycle(self.rightMot, speed)
    def moveBoth(self, speedL, speedR):
        self.pi.set_PWM_dutycycle(self.leftMot, speedL)
        self.pi.set_PWM_dutycycle(self.rightMot, speedR)
    def moveL(self, speed):
        self.pi.set_PWM_dutycycle(self.leftMot, speed)
        self.pi.set_PWM_dutycycle(self.rightMot, 0)
    def moveR(self, speed):
        self.pi.set_PWM_dutycycle(self.leftMot, 0)
        self.pi.set_PWM_dutycycle(self.rightMot, speed)
    def stop(self):
        self.pi.set_PWM_dutycycle(self.leftMot, 0)
        self.pi.set_PWM_dutycycle(self.rightMot, 0)
        
class Servo():
    def __init__(self, servoPin):
        self.pi = pigpio.pi()
        self.servoPin = servoPin
    def setAngle(self, servoAngle):
        self.servoAngle = servoAngle
        if(self.servoAngle >= 180):
           self.servoAngle = 180
        elif(self.servoAngle <= 0):
           self.servoAngle = 0

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

                   
if __name__ == "__main__":
         servoX = Servo(conf.servoPinX)
         servoY = Servo(conf.servoPinY)
         servoX.setAngle(130)
         servoY.setAngle(110)
         servoX.stopServo()
         servoY.stopServo()
