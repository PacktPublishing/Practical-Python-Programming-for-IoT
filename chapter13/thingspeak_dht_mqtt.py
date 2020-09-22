"""
File: chapter13/thingspeak_dht_mqtt.py

Publish temperature and humidity values from a DHT11 or DHT22 sensor to ThingSpeak using MQTT.

Dependencies:
  pip3 install pigpio-dht paho-mqtt

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""

from pigpio_dht import DHT11, DHT22
import paho.mqtt.publish as publish
from datetime import datetime
from time import sleep
from urllib.parse import urlencode
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# DHT Temperature/Humidity Sensor
GPIO = 24                                                                                # (1)

# ThingSpeak Configuration
WRITE_API_KEY = ""  # <<<< ADD YOUR WRITE API KEY HERE
CHANNEL_ID = ""     # <<<< ADD YOUR CHANNEL ID HERE
TIME_ZONE = "Australia/Melbourne" # See for values https://au.mathworks.com/help/thingspeak/time-zones-reference.html


# Configuration check
if not WRITE_API_KEY or not CHANNEL_ID:
  print("\nCONFIGURATION REQUIRED\nPlease update {} and add your ThingSpeak WRITE_API_KEY and CHANNEL_ID\n".format(__file__))
  quit(1)


HOST = "mqtt.thingspeak.com"
MQTT_TOPIC = "channels/" + CHANNEL_ID + "/publish/" + WRITE_API_KEY
QOS = 0  # ThinkSpeak API indicates MATT QoS is to be 0


# How often we collect and send data to ThingSpeak
POLL_INTERVAL_SECS = 60*10  # 10 Minutes


#dht = DHT11(GPIO, use_internal_pullup=True, timeout_secs=0.5)
dht = DHT22(GPIO, use_internal_pullup=True, timeout_secs=0.5)

if __name__ == "__main__":

    logger.info("Collecting Data and Sending to ThingSpeak every {} seconds. Press Control + C to Exit".format(POLL_INTERVAL_SECS))

    try:
        while True:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            try:
                result = dht.read(retries=5) # Singe data read (faster)
                #result = dht.sample()       # Multiple data reads, then take mean (slower)

            except Exception as e:
                # Failed to get reading from sensor
                logging.error("Failed to read sensor. Error: {}".format(e), exc_info=True)
                continue



            if not result['valid']:
                # We got a reading, but it has failed a checksum test
                # So re will try again.
                logger.warn("Data Checksum Invalid. Retrying.")
                continue


            # We have a reading, eg {'temp_c': 19, 'temp_f': 66.2, 'humidity': 32, 'valid': True}
            logger.info("Sensor result {}".format(result))


            # ThinkSpeak supports upto 8 data fields. We're only using 2.
            payload = {
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

            # Prepare encoded payload
            payload = urlencode(payload)

            try:
                # Publish data with ThinkSpeak
                publish.single(MQTT_TOPIC, payload, qos=QOS, hostname=HOST)
                logger.info("Published to {}".format(HOST))
            except Exception as e:
                logger.error("Failed to published to {}. Error: {}".format(HOST, e), exc_info=True)

            sleep(POLL_INTERVAL_SECS)

    except KeyboardInterrupt:
        logger.info("Bye")
