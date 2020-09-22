"""
File: chapter14/tree_mqtt_service/servo.py

Hardware Interface Layer to Servo.

Built and tested with Python 3.7 on Raspberry Pi 4 Model B

Dependencies:
  pip3 install pigpio
"""
from time import sleep
import pigpio
import threading
import logging

logger = logging.getLogger('ServoController')

class Servo:

    def __init__(self, servo_gpio, pi=None, pulse_left_ns=2500, pulse_right_ns=1000, pulse_centre_ns=None):
        """
        Constructor.
        Pulse widths for extreme left (pulse_left_ns) / right (pulse_right_ns) and center (pulse_centre_ns)
        positions in nanoseconds. The default values are 'typical' values for a hobby servo.
        Be gradual when changing the left and right adjustments
        because a servo can be damaged if rotated beyond its limits.
        """

        self.gpio = servo_gpio

        if pi is None:
            self.pi = pi = pigpio.pi()
        else:
            self.pi = pi

        self.pulse_left_ns = pulse_left_ns
        self.pulse_right_ns = pulse_right_ns

        if pulse_centre_ns is None:
            self.pulse_centre_ns = ((pulse_left_ns - pulse_right_ns) // 2) + pulse_right_ns


    def idle(self):
        """
        Idle servo (zero pulse width).
        Servo will be rotatable by hand with little force.
        """
        self.pi.set_servo_pulsewidth(self.gpio, 0)


    def center(self):
         """
         Center the servo.
         """
         self.pi.set_servo_pulsewidth(self.gpio, self.pulse_centre_ns)


    def left(self):
        """
        Rotate servo to full left position.
        """
        self.pi.set_servo_pulsewidth(self.gpio, self.pulse_left_ns)


    def right(self):
        """
        Rotate servo to full right position.
        """
        self.pi.set_servo_pulsewidth(self.gpio, self.pulse_right_ns)


    def angle(self, to_angle):
        """
        Rotate servo to specified angle (between -90 and +90 degrees)
        """

        # Restrict to -90..+90 degrees
        to_angle = int(min(max(to_angle, -90), 90))

        ratio = (to_angle + 90) / 180.0
        pulse_range = self.pulse_left_ns - self.pulse_right_ns
        pulse = self.pulse_left_ns - round(ratio * pulse_range)

        self.pi.set_servo_pulsewidth(self.gpio, pulse)


    def sweep(self, count=4, degrees=90, movement_delay_secs=0.5):
        """
        Sweep servo horn left and right 'degrees' degrees by 'count' times, and
        sleep for movement_delay_secs in-between each movement (to give servo time to complete
        movement)
        """

        self.angle(-degrees) # Starting position
        sleep(movement_delay_secs)

        for i in range(count):
            self.angle(+degrees)
            sleep(movement_delay_secs)
            self.angle(-degrees)
            sleep(movement_delay_secs)

