"""
File: chapter02/led_gpiozero.py

Blinking an LED using GPIOZero.

Dependencies:
  pip3 install gpiozero pigpio

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""
from gpiozero import Device, LED                                                  # (1)
from gpiozero.pins.pigpio import PiGPIOFactory                                    # (2)
from time import sleep

Device.pin_factory = PiGPIOFactory() #Set gpiozero to use pigpio by default.      # (3)

GPIO_PIN = 21
led = LED(GPIO_PIN)                                                               # (4)
led.blink(background=False)                                                       # (5)