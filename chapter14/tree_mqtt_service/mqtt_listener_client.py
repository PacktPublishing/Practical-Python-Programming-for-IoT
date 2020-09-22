"""
File: chapter14/tree_api_service/servo_controller.py

Receives MQTT messages for controlling APA102 and Servo and
republishes them locally using PyPubSub based on mappings
defined in config.py.

Built and tested with Python 3.7 on Raspberry Pi 4 Model B

Dependencies:
  pip3 install pypubsub paho-mqtt
"""
import paho.mqtt.client as mqtt
from pubsub import pub
import logging

logger = logging.getLogger('MQTTListener')

class MQTTListener:

    def __init__(self, config):
        """
        Constructor
        """

        self.mqtt_topic = config.MQTT_TOPIC_ROOT
        self.mqtt_host = config.MQTT_HOST
        self.mqtt_port = config.MQTT_PORT

        if self.mqtt_topic.find("#") == -1:
            raise ValueError("MQTT_TOPIC_ROOT must finish with a wildcard character, eg tree/#")

        self.topic_mappings = config.MQTT_TO_PUBSUB_TOPIC_MAPPINGS

        # Paho MQTT Client Configuration.
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.enable_logger() # Route logging to Python logging.
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_disconnect = self.on_disconnect
        self.mqtt_client.on_message = self.on_message


    def connect(self):
        """
        Connect to MQTT broker and listen to topic
        """

        logging.info("Connecting to MQTT Broker {}:{}".format(self.mqtt_host, self.mqtt_port))

        self.mqtt_client.connect(self.mqtt_host, self.mqtt_port)
        self.mqtt_client.loop_start() # Start listening for MQTT messages.


    def disconnect(self):
        """
        Graceful MQTT disconnection
        """
        logging.info("Disconnecting from MQTT Broker {}:{}".format(self.mqtt_host, self.mqtt_port))

        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()


    def on_connect(self, client, user_data, flags, connection_result_code):
        """
        on_connect is called when our program connects to the MQTT Broker.
       Always subscribe to topics in an on_connect() callback.
       This way if a connection is lost, the automatic
       re-connection will also results in the re-subscription occurring.
       """

        if connection_result_code == 0:
            # 0 = successful connection
            logger.info("Connected to MQTT Broker")
        else:
            # connack_string() gives us a user friendly string for a connection code.
            logger.error("Failed to connect to MQTT Broker: " + mqtt.connack_string(connection_result_code))

        # Subscribe to the topic for LED level changes.
        client.subscribe(self.mqtt_topic, qos=0)


    def on_disconnect(self, client, user_data, disconnection_result_code):
        """
        Called disconnects from MQTT Broker.
        """

        logger.error("Disconnected from MQTT Broker")


    def on_message(self, client, userdata, message):
        """
        Global message handler. Called for all messages received on subscribed topics.
        """

        logger.debug("MQTT Topic: {}, Payload: {}".format(message.topic, message.payload))

        mqtt_topic = message.topic.lower()
        pubsub_topic = None

        # Map MQTT topic into pyPybSub topic for configuration in config.py.
        if mqtt_topic in self.topic_mappings:

            pubsub_topic = self.topic_mappings[mqtt_topic]

            data = None

            if message.payload != b'':
                data = message.payload.decode("UTF-8").strip()

                # Normalise any multiple spacings to single space.
                while data.find("  ") != -1:
                    data = data.replace("  ", " ")

                data = data.split(" ") # String to List.

            logger.info("Publishing MQTT topic '{}' to PubSub topic '{}' with data '{}'".format(mqtt_topic, pubsub_topic, data))
            pub.sendMessage(pubsub_topic, sender=self, data=data)

        else:
           logger.warn("MQTT Topic '{}' not found in mapping dictionary.".format(mqtt_topic))
