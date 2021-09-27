import motor
from lane_detection import np, cv2, detect_lane

cap = cv2.VideoCapture(0)

while True:
    res, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([60, 40, 40])
    upper_blue = np.array([150, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    edges = cv2.Canny(mask, 200, 400)
    cropped_edges = cv2.bitwise_and(edges, mask)
    _, servo_angle = detect_lane(frame, hsv, lower_blue, upper_blue, mask, edges) 
    motor.ChangeServoAng(servo_angle)
    motor.ChangeMotorSp(30)
    