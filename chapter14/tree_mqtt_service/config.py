"""
File: chapter14/tree_mqtt_service/config.py

Tree MQTT Service configuration.

This program processes MQTT messages to control the IoTree circuit.

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""

"""
APA102 CONFIGURATION
"""

# Number of LEDs in the APA102 LED Strip.
APA102_NUM_LEDS = 60

# Default APS102 LED contrast between 0 (off) and 255 (max)
APA102_DEFAULT_CONTRAST = 128

# SPI Configuration for APA102 LUMA Class.
# Allowed values for APA102_BUS_SPEED_HZ are 500000, 1000000, 2000000, 4000000, 8000000, 16000000, 32000000
# and the value used needs to be suitable for use with the switching speed of your logical level converter.
# For more information on LUMA SPI see https://github.com/rm-hull/luma.core/blob/master/luma/core/interface/serial.py
# or see Chapter 8 Lights, Indicators and Displaying Information
APA102_PORT = 0
APA102_DEVICE = 0
APA102_BUS_SPEED_HZ = 2000000


"""
SERVO CONFIGURATION
"""

# Servo Signal GPIO.
SERVO_GPIO = 21

# The max left and max right pulse in nanoseconds for the Servo.
# The use of pulse widths and servo positioning was discussed in
# Chapter 10 Movement with Servos, Motors, and Steppers
SERVO_PULSE_LEFT_NS = 2500
SERVO_PULSE_RIGHT_NS = 1000

# The number of degrees from center will the servo sweep when the /servo/sweep API end point is called.
SERVO_SWEEP_DEGREES = 20

# The number of sweeps performed when the /servo/sweep API end point is called.
SERVO_SWEEP_COUNT = 3


"""
PAHO MQTT CLIENT CONFIGURATION
"""

# MQTT Broker Host
MQTT_HOST = "localhost"

# MQTT Broker Port
MQTT_PORT = 1883

# Root MQTT Topic to subscribe to. This is where we expect to receive IoTree control messages.
# Make sure it ends in /# (to subscribe to all sub topics in the hierarchy)
MQTT_TOPIC_ROOT = "tree/#"



"""
MQTT TOPIC to PYPUBSUB TOPIC MAPPINGS
"""

# The following are the internal PyPubSub Topic Names
# used in code (they're defined here rather than being hard coded inline)
PUBSUB_TOPIC_CLEAR     = "clear"
PUBSUB_TOPIC_PATTERN   = "pattern"
PUBSUB_TOPIC_PUSH      = "push"
PUBSUB_TOPIC_ANIMATION = "animation"
PUBSUB_TOPIC_SPEED     = "speed"
PUBSUB_TOPIC_CONTRAST  = "contrast"
PUBSUB_TOPIC_SWEEP     = "sweep"


# The following dictionary defines how MQTT Topics are mapped into local PyPubSub Topics.
# There is a 1:1 mapping to the above PYPUBSUB_* configurations.
MQTT_TO_PUBSUB_TOPIC_MAPPINGS = {
    "tree/lights/clear":     PUBSUB_TOPIC_CLEAR,
    "tree/lights/animation": PUBSUB_TOPIC_ANIMATION,
    "tree/lights/push":      PUBSUB_TOPIC_PUSH,
    "tree/lights/pattern":   PUBSUB_TOPIC_PATTERN,
    "tree/lights/speed":     PUBSUB_TOPIC_SPEED,
    "tree/lights/contrast":  PUBSUB_TOPIC_CONTRAST,
    "tree/servo/sweep":      PUBSUB_TOPIC_SWEEP
}

