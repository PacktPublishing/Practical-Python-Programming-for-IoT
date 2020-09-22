"""
File: chapter05/pwm_hardware_timed.py

PWM demo using hardware timed PWM and a LED.

Dependencies:
  pip3 install pigpio adafruit-circuitpython-ads1x15

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""
from time import sleep
import pigpio

# Below imports are part of Circuit Python and Blinka
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

pi = pigpio.pi()

# We're using hardware-timed PWM which is available on any GPIO Pin.
LED_GPIO_PIN = 12

# Ensure we start with LED off.
pi.set_mode(LED_GPIO_PIN, pigpio.OUTPUT)
pi.write(LED_GPIO_PIN, pigpio.LOW)

# Create the I2C bus & ADS object.
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)

# Analog Inputs on Channels 0 and 1 (A0 and A1 on breakout board)
frequency_ch = AnalogIn(ads, ADS.P0)
duty_cycle_ch = AnalogIn(ads, ADS.P1)

# The max/min range we get from our Analog Inputs on the ADS1115.
# Max value derived by observation. See print(output1) in while loop.
A_IN_EDGE_ADJ = 0.001 # Edge adjustment factor for MIN_A_IN_VOLTS and MAN_A_IN_VOLTS
MIN_A_IN_VOLTS = 0 + A_IN_EDGE_ADJ
MAX_A_IN_VOLTS = 3.286 - A_IN_EDGE_ADJ

# Max/Min Duty Cycle value as per PiGPIO documentation
# for set_PWM_dutycycle()
# http://abyz.me.uk/rpi/pigpio/python.html#set_PWM_dutycycle
MIN_DUTY_CYCLE = 0
MAX_DUTY_CYCLE = 255

# Pre-defined frequency values (at pigpiod default 5ms sample rate)
# as per PiGPIO documentation. The range is 10 to 8000 hertz, but we're
# capping it at 80 hertz for LED visual and piscope demonstration.
# http://abyz.me.uk/rpi/pigpio/python.html#set_PWM_frequency
FREQUENCIES = (10,20,40,50,80,100,160,200,250,320,400,500,800,1000,1600,2000,4000,8000)
MIN_FREQ_INDEX = 0
MAX_FREQ_INDEX = 4 # Max 80Hz

# Helper method to map an input value (v_in) between alternative max/min ranges.
def map_value(in_v, in_min, in_max, out_min, out_max):
    v = (in_v - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    if v < out_min:
        v = out_min
    elif v > out_max:
        v = out_max

    return v

if __name__ == '__main__':
    try:
        last_frequency = -1

        while True:
            # Frequency value mapped from Analog Input Channel to PiGPIO values.
            frequency_index = int(map_value(frequency_ch.voltage, MIN_A_IN_VOLTS, MAX_A_IN_VOLTS, MIN_FREQ_INDEX, MAX_FREQ_INDEX))
            frequency = FREQUENCIES[frequency_index]

            # Duty Cycle value mapped from Analog Input Channel to PiGPIO expected range.
            duty_cycle = int(map_value(duty_cycle_ch.voltage, MIN_A_IN_VOLTS, MAX_A_IN_VOLTS, MIN_DUTY_CYCLE, MAX_DUTY_CYCLE))
            duty_cycle_percent = int((duty_cycle/MAX_DUTY_CYCLE) * 100)

            # Set Hardware Timed PWM Duty Cycle and Frequency.
            # http://abyz.me.uk/rpi/pigpio/python.html#set_PWM_dutycycle
            # http://abyz.me.uk/rpi/pigpio/python.html#set_PWM_frequency
            pi.set_PWM_dutycycle(LED_GPIO_PIN, duty_cycle)

            # Per docs: 'If PWM is currently active on the GPIO it will be switched off and then back on at the new frequency.'
            # This off/on switch occurs even if the new frequency is the same as the current frequency
            # hence we only re-apply frequency if to changes to avoid avoidable distortion to the PWM signal.
            if last_frequency != frequency:
                pi.set_PWM_frequency(LED_GPIO_PIN, frequency)
                #print('Frequency Changed', last_frequency, frequency)
                last_frequency = frequency

            frequency_used = pi.get_PWM_frequency(LED_GPIO_PIN) # For print(output2)

            # Raw Analog input values.
            output1 = "Frequency Pot (A0) value={:>5} volts={:>5.3f}  Duty Cycle Pot (A1) value={:>5} volts={:>5.3f}".format(frequency_ch.value, frequency_ch.voltage, duty_cycle_ch.value, duty_cycle_ch.voltage)
            #print(output1)

            # Text for Terminal display output.
            output2 = "Frequency (Pot) {:>5}Hz   Frequency (Used) {:>5}Hz   Duty Cycle {:>3}%".format(frequency, frequency_used, duty_cycle_percent)
            print(output2)

            sleep(0.01)

    except KeyboardInterrupt:
      print("Bye")

      # Revert GPIO to basic output and make LOW to turn LED off.
      pi.set_mode(LED_GPIO_PIN, pigpio.OUTPUT)
      pi.write(LED_GPIO_PIN, pigpio.LOW)

      # PiGPIO cleanup.
      pi.stop()
