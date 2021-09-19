#MOTOR.PY

import RPi.GPIO as GPIO          
from time import sleep
from gpiozero import AngularServo

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
print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
print("\n")    
while(1):

    x=raw_input()
    
    if x=='r':
        print("run")
        if(temp1==1):
         GPIO.output(in1,GPIO.LOW)
         GPIO.output(in2,GPIO.HIGH)
         GPIO.output(in3,GPIO.LOW)
         GPIO.output(in4,GPIO.HIGH)
         print("forward")
        else:
         GPIO.output(in1,GPIO.HIGH)
         GPIO.output(in2,GPIO.LOW)
         GPIO.output(in3,GPIO.HIGH)
         GPIO.output(in4,GPIO.LOW)
         print("backward")
         x='z'
    elif x=='s':
        print("stop")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.LOW)
        x='z'

    elif x=='f':
        print("forward")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.HIGH)
        temp1=1
        x='z'
    elif x=='b':
        print("backward")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.LOW)
        temp1=0
        x='z'

    elif x=='l':
            print("low")
            pa.ChangeDutyCycle(25)
            pb.ChangeDutyCycle(25)
            x='z'

    elif x=='m':
        print("medium")
        pa.ChangeDutyCycle(50)
        pb.ChangeDutyCycle(50)
        x='z'
    elif x=='h':
        print("high")
        pa.ChangeDutyCycle(75)
        pb.ChangeDutyCycle(75)
        x='z'

    elif x == 'p':
        print("left")
        s.angle = ang
        x = 'z'

    elif x == ']':
        print("right")
        s.angle = -ang
        x = 'z'
        
    elif x == '[':
        print("forward")
        s.angle = zang
        x = 'z'

    elif x=='e':
        GPIO.cleanup()
        break
    
    else:
        print("<<<  wrong data  >>>")
        print("please enter the defined data to continue.....")