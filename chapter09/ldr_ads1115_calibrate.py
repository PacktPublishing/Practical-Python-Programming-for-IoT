"""
File: chapter09/ldr_ads1115_calibrate.py

Measure maximum and minimum voltages using ADS1115 ADC

Dependencies:
  pip3 install adafruit-circuitpython-ads1x15

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""
from time import sleep

# Below imports are part of Circuit Python and Blinka
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus & ADS object.
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
analog_channel = AnalogIn(ads, ADS.P0)  #ADS.P0 --> A0


# Number of voltage readings to sample
SAMPLES = 100


# Write results to this file
OUTPUT_FILE = "ldr_calibration_config.py"


def sample(samples):
    """
    Read a number of voltage samples from ADS1115
    and return the average voltage
    """
    volts_sum = 0
    for c in range(SAMPLES):
        volts = analog_channel.voltage
        #print("Sample #{} = {:0.4f} volts".format(c, volts))
        volts_sum += volts
        sleep(0.01)

    return volts_sum / samples


if __name__ == '__main__':
    output  = "# This file was automatically created by " + __file__ + "\n"
    output += "# Number of samples: " + str(SAMPLES) + "\n"

    # Average minimum and maximum voltages
    min_volts = 0
    max_volts = 0

    try:
        input("Place LDR in the light and press Enter")
        print("Please wait...\n")
        max_volts = sample(SAMPLES)

        input("Place LDR in dark and press Enter")
        print("Please wait...\n")
        min_volts = sample(SAMPLES)

        output += ("MIN_VOLTS = {:0.4f}\n".format(min_volts))
        output += ("MAX_VOLTS = {:0.4f}\n".format(max_volts))

        with open(OUTPUT_FILE, "w") as f:
            f.write(output)

        print("File " + OUTPUT_FILE + " created with:\n")
        print(output)

    finally:
        i2c.deinit()
