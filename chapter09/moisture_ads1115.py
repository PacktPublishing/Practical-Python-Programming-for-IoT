"""
File: chapter09/moisture_LDR.py

Detect moisture using ADS1115 ADC

Dependencies:
  pip3 install pigpio adafruit-circuitpython-ads1x15

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""
from time import sleep
import pigpio
import moisture_calibration_config as calibration                            # (1)  <<<< DIFFERENCE: importing moisture calibration file.

# Below imports are part of Circuit Python and Blinka
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

pi = pigpio.pi()

# LED is connected to this GPIO Pin
LED_GPIO = 21

# Configure LED pin and start wiht LED Off
pi.set_mode(LED_GPIO, pigpio.OUTPUT)
pi.write(LED_GPIO, pigpio.LOW) # LED Off

# Voltage readings from ADS1115 when
# probe is immersed (wet), and when not immersed (dry)
WET_VOLTS = calibration.MAX_VOLTS                                           # (2) <<<< DIFFERENCE: Variable names changed.
DRY_VOLTS = calibration.MIN_VOLTS

# Votage reading (and buffer) where we set
# global variable triggered = True or False
TRIGGER_VOLTS = WET_VOLTS - ((WET_VOLTS - DRY_VOLTS) / 2)                   # (3) <<<< DIFFERENCE: Variable names changed.
TRIGGER_BUFFER = 0.25                                                       # (4)


# Create the I2C bus & ADS object.
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
analog_channel = AnalogIn(ads, ADS.P0)  #ADS.P0 --> A0

# "triggered" is set to True or False as the voltage
# read by the ADS1115 passes over it's
# TRIGGER_VOLTS (+/- TRIGGER_BUFFER) thresholds.
triggered = False                                                           # (5)

def update_trigger(volts):
    """
    Compare the volts parameter to trigger conditions
    TRIGGER_VOLTS +/- TRIGGER_BUFFER and update
    the global 'triggered' variable as appropiate.
    """
    global triggered

    if triggered and volts < TRIGGER_VOLTS - TRIGGER_BUFFER:                # <<<< DIFFERENCE: test condition reversed compaired to LDR example,
        triggered = False                                                   # <<<< DIFFERENCE: this is so we "trigger" when the probe is wet.
    elif not triggered and volts > TRIGGER_VOLTS + TRIGGER_BUFFER:
        triggered = True


if __name__ == '__main__':

    trigger_text = "{:0.4f} +/- {}".format(TRIGGER_VOLTS, TRIGGER_BUFFER)

    try:
        while True:                                                        # (6)
            # Read voltage from ADS1115 channel
            volts = analog_channel.voltage

            update_trigger(volts)

            output = "LDR Reading volts={:>5.3f}, trigger at {}, triggered={}".format(volts, trigger_text, triggered)
            print(output)

            # Switch LED on or off based on trigger.
            pi.write(LED_GPIO, triggered)                                 # (7)
            sleep(0.05)

    except KeyboardInterrupt:
        i2c.deinit()
        print("Switching LED Off")
        pi.write(LED_GPIO, pigpio.LOW) # LED Off
        pi.stop() # PiGPIO Cleanup
