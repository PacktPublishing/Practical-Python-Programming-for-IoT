"""
File: chapter12/version3_pubsub/POT.py

Potentiometer Class

Dependencies:
  pip3 install pypubsub adafruit-circuitpython-ads1x15

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""
from time import sleep
import threading
import logging
import pigpio
# Below imports are part of Circuit Python and Blinka for ADS1115 ADC
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from pubsub import pub

logger = logging.getLogger('POT')

class POT:

    # Root Topic
    TOPIC_ROOT = "Potentiometer"

    # Instance Topic:
    # self.topic (see __init__)

    # Edge adjustments for the Potentiometer's full CW/CCW positions.
    # If you experience value issues when your Potentiometer it is rotated fully
    # clockwise or counter-clockwise, adjust these variables. Please see the
    # ADS1115 example in "Chapter 5 Connecting Your Raspberry Pi to the Physical World"
    #
    # You could consider making these constructor parameters.
    A_IN_EDGE_ADJ = 0.001
    MIN_A_IN_VOLTS = 0 + A_IN_EDGE_ADJ
    MAX_A_IN_VOLTS = 3.286 - A_IN_EDGE_ADJ


    def __init__(self, analog_channel, min_value, max_value, name, poll_secs=0.1):
        """ Constructor """

        self.name = name

        # Min and Max values returned by .get_value()
        self.min_value = min_value
        self.max_value = max_value

        # Create the I2C bus & ADS object.
        self.i2c = busio.I2C(board.SCL, board.SDA)
        ads = ADS.ADS1115(self.i2c)
        self.analog_channel = AnalogIn(ads, analog_channel)

        self.last_value = self.get_value() # Initialise last value.

        self.poll_secs = poll_secs
        self.is_polling = False

        self._thread = None
        self._start() # Start polling ADC

        # Topic that is specific to this individual POT Instance.
        self.topic = POT.TOPIC_ROOT + '.' + self.name


    def __str__(self):
        """ To String """
        return "Potentiometer with instance topic {} has mapped value of {}".format(self.topic, self.get_value())


    def run(self):
        """ Poll ADC for Voltage Changes """
        while self.is_polling:

            # Check if the Potentiometer has been adjusted.
            current_value = self.get_value()
            if self.last_value != current_value:
                logger.debug("Potentiometer with instance topic {} has mapped value of {}".format(self.topic, current_value))

                pub.sendMessage(self.topic, sender=self, name=self.name, value=current_value)

                self.last_value = current_value

            # Sleep
            timer = 0
            while timer < self.poll_secs:
                sleep(0.1)
                timer += 0.1


        self.__thread = None
        logger.debug("Potentiometer Polling Thread Finished.")


    def _start(self):
        """ Start Polling ADC """

        if self._thread is not None:
            # Thread already exists.
            logger.warn("Polling Thread Already Started.")
            return

        self.is_polling = True

        self._thread = threading.Thread(name='Potentiometer',
                                         target=self.run,
                                         daemon=True)
        self._thread.start()
        logger.debug("Potentiometer Polling Thread Started.")


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

    from signal import pause

    def on_pot_message(sender, name, value, topic=pub.AUTO_TOPIC):
        print(sender)

    pub.subscribe(on_pot_message, POT.TOPIC_ROOT) # Root Topic means we get all button messages from all instances.

    pot = POT(analog_channel=ADS.P0, # ADS.P0 -> A0
              min_value=0,
              max_value=5,
              poll_secs=0.1,
              name="MyPOT")

    pause()