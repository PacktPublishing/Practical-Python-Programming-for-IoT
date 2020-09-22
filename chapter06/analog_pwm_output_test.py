"""
File: chapter06/analog_pwm_output_test.py

Create PWM output signal.

Dependencies:
  pip3 install pigpio

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""
import pigpio
from time import sleep

GPIO_PIN = 21
pi = pigpio.pi()

# 8000 max hardware timed frequency by default pigpiod configuration.
pi.set_PWM_frequency(GPIO_PIN, 8000)                                        # (1)

duty_cycle_percentages = [0, 25, 50, 75, 100]                               # (2)
max_voltage = 3.3

try:
    while True:
       for duty_cycle_pc in duty_cycle_percentages:                         # (3)
           duty_cycle = int(255 * duty_cycle_pc / 100)
           estimated_voltage = max_voltage * duty_cycle_pc / 100
           print("Duty Cycle {}%, estimated voltage {} volts".format(duty_cycle_pc, estimated_voltage))
           pi.set_PWM_dutycycle(GPIO_PIN, duty_cycle)                       # (4)
           sleep(5)

except KeyboardInterrupt:
  print("Bye")
  pi.stop() # PiGPIO cleanup.
