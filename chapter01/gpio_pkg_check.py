"""
File: chapter01/gpio_pkg_check.py

This Python script checks for the availability of various Python GPIO Library Packages for the Raspberry Pi.
It does this by attempting to import the Python package. If the package import is successful
we report the package as Available, and if the import (or import initialization) fails for any reason,
we report the package as Unavailable.

Dependencies:
  pip3 install gpiozero pigpio

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""
try:
    import gpiozero
    print('GPIOZero   Available')
except:
    print('GPIOZero   Unavailable. Install with "pip install gpiozero"')

try:
    import pigpio
    print('PiGPIO     Available')
except:
    print('PiGPIO     Unavailable. Install with "pip install pigpio"')

