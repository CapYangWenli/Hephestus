# from motor import Car
from lane_detection import np, cv2, detect_lane
import logging
import math
import datetime
import sys

dev_angle = 15



# car = Car()
# car.ChangeMotorDrc(1)
# car.ChangeMotorSp(20)



cap = cv2.VideoCapture(0)
while True:

    previous_angle = 0
    try:
        ret, frame = cap.read()
        frame = cv2.addWeighted(frame, 1.6, np.full_like(frame, 0), 1, 1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_blue = np.array([60, 40, 40])
        upper_blue = np.array([150, 255, 255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        edges = cv2.Canny(mask, 200, 400)
        cropped_edges = cv2.bitwise_and(edges, mask)

        _, servo_angle = detect_lane(frame, hsv, lower_blue, upper_blue, mask, edges)
        servo_angle = servo_angle - 90
        
        # if servo_angle - previous_angle > dev_angle:
        #     servo_angle = dev_angle + previous_angle
             
             
        # if servo_angle - previous_angle < -dev_angle:
        #     servo_angle = previous_angle - dev_angle
            
        
        servo_angle = (servo_angle+previous_angle)/2
        
        # car.ChangeServoAng(servo_angle)
        previous_angle = servo_angle
        
        # cap.release()

        if cv2.waitKey(1)&0xFF == ord("q"):
            # car.ChangeMotorSp(0)
            # car.ChangeServoAng(0)
            break

    except:
        continue


cv2.destroyAllWindows() 