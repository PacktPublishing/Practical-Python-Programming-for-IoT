"""
File: chapter14/dweet_integration_service/main.py

Program entry point.

This program receives dweets from dweet.io, parses them
then publishes them as MQTT messages based on the mappings
defined in config.py.

Dependencies:
  pip3 install paho-mqtt requests

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""
import logging
from signal import pause
from dweet_listener import DweetListener
import config

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':

    try:
        # Create dweet listener instance.
        dl = DweetListener(config)

        # Start listening for dweets.
        if config.USE_POLLING:
            # Polling method.
            dl.poll()
            pause()
        else:
            # Streaming method. This call below blocks so there is no need for a pause()
            dl.stream_dweets()

    except KeyboardInterrupt:
        print("Bye")