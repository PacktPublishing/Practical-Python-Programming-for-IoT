"""
File: chapter02/pigpio_led_class.py

A Class wrapper that mimics GPIOZero.LED()

Dependencies:
  pip3 install pigpio

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""
import pigpio
import threading
from time import sleep

class PiGPIOLED:

    # Shared class variable.
    blink_rate_secs = 2 # on-off cycle seconds

    def __init__(self, gpio_pin):
        self.pi = pigpio.pi()
        self.gpio_pin = gpio_pin
        self.is_blinking = False
        self.pi.write(self.gpio_pin, 0) # Off by default.


    def __del__(self):
        self.pi.stop()
        self.pi = None


    def on(self):
        self.is_blinking = False
        self.pi.write(self.gpio_pin, 1)  # On


    def blink(self, background=True):
        if self.is_blinking:
            return

        self.is_blinking = True

        def do_blink():
            while self.is_blinking:
                self.pi.write(self.gpio_pin, 1)   # On

                sleep(PiGPIOLED.blink_rate_secs/2)

                if self.is_blinking:
                  self.pi.write(self.gpio_pin, 0) # Off
                  sleep(PiGPIOLED.blink_rate_secs/2)

        if background:
            # daemon=True prevents our thread below from preventing the main thread
            # (essentially the code in if __name__ == '__main__') from exiting naturally
            # when it reaches it's end. If you try daemon=False you will discover that the
            # program never quits back to the Terminal and appears to hang after the LED turns off.
            thread = threading.Thread(name='LED on GPIO ' + str(self.gpio_pin),
                                            target=do_blink,
                                            daemon=True)
            thread.start()
        else:
          do_blink() # Blocking.


    def off(self):
        self.is_blinking = False
        self.pi.write(self.gpio_pin, 0)

if __name__ == '__main__':
    """Run from command line to test."""
    from time import sleep
    LED_GPIO = 21
    led = PiGPIOLED(LED_GPIO)
    led.blink()
    sleep(5)
    led.off()
