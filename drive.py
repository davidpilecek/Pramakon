from time import sleep
import sys
sys.path.append('/home/pi/pigpio-master')
from config import *
import pigpio

class Robot():
    def __init__(self, leftMot, rightMot):
        self.pi = pigpio.pi()
        self.leftMot = leftMot
        self.rightMot = rightMot
        self.pi.set_mode(self.leftMot, pigpio.OUTPUT)
        self.pi.set_mode(self.rightMot, pigpio.OUTPUT)
        self.pi.set_PWM_frequency(self.leftMot, PWM_FREQUENCY)
        self.pi.set_PWM_frequency(self.rightMot, PWM_FREQUENCY)
        self.pi.set_PWM_range(self.leftMot, 100)
        self.pi.set_PWM_range(self.rightMot, 100)
    def straight(self, speed):
        self.pi.set_PWM_dutycycle(self.leftMot, speed)
        self.pi.set_PWM_dutycycle(self.rightMot, speed)
        print(f"left: {self.pi.get_PWM_dutycycle(self.leftMot)}")
        print(f"right: {self.pi.get_PWM_dutycycle(self.rightMot)}")
    def moveBoth(self, speedL, speedR):
        self.pi.set_PWM_dutycycle(self.leftMot, speedL)
        self.pi.set_PWM_dutycycle(self.rightMot, speedR)
        print(f"left: {self.pi.get_PWM_dutycycle(self.leftMot)}")
        print(f"right: {self.pi.get_PWM_dutycycle(self.rightMot)}")
    def moveL(self, speed):
        self.pi.set_PWM_dutycycle(self.leftMot, speed)
        self.pi.set_PWM_dutycycle(self.rightMot, 0)
        print(f"left: {self.pi.get_PWM_dutycycle(self.leftMot)}")
        print(f"right: {self.pi.get_PWM_dutycycle(self.rightMot)}")
    def moveR(self, speed):
        self.pi.set_PWM_dutycycle(self.leftMot, 0)
        self.pi.set_PWM_dutycycle(self.rightMot, speed)
        print(f"left: {self.pi.get_PWM_dutycycle(self.leftMot)}")
        print(f"right: {self.pi.get_PWM_dutycycle(self.rightMot)}")
    def stop(self):
        print(f"stopping robot")
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
    def reset(self,servo, servo_pos):
        self.servo_pos = servo_pos
        self.servo = servo
        self.curr = round(servo.getAngle())

        if(self.curr > self.servo_pos):
            for j in range(self.curr-self.servo_pos):
                servo.setAngle(self.curr - j)
                sleep(0.02)
        else:
            for i in range(abs(self.curr-self.servo_pos)):
                servo.setAngle(self.curr + i)
                sleep(0.02)

    def stopServo(self):
        self.pi.set_servo_pulsewidth(self.servoPin, 0)

if __name__ == "__main__":
         servoX = Servo(X_SERVO_PIN)
         servoX.reset(servoX, SERVOX_POS)
#         servoX.setAngle(120)
