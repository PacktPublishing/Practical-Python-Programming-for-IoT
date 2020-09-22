"""
File: chapter11/hc-sr04.py

Ultrasonic Distance Measurement Example.

Dependencies:
  pip3 install pigpio

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""
from time import sleep, time
import pigpio

# REMEMBER the HC-SR04 is a 5-volt
# device so you MUST use a voltage
# divider on ECHO_GPIO
TRIG_GPIO = 20                                         # (1)
ECHO_GPIO = 21


# Speed of Sound in meters per second
# at 20 degrees C (68 degrees F)
VELOCITY = 343                                         # (2)

# Sensor timeout and return value
TIMEOUT_SECS = 0.1   # based on max distance of 4m     # (3)
SENSOR_TIMEOUT  = -1

pi = pigpio.pi()

# Initialise GPIOs
pi.set_mode(TRIG_GPIO, pigpio.OUTPUT)
pi.write(TRIG_GPIO, pigpio.LOW)
pi.set_mode(ECHO_GPIO, pigpio.INPUT)
pi.set_pull_up_down(ECHO_GPIO, pigpio.PUD_DOWN)

# For timing our ultrasonic pulse
echo_callback = None                                   # (4)
tick_start = -1
tick_end = -1
reading_success = False


def trigger():                                         # (5)
    """ Trigger ultrasonic pulses """
    global reading_success

    reading_success = False

    # Start ultrasonic pulses
    pi.write(TRIG_GPIO, pigpio.HIGH)                   # (6)
    sleep(1 / 1000000) # Pause 10 microseconds
    pi.write(TRIG_GPIO, pigpio.LOW)


def get_distance_cms():                                # (7)
    """ Get distance in centimeters """
    trigger()

    timeout = time() + TIMEOUT_SECS                    # (8)
    while not reading_success:
      if time() > timeout:
          return SENSOR_TIMEOUT
      sleep(0.01)

    # Elapsed time in microseconds. Divide by 2 to get time from sensor to object.
    elapsed_microseconds = pigpio.tickDiff(tick_start, tick_end) / 2                        # (9)

    # Convert to seconds
    elapsed_seconds = elapsed_microseconds / 1000000

    # Calculate distance in meters (d = v * t)
    distance_in_meters = elapsed_seconds * VELOCITY                                         # (10)

    # Convert to centimeters
    distance_in_centimeters = distance_in_meters * 100

    return distance_in_centimeters


def echo_handler(gpio, level, tick):                                                        # (11)
    """ Called whenever a level change occurs on ECHO_GPIO Pin.
      Parameters defined by PiGPIO pi.callback() """
    global tick_start, tick_end, reading_success

    if level == pigpio.HIGH:
        tick_start = tick # Start Timer                                                     # (12)

    elif level == pigpio.LOW:
        tick_end = tick # End Timer                                                         # (13)
        reading_success = True


# Register ECHO Pin Callback
echo_callback = pi.callback(ECHO_GPIO, pigpio.EITHER_EDGE, echo_handler)                    # (14)


if __name__ == "__main__":

    try:
        print("Press Control + C to Exit")

        while True:                                                                         # (15)

            distance_cms = get_distance_cms()

            if distance_cms == SENSOR_TIMEOUT:
                print("Timeout")
            else:
                distance_inches = distance_cms/2.54
                print("{:0.4f}cm, {:0.4f}\"".format(distance_cms, distance_inches))

            sleep(0.25) # Sleep a little between readings. (Note - We shouldn't query the sensor more than once every 60ms.)

    except KeyboardInterrupt:
        echo_callback.cancel()
        pi.stop()
