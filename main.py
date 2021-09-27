import motor
import lane_detection

lane_detection.init()

while True:
    
    servo_angle = lane_detection.main()
    motor.ChangeServoAng(servo_angle)
    motor.ChangeMotorSp(30)