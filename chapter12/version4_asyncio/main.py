"""
File: chapter12/version4_asyncio/main.py

Asynchronous IO Example

Dependencies:
  pip3 install pigpio adafruit-circuitpython-ads1x15

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""
import adafruit_ads1x15.ads1115 as ADS
import pigpio

from time import sleep
import asyncio
import logging
import sys

# Our custom classes
from BUTTON import BUTTON
from POT import POT
from LED import LED

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Main")

pi = pigpio.pi()

# Button GPIO
BUTTON_GPIO = 21

def button_handler(the_button, state):
    """ Handles button event.
        Parameters:
          'the_button' is a reference to the BUTTON instance that invoked the callback (ie the button variable created below)
          'state' is the button state, eg PRESSED, RELEASED, HOLD """

    global led_index

    if state == BUTTON.PRESSED:
        led_index += 1

        if led_index >= len(LEDS):
            led_index = 0

        logger.info("Turning the Potentiometer dial will change the rate for LED #{}".format(led_index))

    if state == BUTTON.HOLD:
        rate = pot.get_value()
        logger.info("Changing rate for all LEDs to {}".format(rate))
        LED.set_rate_all(rate)


# Create BUTTON class instances and register button_handler() callback with it.
button = BUTTON(gpio=BUTTON_GPIO,
               pi=pi,
               callback=button_handler)



# Potentiometer / ADC settings (for POT Class)
POT_CHANNEL = ADS.P0    # P0 maps to output A1 on ADS1115
MIN_BLINK_RATE_SECS = 0 # Minimum value returnable by POT class
MAX_BLINK_RATE_SECS = 5 # Maximum value returnable by POT class


def pot_handler(the_pot, value):
    """ Handles potentiometer event
        Parameters:
          'the_pot' is a reference to the POT instance that invoked the callback (ie the pot variable created below)
          'value' is the mapped value (ie in the range MIN_BLINK_RATE_SECS..MAX_BLINK_RATE_SECS) """

    logger.debug(the_pot)
    logger.info("Changing LED #{} rate to {}".format(led_index, value))
    LEDS[led_index].set_rate(value)


# Create POT class instances and register pot_handler() callback with it.
pot = POT(analog_channel=POT_CHANNEL,
         min_value=MIN_BLINK_RATE_SECS,
         max_value=MAX_BLINK_RATE_SECS,
         callback=pot_handler)



# Create LED class instances.
LEDS = [
    LED(gpio=13, pi=pi),
    LED(gpio=19, pi=pi)
]


# The index of the LED in LEDS List which will be affected when the potentiometer value changes.
# 'led_index' is updated in button_handler() and referenced in pot_handler()
led_index = 0


if __name__ == "__main__":

    try:
        logger.info("Version 4 - Asynchronous IO Example. Press Control + C To Exit.")

        # Initialise all LEDs
        rate = pot.get_value()
        LED.set_rate_all(rate)  # Initialise all LEDS based on POT value.
        logger.info("Setting rate for all LEDs to {}".format(rate))

        logger.info("Turning the Potentiometer dial will change the rate for LED #{}".format(led_index))


        ##
        ## The Asynchronous IO Part...
        ##

        # Get (create) an event loop.
        loop = asyncio.get_event_loop()                                                  # (1)

        # Register the LEDs.
        for led in LEDS:
            loop.create_task(led.run())                                                  # (2)

        # Register Button and Pot
        loop.create_task(pot.run())                                                      # (3)
        loop.create_task(button.run())                                                   # (4)

        # Start the event loop.
        loop.run_forever()                                                               # (5)

    except KeyboardInterrupt:
        LED.set_rate_all(0) # Turn all LEDs off.
        pi.stop()
