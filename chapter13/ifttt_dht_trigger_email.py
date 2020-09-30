"""
File: chapter13/ifttt_dht_trigger_email.py

This program monitors the temperature using a DHT 11 or DHT 22 sensor, and
triggers an IFTTT Applet via a Webhook when the temperature reaches a configured point.

Dependencies:
  pip3 install pigpio-dht requests

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""
from pigpio_dht import DHT11, DHT22
from datetime import datetime
from time import sleep
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# DHT Temperature/Humidity Sensor GPIO.
GPIO = 24                                                                                      # (1)

# Configure DHT sensor - Uncomment appropiate line based on the sensor you have.
dht = DHT11(GPIO, use_internal_pullup=True, timeout_secs=0.5)                                 # (2)
#dht = DHT22(GPIO, use_internal_pullup=True, timeout_secs=0.5)

# How often we check the temperature
POLL_INTERVAL_SECS = 60*10  # 10 Minutes


# Celsius or Fahrenheit
USE_DEGREES_CELSIUS = True                                                                     # (3)

# At what high temperature will we send an email
HIGH_TEMP_TRIGGER = 20 # Degrees                                                               # (4)

# At what low temperature will we send an email
LOW_TEMP_TRIGGER = 19  # Degrees                                                               # (5)


# To track when a high temp event has been triggered
triggered_high = False


# IFTTT Configuration
EVENT = "RPITemperature" # <<<< Add your IFTTT Event name                                      # (6)
API_KEY = "<ADD YOUR IFTTT API KEY HERE>" # <<<< Add your IFTTT API Key


# Configuration check
if not EVENT or not API_KEY:
  print("\nCONFIGURATION REQUIRED\nPlease update {} and add your EVENT name and API_KEY\n".format(__file__))
  quit(1)


# Create the IFTTT Webhook URL
URL = "https://maker.ifttt.com/trigger/{}/with/key/{}".format(EVENT, API_KEY)                  # (7)

# HTTP headers used with Webhook request.
REQUEST_HEADERS = {"Content-Type": "application/json"}


def send_ifttt_event(temperature, humidity, message):
    """ Call the IFFF Webhook URL """

    # In IFTTT, the dict/JSON key names must be value1, value2 and value3
    data = {
      "value1": result['temp_c'],
      "value2": result['humidity'],
      "value3": message
    }

    # Make IFTTT request - it can be either a HTTP GET or POST
    response = requests.post(URL, headers=REQUEST_HEADERS, params=data)

    # IFTTT Response is plain text
    logger.info("Response {}".format(response.text))

    if response.status_code == requests.codes.ok:
        logger.info("Successful Request.")
    else:
        logger.info("Unsuccessful Request. Code:{}".format(response.status_code))


if __name__ == "__main__":

    try:
        logger.info("Press Control + C To Exit.")

        while True:
            try:
                result = dht.read(retries=5) # Singe data read (faster)
                #result = dht.sample()       # Multiple data reads, then take mean (slower)

            except Exception as e:
                # Failed to get reading from sensor
                logger.error("Failed to read sensor. Error: {}".format(e), exc_info=True)
                continue

            if not result['valid']:
                # We got a reading, but it has failed a checksum test
                # So re will try again.
                logger.warn("Data Checksum Invalid. Retrying.")
                continue

            # We have a reading, eg {'temp_c': 19, 'temp_f': 66.2, 'humidity': 32, 'valid': True}
            logger.info("Sensor result {}".format(result))

            current_temp = None

            if USE_DEGREES_CELSIUS:
                current_temp =  result['temp_c']
            else:
                current_temp =  result['temp_f']

            humidity = result['humidity']

            if not triggered_high and current_temp >= HIGH_TEMP_TRIGGER:
                # Trigger IFTTT Event (eg that will send email)
                logger.info("Temperature {} is >= {}, triggering event {}".format(current_temp, HIGH_TEMP_TRIGGER, EVENT))
                triggered_high = True
                send_ifttt_event(current_temp, humidity, "High Temperature Trigger")

            elif triggered_high and current_temp <= LOW_TEMP_TRIGGER:
                # Temperature is at or below low trigger threshold.
                logger.info("Temperature {} is <= {}, trigger reset".format(current_temp, LOW_TEMP_TRIGGER))
                triggered_high = False
                send_ifttt_event(current_temp, humidity, "Low Temperature Trigger")

            sleep(POLL_INTERVAL_SECS)

    except KeyboardInterrupt:
        print("Bye")
