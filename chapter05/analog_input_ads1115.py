"""
File: chapter05/analog_input_ads1115.py

Read analog input from an ADS1115 ADC I2C module.

Dependencies:
  pip3 install pigpio adafruit-circuitpython-ads1x15

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""
from time import sleep

# Below imports are part of Circuit Python and Blinka
import board                                                                           # (1)
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus & ADS object.
i2c = busio.I2C(board.SCL, board.SDA)                                                  # (2)
ads = ADS.ADS1115(i2c)

# The max/min range we get from our Analog Inputs on the ADS1115.
# Max value derived by observation. See print(output1) in while loop.
# A_IN_EDGE_ADJ is an edge adjustment factor
# for MIN_A_IN_VOLTS and MAN_A_IN_VOLTS
A_IN_EDGE_ADJ = 0.002                                                                  # (3)
MIN_A_IN_VOLTS = 0 + A_IN_EDGE_ADJ
MAX_A_IN_VOLTS = 3.3 - A_IN_EDGE_ADJ

# Analog Inputs on Channels 0 and 1 (A0 and A1 on breakout board)
frequency_ch = AnalogIn(ads, ADS.P0)  #ADS.P0 --> A0                                   # (4)
duty_cycle_ch = AnalogIn(ads, ADS.P1) #ADS.P1 --> A1

if __name__ == '__main__':
    try:
        while True:
            output = ("Frequency Pot (A0) value={:>5} volts={:>5.3f} "
                      "Duty Cycle Pot (A1) value={:>5} volts={:>5.3f}")
            output = output.format(frequency_ch.value, frequency_ch.voltage,           # (5)
                                   duty_cycle_ch.value, duty_cycle_ch.voltage)

            print(output)
            sleep(0.05)

    except KeyboardInterrupt:
        i2c.deinit()                                                                   # (6)