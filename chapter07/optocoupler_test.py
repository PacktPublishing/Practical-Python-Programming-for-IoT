"""
File: chapter07/optocoupler_test.py

Control an Optocoupler from a GPIO Pin.

Dependencies:
  pip3 install pigpio

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""
import pigpio
from time import sleep

GPIO_PIN = 21
pi = pigpio.pi()

try:
    # Note:  Circuit is wired as ACTIVE LOW.
    pi.write(GPIO_PIN, pigpio.LOW) # On.                       # (1)
    print("On")
    sleep(2)
    pi.write(GPIO_PIN, pigpio.HIGH)  # Off.                    # (2)
    print("Off")
    sleep(2)

except KeyboardInterrupt:
    print("Bye")

finally:
    pi.write(GPIO_PIN, pigpio.HIGH) # Off.
    pi.stop() # PiGPIO cleanup.

