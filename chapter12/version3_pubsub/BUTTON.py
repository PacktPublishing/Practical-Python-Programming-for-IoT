"""
File: chapter12/version3_pubsub/BUTTON.py

BUTTON Class

Dependencies:
  pip3 install pypubsub pigpio

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""
import pigpio
from time import sleep
import logging
from pubsub import pub

logger = logging.getLogger('BUTTON')

class BUTTON:

    # Button States. These are passed as a parameter to published messages.
    PRESSED  = "PRESSED"
    RELEASED = "RELEASED"
    HOLD     = "HOLD"

    # Root Topic. When you subscribe to a Root Topic you get all button messages from all instances.
    TOPIC_ROOT = "BUTTON"

    # Instance Topic, see
    # self.topic


    def __init__(self, gpio, pi, name, hold_secs=0.5):
        """ Constructor """
        self.pi = pi
        self.gpio = gpio
        self.name = name
        self.hold_secs = hold_secs

        # Setup Button GPIO as INPUT and enable internal Pull-Up Resistor.
        # Our button is therefore Active LOW.
        self.pi.set_mode(gpio, pigpio.INPUT)
        self.pi.set_pull_up_down(gpio, pigpio.PUD_UP)
        self.pi.set_glitch_filter(gpio, 10000) # microseconds debounce

        # Topic that is specific to this individual BUTTON Instance.
        self.topic = BUTTON.TOPIC_ROOT + "." + self.name

        self._hold_timer = 0  # For detecting hold events.
        self.pressed = False  # True when button pressed, false when released.
        self.hold = False     # Hold has been detected.

        # Register internal PiGPIO callback (as an alternative to polling the button in a while loop)
        self._pigpio_callback = self.pi.callback(self.gpio, pigpio.EITHER_EDGE, self._callback_handler)


    def __str__(self):
        """ To String """
        return "Button on GPIO {}: name={}, instance topic={}, pressed={}, hold={}".format(self.gpio, self.name, self.topic, self.pressed, self.hold)


    def _callback_handler(self, gpio, level, tick):
        """ PiGPIO Callback """

        if level == pigpio.LOW: # Active LOW
            # Button is pressed.
            self.pressed = True

            pub.sendMessage(self.topic, sender=self, name=self.name, state=BUTTON.PRESSED)

            # While button is pressed start a timer to detect if it remains pressed for self.hold_secs
            timer = 0
            while (timer < self.hold_secs) and not self.pi.read(self.gpio):
                sleep(0.01)
                timer += 0.01

            if not self.pi.read(self.gpio):  # Active LOW
                # Button is still pressed after self.hold_secs
                self.hold = True

                pub.sendMessage(self.topic, sender=self, name=self.name, state=BUTTON.HOLD)

        else: # level is HIGH
            # Button released
            self.pressed = False
            self.hold = False

            pub.sendMessage(self.topic, sender=self, name=self.name, state=BUTTON.RELEASED)


if __name__ == '__main__':
    """ Run from command line to test BUTTON Class. Control + C to exit. """

    from signal import pause

    logging.basicConfig(level=logging.DEBUG)

    BUTTON_GPIO = 21

    def on_button_message(sender, name, state, topic=pub.AUTO_TOPIC):
        print(sender)

    pub.subscribe(on_button_message, BUTTON.TOPIC_ROOT) # Root Topic means we get all button messages from all instances.

    button = BUTTON(gpio=BUTTON_GPIO,
                    hold_secs=0.5,
                    pi=pigpio.pi(),
                    name="MyButton")

    print("Press or Hold the Button")

    pause()