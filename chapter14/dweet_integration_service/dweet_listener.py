"""
File: chapter14/dweet_integrtion_service/dweet_listener.py

Core program Implementation that receives dweets and republishes them as MQTT messages.

Dependencies:
  pip3 install paho-mqtt requests

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""
from time import sleep
import os
import threading
import logging
import requests
from uuid import uuid1
import json
import paho.mqtt.publish as publish

logger = logging.getLogger('DweetListener')

class DweetListener:

    @classmethod
    def resolve_thing_name(cls, thing_file="thing_name.txt"):
        """
        Get existing, or create a new thing name
        """

        if os.path.exists(thing_file):
            with open(thing_file, 'r') as file_handle:
                name = file_handle.read().strip()
                logger.info('Thing name ' + name + ' loaded from ' + thing_file)
                return name.strip()
        else:
            name = str(uuid1())[:8]  # UUID object to string.
            logger.info('Created new thing name ' + name)

            with open(thing_file, 'w') as f:  # (5)
                f.write(name)

        return name


    def __init__(self, config):
        """
        Constructor
        """

        self.poll_secs = config.POLL_SECS

        self.mqtt_host = config.MQTT_HOST
        self.mqtt_port = config.MQTT_PORT
        self.mqtt_topic_retain_message = config.TOPIC_RETAIN_MESSAGE

        self.action_topic_mappings = config.ACTION_TOPIC_MAPPINGS
        self.dweet_io_url = config.DWEET_IO_URL

        # Set or resolve Thing Name.
        if config.THING_NAME is None:
            # Get previously used Thing Name from thing_name.txt or generate a new Thing Name.
            self.thing_name = DweetListener.resolve_thing_name()
        else:
            self.thing_name = config.THING_NAME

        # Last dweeted command. We keep track of the last command (and initialise it)
        # so that repeated polls do not result in duplicate MQTT message publications.
        self.last_command = None
        self.init_last_command()

        self.running = False
        self._thread = None

        logger.info("Dweet Listener initialised. Publish command dweets to '{}/dweet/for/{}?command=...'".format(self.dweet_io_url, self.thing_name))


    def stop(self):
        """
        Stop polling Thread
        """

        self.running = False
        self._thread = None


    def poll(self):
        """
        Start Polling for Dweets
        """

        if self._thread is not None:
            # Thread already exists.
            logger.warn("Thread Already Started.")
            return

        self.running = True

        self._thread = threading.Thread(name='DweetListener',
                                         target=self._poll,
                                         daemon=True)
        self._thread.start()
        logger.debug("Thread Started.")


    def _poll(self):
        """ Poll or stream from dweet service """

        while self.running:

            dweet = self.get_latest_dweet()

            if dweet is not None:
                self.process_dweet(dweet)

            # Sleep
            timer = 0
            while timer < self.poll_secs:
                sleep(0.1)
                timer += 0.1

        self.__thread = None
        logger.debug("Thread Finished.")


    def init_last_command(self):
        """
        Get the last dweeted command and store in self.last_command
        """

        dweet_content = self.get_latest_dweet()

        if dweet_content and "command" in dweet_content:
            self.last_command = dweet_content['command'].strip()


    def get_latest_dweet(self):
        """
        Get the last dweet made by our Thing.
        """

        resource = self.dweet_io_url + '/get/latest/dweet/for/' + self.thing_name
        logger.debug('Getting last dweet from url %s', resource)

        r = requests.get(resource)

        if r.status_code == 200:
            dweet = r.json() # return a Python dict.
            logger.debug('Last dweet for thing was %s', dweet)

            dweet_content = None

            if dweet['this'] == 'succeeded':
                # We're just interested in the dweet content property.
                dweet_content = dweet['with'][0]['content']

            return dweet_content

        else:
            logger.error('Getting last dweet failed with http status %s', r.status_code)
            return {}


    def stream_dweets(self):
        """
        Listen for streaming for dweets
        """

        resource = self.dweet_io_url + '/listen/for/dweets/from/' + self.thing_name
        logger.info('Streaming dweets from url %s', resource)

        self.running = True

        session = requests.Session()
        request = requests.Request("GET", resource).prepare()

        while self.running:
            try:
                response = session.send(request, stream=True, timeout=1000)

                for line in response.iter_content(chunk_size=None):
                    if line:
                        try:
                            json_str = line.splitlines()[1]
                            json_str = json_str.decode('utf-8')
                            dweet = json.loads(eval(json_str)) # json_str is a string in a string.
                            logger.debug('Received a streamed dweet %s', dweet)

                            dweet_content = dweet['content']
                            self.process_dweet(dweet_content)
                        except Exception as e:
                            logger.error(e, exc_info=True)
                            logger.error('Failed to process and parse dweet json string %s', json_str)

            except requests.exceptions.RequestException as e:
                #Lost connection. The While loop will reconnect.
                #logger.error(e, exc_info=True)
                pass

            except Exception as e:
                logger.error(e, exc_info=True)


    def process_dweet(self, dweet):                                                     # (1)
        """
        Process dweet and publish to MQTT Topic
        """

        # make sure we have a command parameter and that it's not empty.
        if not "command" in dweet or dweet['command'].strip() == "":
            return

        command = dweet['command'].strip() # String "<action> <data1> <data2> ... <dataN>"

        if self.last_command == command:
            return

        self.last_command = command

        # Normalise any multiple spacings to single space.
        while command.find("  ") != -1:
            command = command.replace("  ", " ")

        elements = command.split(" ") # List <action>,<data1>,<data2>,...,<dataN>
        action = elements[0].lower()
        data = " ".join(elements[1:])

        self.publish_mqtt(action, data)                                                 # (2)


    def publish_mqtt(self, action, data):                                               # (3)
        """
        MQTT Mapping and Publishing
        """

        if action in self.action_topic_mappings:
            # Map Action into MQTT Topic (Eg mode --> tree/lights/mode). See config.py for mappings.

            topic = self.action_topic_mappings[action]
            retain = topic in self.mqtt_topic_retain_message                            # (4)

            logger.info("Publishing action '{}' to MQTT topic '{}' with data '{}'".format(action, topic, data))

            publish.single(topic, data, qos=0,                                          # (5)
                           retain=retain,
                           hostname=self.mqtt_host, port=self.mqtt_port)

        else:
            logger.warn("Action '{}' not recognised in mapping dictionary.".format(action))

