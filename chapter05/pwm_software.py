"""
File: chapter05/pwm_software.py

PWM demo using software PWM and a LED.

Dependencies:
  pip3 install pigpio adafruit-circuitpython-ads1x15 rpi.gpio

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""
import RPi.GPIO as GPIO
from time import sleep

# Below imports are part of Circuit Python and Blinka
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# We're using software PWM which is available on any GPIO Pin.
LED_GPIO_PIN = 12

# RPi.GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_GPIO_PIN, GPIO.OUT)
GPIO.output(LED_GPIO_PIN, GPIO.LOW)

# Create the I2C bus & ADS object.
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)

# Analog Inputs on Channels 0 and 1 (A0 and A1 on breakout board)
frequency_ch = AnalogIn(ads, ADS.P0)
duty_cycle_ch = AnalogIn(ads, ADS.P1)

# The max/min range we get from our Analog Inputs on the ADS1115.
# Max value derived by observation. See print(output1) in while loop.
A_IN_EDGE_ADJ = 0.001 # Edge adjustment factor for MIN_A_IN_VOLTS and MAN_A_IN_VOLTS
MIN_A_IN_VOLTS = 0 + A_IN_EDGE_ADJ
MAX_A_IN_VOLTS = 3.286 - A_IN_EDGE_ADJ

# Max/Min Duty Cycle value as per RPi.GPIO documentation for ChangeDutyCycle()
# https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM
MIN_DUTY_CYCLE = 0
MAX_DUTY_CYCLE = 100

# Max/Min Frequency value for RPi.GPIO method ChangeFrequency(). It's undocumented,
# however we'll assume a max of 70000 (70KHz) as per this link (noting that it
# might not be still accurate on a raspberry Pi 3). However..... we're
# capping it at 60 hertz for LED visual and piscope demonstration.
# https://codeandlife.com/2012/07/03/benchmarking-raspberry-pi-gpio-speed
MIN_FREQ = 1
MAX_FREQ = 60

# Helper method to map an input value (v_in) between alternative max/min ranges.
def map_value(in_v, in_min, in_max, out_min, out_max):
    v = (in_v - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    if v < out_min:
        v = out_min
    elif v > out_max:
        v = out_max

    return v

if __name__ == '__main__':
    try:
        frequency = MIN_FREQ
        duty_cycle = MIN_DUTY_CYCLE

        # RPi.GPIO PWM instance.
        pwm = GPIO.PWM(LED_GPIO_PIN, frequency)
        pwm.start(duty_cycle) # Start software PWM on LED_GPIO_PIN

        while True:
            # Frequency value mapped from Analog Input Channel to RPi.GPIO expected range (capped at 60Hz per above comments).
            frequency = int(map_value(frequency_ch.voltage, MIN_A_IN_VOLTS, MAX_A_IN_VOLTS, MIN_FREQ, MAX_FREQ))

            # Duty Cycle value mapped from Analog Input Channel to RPi.GPIO expected range.
            duty_cycle = int(map_value(duty_cycle_ch.voltage, MIN_A_IN_VOLTS, MAX_A_IN_VOLTS, MIN_DUTY_CYCLE, MAX_DUTY_CYCLE))
            duty_cycle_percent = int((duty_cycle/MAX_DUTY_CYCLE) * 100)

            # Set Software PWM Duty Cycle and Frequency.
            # https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM
            pwm.ChangeDutyCycle(duty_cycle)
            pwm.ChangeFrequency(frequency)

            # Raw Analog input values.
            output1 = "Frequency Pot (A0) value={:>5} volts={:>5.3f}  Duty Cycle Pot (A1) value={:>5} volts={:>5.3f}".format(frequency_ch.value, frequency_ch.voltage, duty_cycle_ch.value, duty_cycle_ch.voltage)
            #print(output1)

            # Text for Terminal display output.
            output2 = "Frequency {:>5}Hz    Duty Cycle {:>3}%".format(frequency, duty_cycle_percent)
            print(output2)

            sleep(0.01)

    except KeyboardInterrupt:
      print("Bye")

      # Stop RPi.GPIO PWM.
      pwm.stop()

      # Revert GPIO to basic output and make LOW to turn LED off.
      GPIO.setup(LED_GPIO_PIN, GPIO.OUT)
      GPIO.output(LED_GPIO_PIN, GPIO.LOW)

      # RPi.GPIO cleanup.
      GPIO.cleanup()
