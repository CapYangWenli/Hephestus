import cv2
import numpy as npa
from motor import Car

cap = cv2.VideoCapture(0)
car = Car()
angle = 40
mt_speed = 20
ang_stat = 0
mt_drc = True

while True:
    try:
        ret, frame = cap.read()

        if cv2.waitKey(1)&0xFF == ord("l"):
           car.s.angle -= 10

        if cv2.waitKey(1)&0xFF == ord("r"):
           car.s.angle += 10

        if cv2.waitKey(1)&0xFF == ord("w"):
            if mt_drc:
                mt_speed += 10
            else:
                mt_speed -= 10

        if cv2.waitKey(1)&0xFF == ord("s"):
            if not mt_drc:
                mt_speed += 10
            else:
                mt_speed -= 10


        if cv2.waitKey(1)&0xFF == ord("e"):
          mt_speed = 0
          mt_drc = True

        if mt_speed > 100:
            mt_speed = 100

        if mt_speed < 0:
            mt_drc = not mt_drc
            mt_speed = abs(mt_speed)

        car.ChangeMotorSp(mt_speed)
    except:
        continue