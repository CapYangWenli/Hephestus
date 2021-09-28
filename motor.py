#MOTOR.PY

import RPi.GPIO as GPIO          
from time import sleep
from gpiozero import AngularServo
from scripts import StringToTuple

class Car:

    ang = -42
    zang = 0

    in1 = 24
    in2 = 25
    ena = 23

    in3 = 17
    in4 = 27
    enb = 22
    
    @classmethod
    def __init__(cls):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(cls.in1,GPIO.OUT)
        GPIO.setup(cls.in2,GPIO.OUT)
        GPIO.setup(cls.ena,GPIO.OUT)
        GPIO.output(cls.in1,GPIO.LOW)
        GPIO.output(cls.in2,GPIO.LOW)

        cls.pa=GPIO.PWM(cls.ena,1000)

        GPIO.setup(cls.in3,GPIO.OUT)
        GPIO.setup(cls.in4,GPIO.OUT)
        GPIO.setup(cls.enb,GPIO.OUT)
        GPIO.output(cls.in3,GPIO.LOW)
        GPIO.output(cls.in4,GPIO.LOW)

        cls.pb=GPIO.PWM(cls.enb,1000)

        cls.pa.start(25)
        cls.pb.start(25)

        cls.s = AngularServo(13) 

    
    def ChangeMotorSp(self, val):
        self.pa.ChangeDutyCycle(val)
        self.pb.ChangeDutyCyscle(val)
    
    def ChangeServoAng(self, val):
        self.s.angle = val

    def ChangeMotorDrc(self, bol):
        GPIO.output(self.in1, not bol)
        GPIO.output(self.in2, bol)
        GPIO.output(self.in3, not bol)
        GPIO.output(self.in4, bol)

        

def main():
    car1 = Car()
    while(1):
    
        str = input()
        
        str = str.split(" ")
        tup = tuple(map(int, str))

        mot_sp, s_angl, drc = tup

        car1.ChangeMotorSp(mot_sp)
        car1.ChangeServoAng(s_angl)
        car1.ChangeMotorDrc(drc)

if __name__ == "__main__":
    main()
    
