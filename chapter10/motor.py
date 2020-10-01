"""
File: chapter10/motor.py

Using a L293D as a H-Bridge to control a DC Motor.

Dependencies:
  pip3 install pigpio

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""
import pigpio                                                   # (1)
from time import sleep
from motor_class import Motor

# Motor A
CHANNEL_1_ENABLE_GPIO = 18                                      # (2)
INPUT_1Y_GPIO = 23 
INPUT_2Y_GPIO = 24

# Motor B
CHANNEL_2_ENABLE_GPIO = 16                                      # (3)
INPUT_3Y_GPIO = 20
INPUT_4Y_GPIO = 21

pi = pigpio.pi()                                                # (4)
motor_A = Motor(pi, CHANNEL_1_ENABLE_GPIO, INPUT_1Y_GPIO, INPUT_2Y_GPIO)
motor_B = Motor(pi, CHANNEL_2_ENABLE_GPIO, INPUT_3Y_GPIO, INPUT_4Y_GPIO)


if __name__ == '__main__':
    try:
        # Make the motors move

        print("Motor A and B Speed 50, Right")
        motor_A.set_speed(50)                                   # (5)
        motor_A.right()
        motor_B.set_speed(50)    
        motor_B.right()
        sleep(2)

        print("Motor A Speed 100")
        motor_A.set_speed(100)

        print("Motor B Left")
        motor_B.left()
        sleep(2)

        print("Motor B Speed 100")
        motor_B.set_speed(100)
        sleep(2)        

        print("Motor A Classic Brake, Motor B PWM Brake")
        motor_A.brake()                                         # (6)
        motor_B.brake_pwm()
        sleep(2)

    finally:
        motor_A.set_speed(0)                                               
        motor_B.set_speed(0)                                               
        pi.stop()
