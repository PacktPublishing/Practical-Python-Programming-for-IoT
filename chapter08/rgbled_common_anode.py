"""
File: chapter08/RGBLED_Common_Anode.py

Control a Common Anode RGBLED with PWM.

Dependencies:
  pip3 install pigpio Pillow

Built and tested with Python 3.7 on Raspberry Pi 4 Model B

## A Note On Color Models and Formats.

The functions in this file that take a 'color' parameter or list can handle the following
formats thanks to the PIL method getrgb() (non exhaustive):
 - A common word: red, green or blue.
 - A HEX value: #FF0000
 - A HEX value with Alpha: #FF0000CC
 - RGB Integer tuple: (255, 0, 0)
 - RGB Integer tuple with Alpha (255, 0, 0, 128)
See this link for more information and additional formats: https://pillow.readthedocs.io/en/latest/reference/ImageColor.html#module-PIL.ImageColor
"""

from PIL.ImageColor import getrgb                     # (1)
from time import sleep
import pigpio

# Common Anode connected to +3.3V Pin,
# Color legs to the following GPIOs.
GPIO_RED   = 16
GPIO_GREEN = 20
GPIO_BLUE  = 21

pi = pigpio.pi()

pi.set_PWM_range(GPIO_RED, 255)                       # (2)
pi.set_PWM_range(GPIO_GREEN, 255)
pi.set_PWM_range(GPIO_BLUE, 255)
pi.set_PWM_frequency(GPIO_RED, 8000)
pi.set_PWM_frequency(GPIO_GREEN, 8000)
pi.set_PWM_frequency(GPIO_BLUE, 8000)

def set_color(color):                                 # (3)
    """
    Set REG LED Color.
    """
    rgb = getrgb(color)                               # (4)

    print("LED is {} ({})".format(color, rgb))

    pi.set_PWM_dutycycle(GPIO_RED, 255-rgb[0])        # (5)       <<<< DIFFERENCE
    pi.set_PWM_dutycycle(GPIO_GREEN, 255-rgb[1])      #           <<<< DIFFERENCE
    pi.set_PWM_dutycycle(GPIO_BLUE, 255-rgb[2])       #           <<<< DIFFERENCE


def cycle_colors(colors=("red", "green", "blue"), delay_secs=1):   # (6)
    """
    Cycle RGB LED through a list of colors.
    """

    for c in colors:
        set_color(c)
        sleep(delay_secs)


def rainbow_example(loops=1, delay_secs=0.01):                     # (7)
    """
    Cycle RGB LED through a range of colors.
    """
    saturation = 100  # 0 (grayer) to 100 (full color)
    brightness = 100  # 0 (darker) to 100 (brighter)

    for i in range(0, loops):
        for hue in tuple(range(0, 360)) + tuple(range(360, -1, -1)):  # 0..360..0
            color_str = "hsb({}, {}%, {}%)".format(hue, saturation, brightness)
            rgb = getrgb(color_str)
            pi.set_PWM_dutycycle(GPIO_RED, 255-rgb[0])              # <<<< DIFFERENCE
            pi.set_PWM_dutycycle(GPIO_GREEN, 255-rgb[1])            # <<<< DIFFERENCE
            pi.set_PWM_dutycycle(GPIO_BLUE, 255-rgb[2])             # <<<< DIFFERENCE
            sleep(delay_secs)

try:
    cycle_colors()
    sleep(1)
    rainbow_example()
    sleep(1)

except KeyboardInterrupt:
    print("Bye")

finally:
    # Turn of LEDs and PiGPIO cleanup.
    set_color("black")  # All LED's will be duty cycle 0, hence off.
    pi.stop()

