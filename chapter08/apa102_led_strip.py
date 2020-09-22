"""
File: chapter08/APA102_LED_Strip.py

Control a APA102 LED Strip.

Dependencies:
  pip3 install luma.led_matrix

If luma.led_matrix fails to install see it's documentation for dependencies what you may need to install first:
https://luma-led-matrix.readthedocs.io/en/latest/install.html#installing-from-pypi

Built and tested with Python 3.7 on Raspberry Pi 4 Model B

## A Note On Color Models and Formats.
The functions in this file that take a 'color' parameter or list can handle the following
formats thanks to the PIL method getrgb() used by Luma (non exhaustive):
 - A common word: red, green or blue.
 - A HEX value: #FF0000
 - A HEX value with Alpha: #FF0000CC
 - RGB Integer tuple: (255, 0, 0)
 - RGB Integer tuple with Alpha (255, 0, 0, 128)
See this link for more information and additional formats: https://pillow.readthedocs.io/en/latest/reference/ImageColor.html#module-PIL.ImageColor
"""
from math import ceil
from time import sleep
from collections import deque                                                           # (1)
from PIL.ImageColor import getrgb
from luma.core.render import canvas
from luma.led_matrix.device import apa102
from luma.core.interface.serial import spi, bitbang


# Number of LED's in your APA102 LED Strip.
NUM_LEDS = 60                                                                           # (2)


# Color buffer "array", initialised to all black.
# The color values in this buffer are applied to the APA102 LED Strip
# by the update() function. The value at position 0 = the LED first LED
# in the strip.
color_buffer = deque(['black']*NUM_LEDS, maxlen=NUM_LEDS)                               # (3)


# Initialise serial using Hardware SPI0 (SCLK=BCM 11, MOSI/SDA=BCM 10).
# Default bus_speed_hz=8000000. This value may need to be lowered
# if your Logic Level Converter cannot switch fast enough.
# Allowed values are 500000, 1000000, 2000000, 4000000, 8000000, 16000000, 32000000
# For find the spi class at https://github.com/rm-hull/luma.core/blob/master/luma/core/interface/serial.py
serial = spi(port=0, device=0, bus_speed_hz=2000000)                                   # (4)


# Initialise serial using "Big Banging" SPI technique on general GPIO Pins.
# For find the bitbang class at https://github.com/rm-hull/luma.core/blob/master/luma/core/interface/serial.py
# serial = bitbang(SCLK=13, SDA=6)                                                     # (5)


#Initialise APA102 device instance using serial instance created above.
device = apa102(serial_interface=serial, cascaded=NUM_LEDS)                            # (6)


# Reset device and set it's global contrast level.
device.clear()                                                                         # (7)
contrast_level = 128 # 0 (off) to 255 (maximum brightness)
device.contrast(contrast_level)

def set_color(color='black', index=-1):                                                # (8)
    """
    Set the color of single LED (index >= 0), or all LEDs (when index == -1)
    """
    if index == -1:
        global color_buffer
        color_buffer = deque([color]*NUM_LEDS, maxlen=NUM_LEDS)
    else:
        color_buffer[index] = color


def push_color(color):                                                                  # (9)
    """
    Push a new color into the color array at index 0. The last value is dropped.
    """
    color_buffer.appendleft(color)


def set_pattern(colors=('green', 'blue', 'red')):                                       # (10)
    """
    Fill the color buffer with a repeating color pattern.
    """
    for i in range(0, int(ceil(float(NUM_LEDS)/float(len(colors))))):
        for color in colors:
            push_color(color)


def rotate_colors(count=1):                                                             # (11)
    """
    Rotate colors in the buffer count times.
    """
    color_buffer.rotate(count)


def update():                                                                           # (12)
    """
    Apply the color buffer to the APA102 strip.
    """
    with canvas(device) as draw:
        for led_pos in range(0, len(color_buffer)):
            color = color_buffer[led_pos]

            ## If your LED strip's colors are are not in the expected
            ## order, uncomment the following lines and adjust the indexes
            ## in the line color = (rgb[0], rgb[1], rgb[2])
            # rgb = getrgb(color)
            # color = (rgb[0], rgb[1], rgb[2])
            # if len(rgb) == 4:
            #     color += (rgb[3],)  # Add in Alpha

            draw.point((led_pos, 0), fill=color)


#
# LED sequence examples
#

def cycle_colors(colors=("red", "green", "blue"), delay_secs=1):
    """
    Cycle a set of colours.
    """
    set_color('black') # Start with all LED's "off"

    for c in colors:
        print("LEDs are all " + c)
        set_color(c)
        update()
        sleep(delay_secs)


def pattern_example(delay_secs=3):
    """
    Pattern examples.
    """
    set_color('black') # Start with all LED's "off"
    update()

    set_pattern(colors=("red", "green", "blue"))
    update()
    sleep(delay_secs)

    set_pattern(colors=("purple", "yellow"))
    update()


def rotate_example(colors=("red", "green", "blue"), rounds=2, delay_secs=0.02):
    """
    A simple LED 'chaser' animation.
    """
    set_color('black') # Start with all LED's "off"

    for c in colors:
        push_color(c)

    for i in range(0, rounds):

      for j in range(0, NUM_LEDS - len(colors)):
        rotate_colors()
        update()
        sleep(delay_secs)

      for j in range(0, NUM_LEDS - len(colors)):
        rotate_colors(-1)
        update()
        sleep(delay_secs)


def rainbow_example(rounds=1, delay_secs=0.01):
    """
    Rainbow sequence animation example.
    """
    set_color('black') # Start with all LED's "off"
    update()

    saturation = 100 # 0 (grayer) to 100 (full color)
    brightness = 100 # 0 (darker) to 100 (brighter)

    for i in range(0, rounds):
        for hue in tuple(range(0, 360)) + tuple(range(360, -1, -1)): # 0..360..0
            color_str = "hsb({}, {}%, {}%)".format(hue, saturation, brightness)
            push_color(color_str)
            update()
            sleep(delay_secs)

#
# Run Examples
#
try:
    print("Color Cycle")
    cycle_colors()
    sleep(1)

    print("Pattern Example")
    pattern_example()
    sleep(1)

    print("Rotate Example")
    rotate_example(colors=("red", "green", "blue"), rounds=2, delay_secs=0.02)
    sleep(1)

    print("Rainbow Example")
    rainbow_example(rounds=1, delay_secs=0.01)
    sleep(1)

except KeyboardInterrupt:
    print("Bye")

finally:
    # Cleanup
    set_color("black") # All LED's "Off"
    device.clear()

