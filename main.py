# import motor
import lane_detection
cap = lane_detection.cv2.VideoCapture(0)

while True:
    res, frame = cap.read()
    lane_detection.detect_lane(frame, *lane_detection.loop_condtions()) 
    # servo_angle = lane_detection.main()
    # motor.ChangeServoAng(servo_angle)
    # motor.ChangeMotorSp(30)