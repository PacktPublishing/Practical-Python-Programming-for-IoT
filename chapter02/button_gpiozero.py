"""
File: chapter02/button_gpiozero.py

Turn on and off an LED with a Button using GPIOZero.

Dependencies:
  pip3 install gpiozero pigpio

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""
from gpiozero import Device, LED, Button                                                 # (1)
from gpiozero.pins.pigpio import PiGPIOFactory
import signal                                                                            # (2)

LED_GPIO_PIN = 21
BUTTON_GPIO_PIN = 23

Device.pin_factory = PiGPIOFactory() #set gpiozero to use pigpio by default.

def pressed():
    led.toggle()                                                                         # (3)
    state = 'on' if led.value == 1 else 'off'                                            # (4)
    print("Button pressed: LED is " + state)                                             # (5)

led = LED(LED_GPIO_PIN)
led.off()


button = Button(BUTTON_GPIO_PIN, pull_up=True, bounce_time=0.1) # Bounce time in seconds # (6)
button.when_pressed = pressed                                                            # (7)

print("Press button to turn LED on and off.")

signal.pause() # Stops program from exiting.                                             # (8)