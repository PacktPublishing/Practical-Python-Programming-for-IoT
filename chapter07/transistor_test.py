"""
File: chapter07/transistor_test.py

Control a MOSFET Transitor from a GPIO Pin.

Dependencies:
  pip3 install pigpio

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""
import pigpio
from time import sleep

GPIO_PIN = 21
pi = pigpio.pi()

# 8000 max hardware timed frequency by default pigpiod configuration.
pi.set_PWM_frequency(GPIO_PIN, 8000)

# We set the range to 0..100 to mimic 0%..100%. This means
# calls to pi.set_PWM_dutycycle(GPIO_PIN, duty_cycle) now
# take a value in the range 0 to 100 as their duty_cycle
# parameter rather than the default range of 0..255.
pi.set_PWM_range(GPIO_PIN, 100)                                      # (1)

try:
    pi.write(GPIO_PIN, pigpio.HIGH) # On.                            # (2)
    print("On")
    sleep(2)
    pi.write(GPIO_PIN, pigpio.LOW)  # Off.
    print("Off")
    sleep(2)

    # Fade In.
    for duty_cycle in range(0, 100):                                 # (3)
        pi.set_PWM_dutycycle(GPIO_PIN, duty_cycle)
        print("Duty cycle {}%".format(duty_cycle))
        sleep(0.05)

    # Fade Out.
    for duty_cycle in range(100, 0, -1):                             # (4)
        pi.set_PWM_dutycycle(GPIO_PIN, duty_cycle)
        print("Duty Cycle {}%".format(duty_cycle))
        sleep(0.05)

    sleep(2)

except KeyboardInterrupt:
    print("Bye")

finally:
    pi.write(GPIO_PIN, pigpio.LOW) # Off.
    pi.stop() # PiGPIO cleanup.

