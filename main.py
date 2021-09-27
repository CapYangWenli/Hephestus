import motor
import lane_detection



while True:
    lane_detection.init()
    servo_angle = lane_detection.main()
    motor.ChangeServoAng(servo_angle)
    motor.ChangeMotorSp(30)