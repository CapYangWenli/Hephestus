#MOTOR.PY

import RPi.GPIO as GPIO          
from time import sleep
from gpiozero import AngularServo
from scripts import StringToTuple

s = AngularServo(13) 

ang = -42
zang = 0

in1 = 24
in2 = 25
ena = 23

in3 = 17
in4 = 27
enb = 22

temp1=1

s.angle = zang

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(ena,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
pa=GPIO.PWM(ena,1000)

GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(enb,GPIO.OUT)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
pb=GPIO.PWM(enb,1000)

pa.start(25)
pb.start(25)

print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("You should write three numbers separated by comma.")
print("First one is responsible for motor speed. It shoul range from 0 to 100")
print("The second number is servo angle. It must be in range of -15 to 15")
print("The third number is direction of motors. It must be either 1 or 0 where 1 is forward and 0 is backward")
print("\n")

def ChangeMotorSp(val):
    pa.ChangeDutyCycle(val)
    pb.ChangeDutyCycle(val)

def ChangeServoAng(val):
    s.angle = val

def ChangeMotorDrc(bol):
    GPIO.output(in1, not bol)
    GPIO.output(in2, bol)
    GPIO.output(in3, not bol)
    GPIO.output(in4, bol)


def main():
    while(1):
    
        tup = StringToTuple(raw_input())
    
        mot_sp, s_angl, drc = tup

        ChangeMotorSp(mot_sp)
        ChangeServoAng(s_angl)
        ChangeMotorDrc(drc)

if __name__ == "__main__":
    main()
    
