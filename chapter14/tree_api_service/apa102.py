"""
File: chapter14/tree_api_service/apa102.py

Hardware Interface Layer to APA102 LED Strip.

Built and tested with Python 3.7 on Raspberry Pi 4 Model B

Dependencies:
  pip3 install luma.led_matrix
"""
from math import ceil
from time import sleep
import threading
import logging
from collections import deque
from PIL.ImageColor import getrgb
from luma.core.render import canvas
from luma.led_matrix.device import apa102
from luma.core.interface.serial import spi, bitbang

logger = logging.getLogger('APA102')

class APA102:

    # Strip modes. Used in run() to create animations.
    MODE_NOT_ANIMATING = 0  # Eg LEDs are a static color
    MODE_ROTATE_LEFT = 2
    MODE_ROTATE_RIGHT = 3
    MODE_BLINK = 4
    MODE_RAINBOW = 5

    def __init__(self, num_leds, port=0, device=0, bus_speed_hz=2000000):
        """
        Constructor
        """

        self.num_leds = num_leds  # Number of LED's in your APA102 LED Strip.

        # Initialise serial using Hardware SPI0 (SCLK=BCM 11, MOSI/SDA=BCM 10).
        # Default bus_speed_hz=8000000. This value may need to be lowered
        # if your Logic Level Converter cannot switch fast enough.
        # Allowed vales are 500000 ,1000000, 2000000, 4000000, 8000000, 16000000, 32000000
        # For find the spi class at https://github.com/rm-hull/luma.core/blob/master/luma/core/interface/serial.py
        self.serial = spi(port=port, device=device, bus_speed_hz=bus_speed_hz)

        # Initialise serial using "Big Banging" SPI technique on general GPIO Pins.
        # For find the bitbang class at https://github.com/rm-hull/luma.core/blob/master/luma/core/interface/serial.py
        # self.serial = bitbang(SCLK=13, SDA=6)

        # Color buffer "array", initialised to all black.
        # The color values in this buffer are applied to the APA102 LED Strip
        # by the update() function. The value at position 0 = the LED first LED
        # in the strip.
        self.color_buffer = deque([None] * self.num_leds, maxlen=self.num_leds)

        # Initialise APA102 device instance using serial instance created above.
        self.device = apa102(serial_interface=self.serial, cascaded=self.num_leds)

        # Reset device and set it's global contrast level.
        self.clear()
        self.set_contrast(128)
        self._last_contrast = 0 # Used in _blink()
        self._blink_buffer = None # used in _blink()
        self._blink_index = 0  # used in _blink()

        self._thread = None
        self.mode = APA102.MODE_NOT_ANIMATING

        self.animation_speed = 5 #see set_animation_speed()
        self.animation_delay_secs = 0.5  #see set_animation_speed()


    def start_animation(self):
        """
        Start Animation Thread
        """

        if self._thread is not None:
            # Thread already exists.
            return

        self._thread = threading.Thread(name='APA102',
                                         target=self.run,
                                         daemon=True)
        self._thread.start()


    def stop_animation(self):
        """
        Stop Animation Thread
        """

        self._thread = None
        self.mode = APA102.MODE_NOT_ANIMATING


    def is_animating(self):
        """
        Test if LEDs are animating
        """

        return self._thread is not None


    def run(self):
        """
        Animate LEDs
        """

        while self.is_animating() and self.mode > APA102.MODE_NOT_ANIMATING:
            if self.mode == APA102.MODE_RAINBOW:
                self._rainbow()
            if self.mode == APA102.MODE_ROTATE_LEFT:
                self._rotate_colors(1)
            elif self.mode == APA102.MODE_ROTATE_RIGHT:
                self._rotate_colors(-1)
            elif self.mode == APA102.MODE_BLINK:
                self._blink()

            self._update()

            timer = 0
            while self.is_animating() and timer < self.animation_delay_secs:
                timer += 0.01
                sleep(0.01)

            self.set_contrast(self.contrast) # Restore contrast (in case we were in a blinking animation and it ended with an Off blink state).

    def is_valid_color(self, color):
        """
        Test if param color is a valid color that is compatible with Pillow getrgb()
        Valid colors include names like red, blue, green that are recognised by getrgb(),
        and hex values like #44FC313.
        For full details on supported color formats, see
        https://pillow.readthedocs.io/en/latest/reference/ImageColor.html#module-PIL.ImageColor
        """

        try:
            getrgb(color)
            return True
        except ValueError:
            return False

    def set_animation_speed(self, speed):
        """
        Set animation speed between 1 to 10.
        Speed is converted into a second delay
        used in the Thread loop.
        """

        if speed >= 1 and speed <= 10:
            self.animation_speed = speed
            self.animation_delay_secs = ((11-speed)/10)


    def rotate_left(self):
        """
        Start LED left rotation animation
        """

        self.mode = APA102.MODE_ROTATE_LEFT
        self.start_animation()


    def rotate_right(self):
        """
        Start LED right rotation animation
        """

        self.mode = APA102.MODE_ROTATE_RIGHT
        self.start_animation()


    def rainbow(self):
        """
        Start LED rainbow animation
        """

        self.mode = APA102.MODE_RAINBOW
        self.start_animation()


    def blink(self, alternate=True):
        """
        Start blink animation.
        When alternate==True, the animation blinks each color in color buffer using all LEDs.
        For example, if the color buffer is red, green, blue then all LEDs turn red, then all
        LEDs turn green, then all LEDs turn blue before the pattern repeats.
        When alternate=False, the color buffer simply alternates between on and off (ie all LEDs black).
        """
        if alternate:
            self._blink_buffer = self.color_buffer.copy() # Blink colours in buffer one at a time.
        else:
            self._blink_buffer = None # Blink all colors in buffer

        self.mode = APA102.MODE_BLINK
        self.start_animation()


    def clear(self):
        """
        Stop any running animation and clear (turn off) all LEDs
        """

        self.stop_animation()
        self.color_buffer = deque([None] * self.num_leds, maxlen=self.num_leds)
        self._blink_buffer = None
        self._update()
        self.device.clear()


    def set_contrast(self, level):
        """
        Set global LED contrast between 0 (off) to 255 (maximum)
        """

        if level < 0:
            level = 0
        elif level > 255:
            level = 255

        self.contrast = level
        self.device.contrast(level)


    def set_color(self, color=None, index=-1):
        """
        Set the color of single LED (index >= 0), or all LEDs (when index == -1)
        Return True if color is set, or False of color parameter is not a recognised color value.
        """

        if not self.is_valid_color(color):
            logger.info("Ignoring unrecognised color {}".format(color))
            return False

        self.stop_animation()

        if index == -1:
            self.color_buffer = deque([color] * self.num_leds, maxlen=self.num_leds)
        else:
            self.color_buffer[index] = color

        self._update()
        return True


    def push_color(self, color):
        """
        Push a new color into the color array at index 0. The last value is dropped.
        Return True if color is set, or False of color parameter is not a recognised color value.
        """

        if not self.is_valid_color(color):
            logger.info("Ignoring unrecognised color {}".format(color))
            return False

        self.stop_animation()
        self.color_buffer.appendleft(color)
        self._update()


    def set_pattern(self, colors=('green', 'blue', 'red')):
        """
        Fill the color buffer with a repeating color pattern.
        Unrecognised colors in colors parameter are set to black.
        """

        if len(colors) == 0:
            return

        self.stop_animation()

        for i in range(0, int(ceil(float(self.num_leds) / float(len(colors))))):
            for color in colors:
                if self.is_valid_color(color):
                    self.color_buffer.appendleft(color)
                else:
                    logger.info("Defaulting unrecognised color '{}' to black".format(color))
                    self.color_buffer.appendleft('black')

        self._update()


    def _blink(self):
        """
        Blink animation routine called by Thread loop. Also see blink() and run().
        """

        if self._blink_buffer is None:
            # Blink all colours in buffer on and off.

            if self.contrast == 0:
                self.set_contrast(self._last_contrast)  # Restore previous contrast
            else:
                self._last_contrast = self.contrast
                self.set_contrast(0) # LEDs off
        else:
            # Cycle colors in buffer.
            color = self._blink_buffer[self._blink_index]

            if color is None:
                self._blink_index = 0
                color = self._blink_buffer[self._blink_index]

            self._blink_index += 1
            if self._blink_index >= len(self._blink_buffer):
                self._blink_index = 0

            self.color_buffer = deque([color] * self.num_leds, maxlen=self.num_leds)


    def _rotate_colors(self, count=1):
        """
        Left/Right animation routine called by Thread loop.
        Also see rotate_left(), rotate_right() and run().
        """

        self.color_buffer.rotate(count)


    def _rainbow(self, rounds=1):
        """
        Rainbow animation routine called by Thread loop.
        Also see rainbow() and run().
        """

        saturation = 100  # 0 (grayer) to 100 (full color)
        brightness = 100  # 0 (darker) to 100 (brighter)

        for i in range(0, rounds):
            for hue in tuple(range(0, 360)) + tuple(range(360, -1, -1)):  # 0..360..0
                color_str = "hsb({}, {}%, {}%)".format(hue, saturation, brightness)
                self.color_buffer.appendleft(color_str)
                self._update()

                timer = 0
                while self.is_animating() and timer < self.animation_delay_secs/10:
                    timer += 0.01
                    sleep(0.01)

                if self.mode != APA102.MODE_RAINBOW:
                    return #  Mode has change, so terminate rainbow loops.


    def _update(self):
        """
        Apply the color buffer to the APA102 strip.
        """

        with canvas(self.device) as draw:
            for led_pos in range(0, len(self.color_buffer)):
                color = self.color_buffer[led_pos]

                ## If your LED strip's colors are are not in the expected
                ## order, uncomment the following lines and adjust the indexes
                ## in the line color = (rgb[0], rgb[1], rgb[2])
                # rgb = getrgb(color)
                # color = (rgb[0], rgb[1], rgb[2])
                # if len(rgb) == 4:
                #     color += (rgb[3],)  # Add in Alpha

                if color == None:
                    color = 'black'

                draw.point((led_pos, 0), fill=color)
