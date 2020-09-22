"""
File: chapter10/servo_alt.py

Controlling a servo.

Dependencies:
  pip3 install pigpio

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""
from time import sleep
import pigpio

SERVO_GPIO = 21

# Pulse widths for extreme left/right and center positions in nanoseconds.
# The default values are 'typical' values for a hobby servo.
# Be gradual when changing the left and right adjustments
# because a servo can be damaged if rotated beyond its limits.
RIGHT_PULSE   = 1000  # Smaller values for 'more' right             # (1)
LEFT_PULSE    = 2500  # Higher values for 'more' left
#CENTER_PULSE = 1500  # or calculate as below
CENTER_PULSE = ((LEFT_PULSE - RIGHT_PULSE) // 2) + RIGHT_PULSE

# Delay to give servo time to move
MOVEMENT_DELAY_SECS = 0.5                                           # (2)

pi = pigpio.pi()
pi.set_mode(SERVO_GPIO, pigpio.OUTPUT)


def idle():                                                         # (3)
    """
    Idle servo (zero pulse width).
    Servo will be rotatable by hand with little force.
    """
    pi.set_servo_pulsewidth(SERVO_GPIO, 0)


def center():
     """
     Center the servo.
     """
     pi.set_servo_pulsewidth(SERVO_GPIO, CENTER_PULSE)


def left():
    """
    Rotate servo to full left position.
    """
    pi.set_servo_pulsewidth(SERVO_GPIO, LEFT_PULSE)


def right():
    """
    Rotate servo to full right position.
    """
    pi.set_servo_pulsewidth(SERVO_GPIO, RIGHT_PULSE)


def angle(to_angle):
    """
    Rotate servo to specified angle (between -90 and +90 degrees)
    """

    # Restrict to -90..+90 degrees
    to_angle = int(min(max(to_angle, -90), 90))

    ratio = (to_angle + 90) / 180.0
    pulse_range = LEFT_PULSE - RIGHT_PULSE
    pulse = LEFT_PULSE - round(ratio * pulse_range) 

    pi.set_servo_pulsewidth(SERVO_GPIO, pulse)


def sweep(count=4):
    """
    Sweep servo horn left and right 'count' times.
    """
    left() # Starting position
    sleep(MOVEMENT_DELAY_SECS)

    for i in range(count):
        right()
        sleep(MOVEMENT_DELAY_SECS)
        left()
        sleep(MOVEMENT_DELAY_SECS)


if __name__ == '__main__':

    try:
        print("Sweeping left and right")
        sweep()

    finally:
        idle() # Idle servo.
        pi.stop() # PiGPIO Cleanup
