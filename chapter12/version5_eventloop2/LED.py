"""
File: chapter12/version5_eventloop2/LED.py

LED Class

Dependencies:
  pip3 install pigpio

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""
import pigpio
import threading
from time import time, sleep
import logging

logger = logging.getLogger('LED')

class LED:

    # A list of all LED instances that have been created.
    instances = []

    @classmethod
    def set_rate_all(cls, rate):
        """ Set rate and synchronise all LEDs """

        # Tuen all LED's Off
        for i in LED.instances:
            i.set_rate(0)

        # Start LED's blinking
        for i in LED.instances:
            i.set_rate(rate)


    def __init__(self, gpio, pi, rate=0):
        """ Constructor """
        self.pi = pi
        self.gpio = gpio
        self.blink_rate_secs = 0

        # Configure LED GPIO as Output and LOW (ie LED Off) by default.
        # self.pi.set_mode(self.gpio, pigpio.OUTPUT)
        self.pi.write(self.gpio, pigpio.LOW) # Off by default.

        self.toggle_at = 0 # time when we will toggle the LED On/Off. <=0 means LED is off.

        # Add this LED instance to the Class-level instances list/array.
        LED.instances.append(self)

        # Start LED blinking (Note it will not start blinking until .run() has been registered with an event-loop!)
        self.set_rate(rate)


    def __del__(self):
        """ Destructor """
        self.instances.remove(self)


    def __str__(self):
        """ To String """
        if self.is_blinking:
            return "LED on GPIO {} is blinking at a rate of {} seconds".format(self.gpio, self.blink_rate_secs)
        else:
            return "LED on GPIO {} is Off".format(self.gpio)


    def run(self):
        """ Do the blinking """

        while True:

            if self.toggle_at > 0 and (time() >= self.toggle_at):

                self.pi.write(self.gpio, not self.pi.read(self.gpio)) # Toggle LED
                self.toggle_at += self.blink_rate_secs

                logger.debug("LED on GPIO {} is {}".format(self.gpio, "On" if self.pi.read(self.gpio) else "Off"))

            sleep(0)


    def set_rate(self, secs):
        """ Set LED blinking rate.
        A rate <= 0 will turn the LED off. """

        logger.debug("LED on GPIO {} is blinking at a rate of {} seconds.".format(self.gpio, secs))
        self.blink_rate_secs = secs

        if secs <= 0:
            self.toggle_at = 0
            self.pi.write(self.gpio, pigpio.LOW) # LED Off

        else:
            self.toggle_at = time() + self.blink_rate_secs
            self.pi.write(self.gpio, pigpio.HIGH) # LED On

