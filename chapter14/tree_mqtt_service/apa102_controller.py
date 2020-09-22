"""
File: chapter14/tree_api_service/apa102_controller.py

Receives and processes PyPubSub messages for controlling APA102 LED Strip.

Built and tested with Python 3.7 on Raspberry Pi 4 Model B

Dependencies:
  pip3 install pypubsub paho-mqtt
"""
from time import sleep
from pubsub import pub
import logging
import config

logger = logging.getLogger('APA102Controller')

class APA102Controller:

    def __init__(self, apa102):
        """
        Constructor
        """

        self.apa102 = apa102

        # PyPubSub Subscriptions.
        pub.subscribe(self.on_push_message, config.PUBSUB_TOPIC_PUSH)
        pub.subscribe(self.on_pattern_message, config.PUBSUB_TOPIC_PATTERN)
        pub.subscribe(self.on_animation_message, config.PUBSUB_TOPIC_ANIMATION)
        pub.subscribe(self.on_speed_message, config.PUBSUB_TOPIC_SPEED)
        pub.subscribe(self.on_contrast_message, config.PUBSUB_TOPIC_CONTRAST)
        pub.subscribe(self.on_clear_message, config.PUBSUB_TOPIC_CLEAR)


    def on_clear_message(self, sender, data, topic=pub.AUTO_TOPIC):
        """
        PyPubSub handler for "clear" topic.
        """

        logger.debug("Topic {}, Params: {}".format(topic.getName(), data))
        self.apa102.clear()


    def on_contrast_message(self, sender, data, topic=pub.AUTO_TOPIC):
        """
        PyPubSub handler for "contrast" topic.
        """

        logger.debug("Topic {}, Params: {}".format(topic.getName(), data))

        if len(data) > 0 and data[0].isnumeric():
            contrast = int(data[0])
            self.apa102.set_contrast(contrast)


    def on_animation_message(self, sender, data, topic=pub.AUTO_TOPIC):
        """
        PyPubSub handler for "animation" topic.
        """

        logger.debug("Topic {}, Params: {}".format(topic.getName(), data))

        if len(data) == 0:
            return

        mode = data[0].upper()

        if mode == "CLEAR":
            self.apa102.clear()
        elif mode == "BLINK":
            self.apa102.blink(False)
        elif mode == "LEFT":
            self.apa102.rotate_left()
        elif mode == "RIGHT":
            self.apa102.rotate_right()
        elif mode == "RAINBOW":
            self.apa102.rainbow()
        else:
            logger.warn("Mode '{}' not recognised".format(mode))


    def on_push_message(self, sender, data, topic=pub.AUTO_TOPIC):
        """
        PyPubSub handler for "push" color topic.
        """

        logger.debug("Topic {}, Params: {}".format(topic.getName(), data))

        if len(data) == 0:
            return

        for color in data:
            self.apa102.push_color(color)


    def on_pattern_message(self, sender, data, topic=pub.AUTO_TOPIC):
        """
        PyPubSub handler for "pattern" color topic.
        """

        logger.debug("Topic {}, Params: {}".format(topic.getName(), data))

        if len(data) == 0:
            return

        self.apa102.set_pattern(data)


    def on_speed_message(self, sender, data, topic=pub.AUTO_TOPIC):
        """
        PyPubSub handler for "speed" topic.
        """

        logger.debug("Topic {}, Params: {}".format(topic.getName(), data))

        if len(data) == 0:
            return

        speed = int(data[0])
        self.apa102.set_animation_speed(speed)


