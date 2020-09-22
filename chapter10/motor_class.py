"""
File: chapter10/motor_class.py

Using a L293D as a H-Bridge to control a DC Motor.

Dependencies:
  pip3 install pigpio

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""
import pigpio
from time import sleep

class Motor:

    def __init__(self, pi, enable_gpio, logic_1_gpio, logic_2_gpio):

          self.pi = pi
          self.enable_gpio = enable_gpio
          self.logic_1_gpio = logic_1_gpio
          self.logic_2_gpio = logic_2_gpio	  

          pi.set_PWM_range(self.enable_gpio, 100)  # speed is 0..100               # (1)

	      # Set default state - motor not spinning and set for forward direction.
          self.set_speed(0)                                                        # (2)
          self.right()

    def right(self, speed=None):                                                   # (3)
        """
        Spin motor right.
        """
        if speed is not None:
            self.set_speed(speed)

        self.pi.write(self.logic_1_gpio, pigpio.LOW)
        self.pi.write(self.logic_2_gpio, pigpio.HIGH)


    def left(self, speed=None):                                                    # (4)
        """
        Spin motor left.
        """
        if speed is not None:
            self.set_speed(speed)

        self.pi.write(self.logic_1_gpio, pigpio.HIGH)
        self.pi.write(self.logic_2_gpio, pigpio.LOW)

        
    def is_right(self):                                                            # (5)
        """
        Is motor set to spin right?
        """
        return (not self.pi.read(self.logic_1_gpio)  # LOW
              and self.pi.read(self.logic_2_gpio))   # HIGH


    def set_speed(self, speed):                                                    # (6)
        """
        Set motor speed using PWM.
        """
        assert 0<=speed<=100		
        self.pi.set_PWM_dutycycle(self.enable_gpio, speed)


    def brake(self):                                                               # (7)
        """
        Motor Brake (Using L293D).
        """
        was_right = self.is_right() # To restore direction after braking
        
        self.set_speed(100)
        self.pi.write(self.logic_1_gpio, pigpio.LOW)
        self.pi.write(self.logic_2_gpio, pigpio.LOW)
        self.set_speed(0)

        if was_right:
            self.right()
        else:
            self.left()


    def brake_pwm(self, brake_speed=100, delay_millisecs=50):                      # (8)
        """
        Motor Brake (Alternative using Reverse PWM).
        You may need to adjust brake_speed and delay_millisecs
        based on your physical motor and voltage/current usage.
        """
        was_right = None # To restore direction after braking

        if self.is_right():      
            self.left(brake_speed)
            was_right = True
        else:
            self.right(brake_speed)
            was_right = False

        sleep(delay_millisecs / 1000)
        self.set_speed(0)

        if was_right:
            self.right()
        else:
            self.left()