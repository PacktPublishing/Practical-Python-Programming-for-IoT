"""
File: chapter04/mqtt_led.py

A full life-cycle Python + MQTT program to control an LED.

Dependencies:
  pip3 install paho-mqtt gpiozero pigpio

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""
import logging
import signal
import sys
import json
from time import sleep
from gpiozero import Device, PWMLED
from gpiozero.pins.pigpio import PiGPIOFactory
import paho.mqtt.client as mqtt                                                                # (1)


# Initialize Logging
logging.basicConfig(level=logging.WARNING)  # Global logging configuration
logger = logging.getLogger("main")  # Logger for this module
logger.setLevel(logging.INFO) # Debugging for this file.


# Initialize GPIO
Device.pin_factory = PiGPIOFactory() # Set GPIOZero to use PiGPIO by default.


# Global Variables
LED_GPIO_PIN = 21
BROKER_HOST = "localhost"                                                                       # (2)
BROKER_PORT = 1883
CLIENT_ID = "LEDClient"                                                                         # (3)
TOPIC = "led"                                                                                   # (4)
client = None  # MQTT client instance. See init_mqtt()                                          # (5)
led = None     # PWMLED Instance. See init_led()


"""
GPIO Related Functions
"""
def init_led():
    """Create and initialise an LED Object"""
    global led
    led = PWMLED(LED_GPIO_PIN)
    led.off()


def set_led_level(data):                                                                       # (6)
    """Set LED State to one of On, Blink or Off (Default)
      'data' expected to be a dictionary with the following format:
      {
          "level": a number between 0 and 100,
      }
    """

    level = None # a number 0..100

    if "level" in data:
        level = data["level"]

        if isinstance(level, int) or isinstance(level, float) or level.isdigit():
            # State is a number
            level = max(0, min(100, int(level))) # Bound state to range 0..100
            led.value = level / 100  # Scale 0..100% back to 0..1
            logger.info("LED at brightness {}%".format(level))

        else:
            logger.info("Request for unknown LED level of '{}'. We'll turn it Off instead.".format(level))
            led.value = 0 # 0% = Led off.
    else:
        logger.info("Message '{}' did not contain property 'level'.".format(data))


"""
MQTT Related Functions and Callbacks
"""
def on_connect(client, user_data, flags, connection_result_code):                              # (7)
    """on_connect is called when our program connects to the MQTT Broker.
       Always subscribe to topics in an on_connect() callback.
       This way if a connection is lost, the automatic
       re-connection will also results in the re-subscription occurring."""

    if connection_result_code == 0:                                                            # (8)
        # 0 = successful connection
        logger.info("Connected to MQTT Broker")
    else:
        # connack_string() gives us a user friendly string for a connection code.
        logger.error("Failed to connect to MQTT Broker: " + mqtt.connack_string(connection_result_code))

    # Subscribe to the topic for LED level changes.
    client.subscribe(TOPIC, qos=2)                                                             # (9)



def on_disconnect(client, user_data, disconnection_result_code):                               # (10)
    """Called disconnects from MQTT Broker."""
    logger.error("Disconnected from MQTT Broker")



def on_message(client, userdata, msg):                                                         # (11)
    """Callback called when a message is received on a subscribed topic."""
    logger.debug("Received message for topic {}: {}".format( msg.topic, msg.payload))

    data = None

    try:
        data = json.loads(msg.payload.decode("UTF-8"))                                         # (12)
    except json.JSONDecodeError as e:
        logger.error("JSON Decode Error: " + msg.payload.decode("UTF-8"))

    if msg.topic == TOPIC:                                                                     # (13)
        set_led_level(data)                                                                    # (14)

    else:
        logger.error("Unhandled message topic {} with payload " + str(msg.topic, msg.payload))



def signal_handler(sig, frame):
    """Capture Control+C and disconnect from Broker."""
    global led_state

    logger.info("You pressed Control + C. Shutting down, please wait...")

    client.disconnect() # Graceful disconnection.
    led.off()
    sys.exit(0)



def init_mqtt():
    global client

    # Our MQTT Client. See PAHO documentation for all configurable options.
    # "clean_session=True" means we don"t want Broker to retain QoS 1 and 2 messages
    # for us when we"re offline. You"ll see the "{"session present": 0}" logged when
    # connected.
    client = mqtt.Client(                                                                      # (15)
        client_id=CLIENT_ID,
        clean_session=False)

    # Route Paho logging to Python logging.
    client.enable_logger()                                                                     # (16)

    # Setup callbacks
    client.on_connect = on_connect                                                             # (17)
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    # Connect to Broker.
    client.connect(BROKER_HOST, BROKER_PORT)                                                   # (18)



# Initialise Module
init_led()
init_mqtt()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)  # Capture Control + C                        # (19)
    logger.info("Listening for messages on topic '" + TOPIC + "'. Press Control + C to exit.")

    client.loop_start()                                                                        # (20)
    signal.pause()
