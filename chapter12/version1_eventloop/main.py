"""
File: chapter12/version1_eventloop/main.py

Event Loop Example

Dependencies:
  pip3 install pigpio adafruit-circuitpython-ads1x15

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""
import pigpio
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from time import sleep, time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Main")

pi = pigpio.pi()


#
# Setup LEDs
#

# Maximum and minimum "blinking" rates for the LEDs. These values will be the
# mapped values returned by our Potentiometer.
MIN_RATE = 0.1 # Seconds
MAX_RATE = 5   # Seconds

# GPIO's that our LEDs are connected to.
LED_GPIOS = [13, 19]

# Configure LED GPIOs as OUTPUT and turn LEDs off.
for gpio in LED_GPIOS:
    pi.set_mode(gpio, pigpio.OUTPUT)
    pi.write(gpio, pigpio.LOW) # LED Off

# Variables to manage LEDs and their blinking.
led_index = 0
led_rates = [0, 0, 0]
led_toggle_at_time = [0, 0, 0]


#
# Setup Button
#
BUTTON_GPIO = 21
BUTTON_HOLD_SECS = 0.5

# Button GPIO is configured as INPUT with an internal pull-up resistor enabled,
# thus the button will be Active LOW.
pi.set_mode(BUTTON_GPIO, pigpio.INPUT)
pi.set_pull_up_down(BUTTON_GPIO, pigpio.PUD_UP)
pi.set_glitch_filter(BUTTON_GPIO, 10000) # microseconds debounce



#
# Setup Potentiometer (connected via ADSlll5 ADC Module)
#
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
pot_channel = AnalogIn(ads, ADS.P0)


# Edge adjustments for the Potentiometer's full CW/CCW positions.
# If you experience value issues when your Potentiometer it is rotated fully
# clockwise or counter-clockwise, adjust these variables. Please see the
# ADS1115 example in "Chapter 5 Connecting Your Raspberry Pi to the Physical World"
# form more information.
A_IN_EDGE_ADJ = 0.001
MIN_A_IN_VOLTS = 0 + A_IN_EDGE_ADJ
MAX_A_IN_VOLTS = 3.286 - A_IN_EDGE_ADJ


def map_value(in_v, in_min, in_max, out_min, out_max):
    """Helper method to map an input value (v_in)
    between alternative max/min ranges."""
    v = (in_v - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    return max(min(out_max, v), out_min)


if __name__ == "__main__":

    SLEEP_DELAY = 0.01

    try:
        logger.info("Version 1 - Event Loop Example. Press Control + C To Exit.")

        # Get initial 'voltage' value from Potentiometer/ADC and map into a blinking 'rate'
        voltage = pot_channel.voltage
        rate = round(map_value(voltage, MIN_A_IN_VOLTS, MAX_A_IN_VOLTS, MIN_RATE, MAX_RATE), 1)

        # Initialise all LEDs
        led_rates = [rate] * len(led_rates) # Initialise blink rate to match POT value.
        logger.info("Setting rate for all LEDs to {}".format(rate))

        # State variables.
        last_rate = rate
        last_led_index = 0
        was_pressed = False
        button_held = False
        button_pressed = False
        button_hold_timer = 0

        logger.info("Turning the Potentiometer dial will change the rate for LED #{}".format(last_led_index))

        #
        # Start of "Event Loop"
        #
        while True:                                                                           # (1)
            #
            # Check if the button is pressed or held down.
            #
            button_pressed = pi.read(BUTTON_GPIO) == pigpio.LOW # Button is Active LOW.       # (2)

            if button_pressed and not button_held:
                # Button has been pressed.
                button_hold_timer += SLEEP_DELAY
                was_pressed = True

            elif not button_pressed:

                if was_pressed and not button_held:
                    # Button has been released

                    # Update 'led_index' so that Potentiometer adjustments affect the next LED.
                    led_index += 1
                    if led_index >= len(LED_GPIOS):
                        led_index = 0

                    if led_index != last_led_index:
                        logger.info("Turning the Potentiometer dial will change the rate for LED #{}".format(led_index))
                        last_led_index = led_index

                button_held = False
                button_hold_timer = 0
                was_pressed = False

            if button_hold_timer >= BUTTON_HOLD_SECS and not button_held:
                # Button has been held down

                # Set all LEDs to same rate
                logger.info("Changing rate for all LEDs to {}".format(rate))
                led_rates = [rate] * len(led_rates)
                led_toggle_at_time = [0] * len(led_rates)

                for gpio in LED_GPIOS:
                    # Turn all LEDs off so that when they start blinking (below) are all synchronised.
                    pi.write(gpio, pigpio.LOW)

                button_hold_timer = 0
                button_held = True

            #
            # Check if the Potentiometer dial been turned.
            #
            voltage = pot_channel.voltage
            rate = round(map_value(voltage, MIN_A_IN_VOLTS, MAX_A_IN_VOLTS, MIN_RATE, MAX_RATE), 1)

            if rate != last_rate:
                # Set individual LED (at led_index) to new blinking rate
                logger.info("Changing LED #{} rate to {}".format(led_index, rate))
                led_rates[led_index] = rate
                last_rate = rate

            #
            # Blink the LEDs.
            #
            now = time()                                                                      # (3)
            for i in range(len(LED_GPIOS)):
                if led_rates[i] <= 0:
                    pi.write(LED_GPIOS[i], pigpio.LOW) # LED Off.
                elif now >= led_toggle_at_time[i]:
                    pi.write(LED_GPIOS[i], not pi.read(LED_GPIOS[i])) # Toggle LED
                    led_toggle_at_time[i] = now + led_rates[i]

            logger.debug("Sleep...")
            sleep(SLEEP_DELAY)

    except KeyboardInterrupt:

        # Turn all LEDs off.
        for gpio in LED_GPIOS:
            pi.write(gpio, pigpio.LOW)

        pi.stop()
