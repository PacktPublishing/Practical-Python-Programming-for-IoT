"""
File: chapter13/thingspeak_dht_http.py

Publish temperature and humidity values from a DHT11 or DHT22 sensor to ThingSpeak using the
ThingSpeak RESTFul-API.

Dependencies:
  pip3 install pigpio-dht requests

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""
from pigpio_dht import DHT11, DHT22
import requests
from datetime import datetime
from urllib.parse import urlencode
from time import sleep
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# DHT Temperature/Humidity Sensor
GPIO = 24                                                                          # (1)

#dht = DHT11(GPIO, use_internal_pullup=True, timeout_secs=0.5)
dht = DHT22(GPIO, use_internal_pullup=True, timeout_secs=0.5)

# ThingSpeak Configuration
WRITE_API_KEY = ""   # <<<< ADD YOUR WRITE API KEY HERE                            # (2)
TIME_ZONE = "Australia/Melbourne" # See for values https://au.mathworks.com/help/thingspeak/time-zones-reference.html


# Configuration check
if not WRITE_API_KEY:
  print("\nCONFIGURATION REQUIRED\nPlease update {} and add your ThingSpeak WRITE_API_KEY\n".format(__file__))
  quit(1)


# ThinkSpeak RESTFul API endpoint for updates.
URL = "https://api.thingspeak.com/update.json"


# How often we collect and send data to ThingSpeak
POLL_INTERVAL_SECS = 60*10  # 10 Minutes



REQUEST_HEADERS = {"Content-Type": "application/json"}

if __name__ == "__main__":

    print("Collecting Data and Sending to ThingSpeak every {} seconds. Press Control + C to Exit".format(POLL_INTERVAL_SECS))

    try:
        while True:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

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
                logger.warning("Data Checksum Invalid. Retrying.")
                continue


            # We have a reading, eg {'temp_c': 19, 'temp_f': 66.2, 'humidity': 32, 'valid': True}
            logger.info("Sensor result {}".format(result))


            # ThinkSpeak supports upto 8 data fields. We're only using 2.
            payload = {
                "api_key": WRITE_API_KEY,
                "field1": result['temp_c'],
                "field2": result['humidity'],
                #"field3": '',
                #"field4": '',
                #"field5": '',
                #"field6": '',
                #"field7": '',
                #"field8": '',
                "created_at:": timestamp,
                "timezone": TIME_ZONE
            }

            # Send data to ThinkSpeak
            response = requests.get(URL, headers=REQUEST_HEADERS, params=payload)

            if response.status_code == requests.codes.ok:
                logger.info("Request: {}, Response: {}".format(response.url, response.text))
            else:
                logger.error("Failed to request {}. Error: {}".format(response.url, response.status_code))

            sleep(POLL_INTERVAL_SECS)

    except KeyboardInterrupt:
        logger.info("Bye")
