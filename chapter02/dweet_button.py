"""
File: chapter02/dweet_button.py

A Python program to control an LED using the public dweet.io service
by using a Button to post a dweet.

Dependencies:
  pip3 install gpiozero pigpio requests

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""
import signal
import requests
import logging
from gpiozero import Device, Button
from gpiozero.pins.pigpio import PiGPIOFactory

# Initialize Logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger('main')
logger.setLevel(logging.INFO)

# Initialise GPIOZero
Device.pin_factory = PiGPIOFactory()

BUTTON_GPIO_PIN = 23
button = None
LED_STATES = ['off', 'on', 'blink']
current_led_state = 0 # off

# Make sure thing_name matches the "dweet_led thing" you want to control.
thing_name = '**** ADD YOUR THING NAME HERE ****'
URL = 'https://dweet.io'


def init_button():
    """Setup button"""
    global button
    button = Button(BUTTON_GPIO_PIN, pull_up=True, bounce_time=0.1)
    button.when_pressed = button_pressed


def button_pressed():
    """Button pressed handler"""
    cycle_led_state()


def cycle_led_state():
    """Send revolving dweet to change LED from off -> on -> blink -> off -> ..."""
    global current_led_state
    current_led_state += 1

    if current_led_state >= len(LED_STATES):
        current_led_state = 0

    state = LED_STATES[current_led_state]

    logger.info('Setting LED state %s', state)
    send_dweet(thing_name, {'state': state})


def send_dweet(thing_name, values):
    """Send a dweet to a thing."""

    resource = URL + '/dweet/for/' + thing_name
    logger.debug('Dweeting to url %s with values %s', resource, values)

    r = requests.get(resource, params=values)

    if r.status_code == 200:
        dweet_response = r.json()
        logger.debug('Dweet response was %s', dweet_response)
        return dweet_response

    else:
        logger.error('Dweeting dweet failed with http status %s', r.status_code)
        return {}


# Initialise Module
init_button()


# Main entry point
if __name__ == '__main__':
    # You could adopt the get_last_dweet() / process_dweet() from dweet_listner.py
    # to initialise the led state in this file. For simplicity we're just
    # starting with 'Off' (current_led_state = 0)

    print("Press button to send a dweet to turn LED on, blink or off.")

    # Stop Python from exiting.
    signal.pause()