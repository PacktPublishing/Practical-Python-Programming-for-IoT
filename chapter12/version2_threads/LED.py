"""
File: chapter12/version2_threads/LED.py

LED Class

Dependencies:
  pip3 install pigpio

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""
import pigpio
import threading
from time import sleep
import logging

logger = logging.getLogger('LED')

class LED:

    # A list of all LED instances that have been created.
    instances = []

    @classmethod                                                                         # (1)
    def set_rate_all(cls, rate):
        """ Set rate and synchronise all LEDs """

        # Turn off all LEDs.
        for led in cls.instances:
            led.set_rate(0)

        # Wait for all LEDs to be off.
        #
        # We do this so that when we start all the LEDs blinking again
        # they start at the same time (well very, very, very close to the same time)
        # and hence blink in unison.
        #
        # Note: We are "joining" each LED's thread to the
        # calling thread, which in this example is our main
        # thread (for main.py) used to start the program.
        for led in cls.instances:
            if led._thread:
                led._thread.join() # Wait for LED Thread to complete.                    # (2)


        # We do not get to this point in code until all
        # LED Threads are complete (and LEDs are all off)


        # Start LED's blinking
        for led in cls.instances:
            led.set_rate(rate)


    def __init__(self, gpio, pi, rate=0):
        """ Constructor """
        self.gpio = gpio
        self.pi = pi
        self.blink_rate_secs = rate
        self.is_blinking = False
        self._thread = None

        # Configure LED GPIO as Output and LOW (ie LED Off) by default.
        self.pi.set_mode(self.gpio, pigpio.OUTPUT)
        self.pi.write(self.gpio, pigpio.LOW) # Off by default.

        # Add this LED instance to the Class-level instances list/array.
        LED.instances.append(self)

        # Start LED blinking.
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


    def run(self):                                                                       # (3)
        """ Do the blinking (this is the run() method for our Thread) """

        while self.is_blinking:

            self.pi.write(self.gpio, not self.pi.read(self.gpio)) # Toggle LED
            logger.debug("LED on GPIO {} is {}".format(self.gpio, "On" if self.pi.read(self.gpio) else "Off"))

            # Works, but LED responsiveness to rate chances can be sluggish.
            # sleep(self.blink_rate_secs)

            # Better approach - LED responds to changes in near real-time.
            timer = 0
            while timer < self.blink_rate_secs:
                sleep(0.01)
                timer += 0.01

        # self.is_blinking has become False and the Thread ends.
        self._thread = None
        logger.debug("Blinking Thread Finished.")


    def set_rate(self, secs):
        """ Set LED blinking rate.
        A rate <= 0 will turn the LED off. """

        logger.debug("LED on GPIO {} is blinking at a rate of {} seconds.".format(self.gpio, secs))
        self.blink_rate_secs = secs

        if secs <= 0:
            self.is_blinking = False
            self.pi.write(self.gpio, pigpio.LOW) # LED Off

        elif not self._thread:
            self._start() # Start the LED blinking.


    def _start(self):
        """ Create and start Thread what will blink the LED. """

        if self._thread is not None:
            # Thread already exists.
            logger.warn("Blinking Thread already exists.")
            return


        self._thread = threading.Thread(name='LED on GPIO ' + str(self.gpio),
                                         target=self.run,
                                         daemon=True)

        self.is_blinking = True
        self._thread.start()
        logger.debug("Blinking Thread Started.")


if __name__ == '__main__':
    """ Run from command line to test the LED Class. Control + C to exit. """

    from signal import pause

    logging.basicConfig(level=logging.DEBUG)

    LED_GPIO = 13

    led = LED(gpio=LED_GPIO, pi=pigpio.pi(), rate=0)
    led.set_rate(1) # 1 second

    pause()
