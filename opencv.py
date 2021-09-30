
import cv2
import numpy as np
import time

def nothing (x):
    pass
 
kernel = np.ones((5, 5), np.uint8)
 
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read(0)
    frame = cv2.bilateralFilter (frame, 9, 75,75)
    hsv  = cv2.cvtColor (frame, cv2.COLOR_BGR2HSV)
    
 #RED COLOR DETECTION

    red_lower = np.array([136, 87, 111])
    red_upper = np.array([180,255,255])
    red_mask = cv2.inRange(hsv, red_lower, red_upper)
    res_red = cv2.bitwise_and(frame, frame, mask=red_mask)
    red_opening = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)
    red_closing = cv2.morphologyEx(red_opening, cv2.MORPH_CLOSE, kernel)

    contours, h = cv2.findContours(red_closing, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse = True)

    for x in range(len(contours)):
        area = cv2.contourArea(contours[x])
        if area>300:
            x, y, w, h = cv2.boundingRect(contours[x])
            frame = cv2.rectangle(frame, (x, y), (x+w, y+h),( 0, 255, 0), 2)
            frame = cv2.rectangle(frame, (x, y), (x+60, y-25), (0, 0, 0), -1)
            #frame = cv2.circle(frame, (x + (w//2),y + (h//2)), 20, (0, 255, 0), -1)
            print("x:",x + (w//2),"y:",y + (h//2))
            cv2.putText(frame, "Red", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)

 #GREEN COLOR DETECTION

    green_lower = np.array([35, 71, 63])
    green_upper = np.array([159, 245, 120])
    green_mask = cv2.inRange(hsv, green_lower, green_upper)
    res_green = cv2.bitwise_and(frame, frame, mask=green_mask)
    green_opening = cv2.morphologyEx(green_mask, cv2.MORPH_OPEN, kernel)
    green_closing = cv2.morphologyEx(green_opening, cv2.MORPH_CLOSE, kernel)

    contours, h = cv2.findContours(green_closing, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse = True)

    for x in range(len(contours)):
        area = cv2.contourArea(contours[x])
        if area>300:
            x, y, w, h = cv2.boundingRect(contours[x])
            frame = cv2.rectangle(frame, (x, y), (x+w, y+h),( 0, 255, 0), 2)
            frame = cv2.rectangle(frame, (x, y), (x+60, y-25), (0, 0, 0), -1)
            #frame = cv2.circle(frame, (x + (w//2),y + (h//2)), 20, (0, 255, 0), -1)
            print("x:",x + (w//2),"y:",y + (h//2))
            cv2.putText(frame, "Green", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
   
    cv2.imshow("frame", frame)
 
    k = cv2.waitKey(1)&0xFF
    if k==1:
        break
 
cv2.destroyAllWindows ()




