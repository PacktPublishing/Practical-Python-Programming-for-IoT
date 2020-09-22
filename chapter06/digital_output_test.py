"""
File: chapter06/digital_output_test.py

Test digital output.

Dependencies:
  pip3 install pigpio

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""
import pigpio
from time import sleep

GPIO_PIN = 21
pi = pigpio.pi()
pi.set_mode(GPIO_PIN, pigpio.OUTPUT)                   # (1)

try:
    while True:                                        # (2)
        # Alternate between HIGH and LOW
        state = pi.read(GPIO_PIN); # 1 or 0
        new_state = (int)(not state) # 1 or 0
        pi.write(GPIO_PIN, new_state);
        print("GPIO {} is {}".format(GPIO_PIN, new_state))
        sleep(3)

except KeyboardInterrupt:
    print("Bye")
    pi.stop()  # PiGPIO cleanup.
