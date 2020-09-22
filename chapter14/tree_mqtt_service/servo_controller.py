"""
File: chapter14/tree_api_service/servo_controller.py

Receives and processes PyPubSub messages for controlling Servo.

Built and tested with Python 3.7 on Raspberry Pi 4 Model B

Dependencies:
  pip3 install pypubsub paho-mqtt
"""
from time import sleep
from pubsub import pub
import logging
import config

logger = logging.getLogger('ServoController')

class ServoController:

    def __init__(self, servo):
        """
        Constructor
        """

        self.servo = servo

        # PyPubSub subscription for "sweep" topics.
        pub.subscribe(self.on_sweep_message, config.PUBSUB_TOPIC_SWEEP)


    def on_sweep_message(self, sender, data, topic=pub.AUTO_TOPIC):
        """
        PyPubSub handler for "sweep" topic.
        """

        logger.debug("Topic {}, Params: {}".format(topic.getName(), data))

        self.servo.sweep(degrees=config.SERVO_SWEEP_DEGREES, count=config.SERVO_SWEEP_COUNT)
        self.servo.center()
        sleep(1) # Give servo time to move.
        self.servo.idle() # Save power by making servo idle.
