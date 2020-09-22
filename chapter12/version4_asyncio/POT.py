"""
File: chapter12/version4_asyncio/POT.py

Potentiometer Class

Dependencies:
  pip3 install adafruit-circuitpython-ads1x15

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""
from time import sleep
import logging
import pigpio
# Below imports are part of Circuit Python and Blinka for ADS1115 ADC
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import asyncio

logger = logging.getLogger('POT')

class POT:

    # Edge adjustments for the Potentiometer's full CW/CCW positions.
    # If you experience value issues when your Potentiometer it is rotated fully
    # clockwise or counter-clockwise, adjust these variables. Please see the
    # ADS1115 example in "Chapter 5 Connecting Your Raspberry Pi to the Physical World"
    #
    # You could consider making these constructor parameters.
    A_IN_EDGE_ADJ = 0.001
    MIN_A_IN_VOLTS = 0 + A_IN_EDGE_ADJ
    MAX_A_IN_VOLTS = 3.286 - A_IN_EDGE_ADJ

    def __init__(self, analog_channel, min_value, max_value, callback=None):
        """ Constructor """

        # Min and Max values returned by .get_value()
        self.min_value = min_value
        self.max_value = max_value

        self.callback = callback

        # Create the I2C bus & ADS object.
        self.i2c = busio.I2C(board.SCL, board.SDA)
        ads = ADS.ADS1115(self.i2c)
        self.analog_channel = AnalogIn(ads, analog_channel)

        self.last_value = self.get_value()


    def __str__(self):
        """ To String """
        return "Potentiometer mapped value is {}".format(self.get_value())


    async def run(self):
        """ Poll ADC for Voltage Changes """

        while True:

            # Check if the Potentiometer has been adjusted.
            current_value = self.get_value()
            if self.last_value != current_value:

                logger.debug("Potentiometer mapped value is {}".format(current_value))

                if self.callback:
                    self.callback(self, current_value)

                self.last_value = current_value

            await asyncio.sleep(0)


    def _map_value(self, in_v):
        """ Helper method to map an input value (v_in) between alternative max/min ranges. """
        v = (in_v - self.MIN_A_IN_VOLTS) * (self.max_value - self.min_value) / (self.MAX_A_IN_VOLTS - self.MIN_A_IN_VOLTS) + self.min_value
        return max(min(self.max_value, v), self.min_value)


    def get_value(self):
        """ Get current value """
        try:
            voltage = self.analog_channel.voltage     # Raw analog voltage
            return round(self._map_value(voltage), 1) # Mapped to min_value/max_value range
        except OSError as e:
            # Lost communication with ADC via I2C
            logger.error(e, exc_info=True)
            return self.last_value


if __name__ == '__main__':
    """ Run from command line to test POT Class. Control + C to exit. """

    logging.basicConfig(level=logging.DEBUG)

    def pot_handler(the_pot, value):
        print(the_pot)

    pot = POT(analog_channel=ADS.P0,  # ADS.P0 -> A0
              min_value=0,
              max_value=5,
              callback=pot_handler)

    loop = asyncio.get_event_loop()
    loop.create_task(pot.run())
    loop.run_forever()
