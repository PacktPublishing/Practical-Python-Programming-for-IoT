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
RIGHT_PULSE = 1000  # Smaller values for 'more' right
LEFT_PULSE = 2500  # Higher values for 'more' left
# CENTER_PULSE = 1500  # or calculate as below
CENTER_PULSE = ((LEFT_PULSE - RIGHT_PULSE) // 2) + RIGHT_PULSE

# Delay to give servo time to move
MOVEMENT_DELAY_SECS = 0.5

pi = pigpio.pi()

# Servos commonly operate at 50Hz, that is one pulse every 20ms  (1 second / 50 Hz = 0.02)
pi.set_PWM_frequency(SERVO_GPIO, 50)
PULSE_WIDTH = 20000.0  # 20000 microsecond = 20 milliseconds = 0.02 seconds

DUTYCYCLE_RANGE = 100
# DUTYCYCLE_RANGE = pi.get_PWM_range(SERVO_GPIO)  # Default is 255
pi.set_PWM_range(SERVO_GPIO, DUTYCYCLE_RANGE)


def idle():
    """
    Idle servo (zero pulse width).
    Servo will be rotatable by hand with little force.
    """

    # WAS
    # pi.set_servo_pulsewidth(SERVO_GPIO, 0)

    # NOW
    dutycycle = 0
    pi.set_PWM_dutycycle(SERVO_GPIO, dutycycle)


def center():
    """
    Center the servo.
    """

    # WAS
    # pi.set_servo_pulsewidth(SERVO_GPIO, CENTER_PULSE)

    # NOW
    dutycycle_percent = CENTER_PULSE / PULSE_WIDTH
    # Scale duty cycle percentage into PiGPIO duty cycle range 
    dutycycle = dutycycle_percent * DUTYCYCLE_RANGE
    pi.set_PWM_dutycycle(SERVO_GPIO, dutycycle)


def left():
    """
    Rotate servo to full left position.
    """

    # WAS
    # pi.set_servo_pulsewidth(SERVO_GPIO, LEFT_PULSE)

    # NOW
    dutycycle_percent = LEFT_PULSE / PULSE_WIDTH

    # Scale duty cycle percentage into PiGPIO duty cycle range 
    dutycycle = dutycycle_percent * DUTYCYCLE_RANGE

    pi.set_PWM_dutycycle(SERVO_GPIO, dutycycle)


def right():
    """
    Rotate servo to full right position.
    """

    # WAS
    # pi.set_servo_pulsewidth(SERVO_GPIO, RIGHT_PULSE)

    # NOWz
    dutycycle_percent = RIGHT_PULSE / PULSE_WIDTH

    # Scale duty cycle percentage into PiGPIO duty cycle range
    dutycycle = dutycycle_percent * DUTYCYCLE_RANGE

    pi.set_PWM_dutycycle(SERVO_GPIO, dutycycle)


def angle(to_angle):
    """
    Rotate servo to specified angle (between -90 and +90 degrees)
    """

    # Restrict to -90..+90 degrees
    to_angle = int(min(max(to_angle, -90), 90))

    ratio = (to_angle + 90) / 180.0
    pulse_range = LEFT_PULSE - RIGHT_PULSE
    pulse = LEFT_PULSE - round(ratio * pulse_range)

    # WAS
    # pi.set_servo_pulsewidth(SERVO_GPIO, pulse)

    # NOW
    # Pulse in seconds divided by frequency in Hertz
    dutycycle_percent = (pulse / 1000) / 50

    # Scale duty cycle percentage into PiGPIO duty cycle range
    dutycycle = dutycycle_percent * DUTYCYCLE_RANGE

    pi.set_PWM_dutycycle(SERVO_GPIO, dutycycle)


def sweep(count=4):
    """
    Sweep servo horn left and right 'count' times.
    """

    left()  # Starting position
    sleep(MOVEMENT_DELAY_SECS)

    for i in range(count):
        right()
        sleep(MOVEMENT_DELAY_SECS)
        left()
        sleep(MOVEMENT_DELAY_SECS)


if __name__ == '__main__':
    try:
        sweep()

    finally:
        idle()
        pi.stop() # PiGPIO Cleanup
