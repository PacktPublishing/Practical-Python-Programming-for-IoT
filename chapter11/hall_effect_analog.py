"""
File: chapter11/hall_effect_analog.py

Hall-Effect Sensor Example - Ratiometric Type
Tested with AH3505 Hall-Effect Sensor

Dependencies:
  pip3 install pigpio adafruit-circuitpython-ads1x15

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""
from time import sleep
import pigpio

# Below imports are part of Circuit Python and Blinka
import board                                                      
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

pi = pigpio.pi()

# Create the I2C bus & ADS object.
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
analog_channel_A0 = AnalogIn(ads, ADS.P0)  # ADS.P0 --> A0 

if __name__ == '__main__':
      
    try:
        while True:
            output = "Volts={:>5.3f}, Value={}".format(analog_channel_A0.voltage, analog_channel_A0.value)
            print(output)
            sleep(0.05)

    except KeyboardInterrupt:
        i2c.deinit()                                                          
        pi.stop()
