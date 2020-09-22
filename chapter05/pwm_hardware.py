"""
File: chapter05/pwm_hardware.py

PWM demo using hardware PWM and a LED.

Dependencies:
  pip3 pigpio adafruit-circuitpython-ads1x15

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""
from time import sleep
import pigpio


# Below imports are part of Circuit Python and Blinka
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


# PiGPIO Instance
pi = pigpio.pi()


# We're using Hardware PWM. Raspberry Pi 3 & 4 have
# 2 PWM hardware channels labeled PWM0 (GPIO Pins 12 or 18)
# and PWM1 (GPIO Pins 13 or 19). Any other pin numbers
# will result in a PiGPIO exception when
# pi.hardware_PWM() is called later.
LED_GPIO_PIN = 12


# Ensure we start with LED off.
pi.set_mode(LED_GPIO_PIN, pigpio.OUTPUT)
pi.write(LED_GPIO_PIN, pigpio.LOW)


# Create the I2C bus & ADS object.
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)


# Analog Inputs on Channels 0 and 1 (A0 and A1 on breakout board)
frequency_ch = AnalogIn(ads, ADS.P0)
duty_cycle_ch = AnalogIn(ads, ADS.P1)


# The max/min range we get from our Analog Inputs on the ADS1115.
# Max value derived by observation. See print(output1) in while loop.
A_IN_EDGE_ADJ = 0.002 # Edge adjustment factor for MIN_A_IN_VOLTS and MAN_A_IN_VOLTS
MIN_A_IN_VOLTS = 0 + A_IN_EDGE_ADJ
MAX_A_IN_VOLTS = 3.3 - A_IN_EDGE_ADJ


# Max/Min Duty Cycle value as per PiGPIO documentation
# for hardware_PWM()
MIN_DUTY_CYCLE = 0                                                                            # (1)
MAX_DUTY_CYCLE = 1000000


# Max/Min Frequency value as per PiGPIO documentation
# for hardware_PWM() is 0 to 125 million hertz, but we're
# capping it at 60 hertz for LED visual and piscope demonstration.
MIN_FREQ = 0          #(2)
MAX_FREQ = 60 # max 125000000


def map_value(in_v, in_min, in_max, out_min, out_max):                                        # (3)
    """Helper method to map an input value (v_in)
    between alternative max/min ranges."""

    v = (in_v - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    if v < out_min: v = out_min
    elif v > out_max: v = out_max
    return v


if __name__ == '__main__':
    try:
        while True:
            # Frequency value mapped from Analog Input Channel
            # to PiGPIO expected range
            # (capped at 60Hz per above comments).
            frequency = int(map_value(frequency_ch.voltage,                                   # (4)
                                      MIN_A_IN_VOLTS, MAX_A_IN_VOLTS,
                                      MIN_FREQ, MAX_FREQ))

            # Duty Cycle value mapped from Analog Input
            # Channel to PiGPIO expected range.
            duty_cycle = int(map_value(duty_cycle_ch.voltage,                                 # (5)
                                       MIN_A_IN_VOLTS, MAX_A_IN_VOLTS,
                                       MIN_DUTY_CYCLE, MAX_DUTY_CYCLE))

            duty_cycle_percent = int((duty_cycle/MAX_DUTY_CYCLE) * 100)

            # Set Hardware PWM Duty Cycle and Frequency.
            # http://abyz.me.uk/rpi/pigpio/python.html#hardware_PWM
            pi.hardware_PWM(LED_GPIO_PIN, frequency, duty_cycle)                              # (6)

            # Raw Analog values.
            output1 = ("Frequency Pot (A0) value={:>5} volts={:>5.3f} "
                      "Duty Cycle Pot (A1) value={:>5} volts={:>5.3f}")
            output1 = output1.format(frequency_ch.value, frequency_ch.voltage, \
                                   duty_cycle_ch.value, duty_cycle_ch.voltage)
            #print(output1)


            # Value mapped and formatted output.
            output2 = "Frequency {:>5}Hz    Duty Cycle {:>3}%" \
                      .format(frequency, duty_cycle_percent)

            print(output2)

            sleep(0.05)

    except KeyboardInterrupt:
      i2c.deinit()

      # Revert GPIO to basic output and make LOW to turn LED off.
      pi.set_mode(LED_GPIO_PIN, pigpio.OUTPUT)
      pi.write(LED_GPIO_PIN, pigpio.LOW)

      # PiGPIO cleanup.
      pi.stop()
