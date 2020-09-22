"""
File: chapter14/dweet_integration_service/config.py

Dweet Integration Service configuration.

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""

"""
DWEET CONFIGURATION
"""

# Receive dweets using a polling method (USE_POLLING = True), or
# use a HTTP streaming method (USE_POLLING = False)
USE_POLLING = True  # False to stream dweets.

# The polling schedule in seconds when using USE_POLLING = True
POLL_SECS = 2

# Dweet.io service base URL.
DWEET_IO_URL = "https://dweet.io"

# Dweet.io thing name.
# Leave as None to generate a name (and save it to thing_name.txt)
THING_NAME = None



"""
PAHO MQTT CLIENT CONFIGURATION
"""

# MQTT Broker Host
MQTT_HOST = "localhost"

# MQTT Broker Port
MQTT_PORT = 1883


"""
DWEETED COMMAND TO MQTT TOPIC MAPPINGS
"""

# The following dictionary describes how a dweeted command actions map into MQTT Topics.
# For example, if a dweeted command includes the "push" action, this will be republished
# as an MQTT message to the topic "tree/lights/push"
ACTION_TOPIC_MAPPINGS = {
    "clear": "tree/lights/clear",
    "push": "tree/lights/push",
    "pattern": "tree/lights/pattern",
    "contrast": "tree/lights/contrast",
    "animation": "tree/lights/animation",
    "speed": "tree/lights/speed",
    "sweep": "tree/servo/sweep",
    "jingle": "tree/servo/sweep", # Alias for "sweep".
}


"""
MQTT MESSAGE RETENTION CONFIGURATION
"""

# The following dictionary determines which MQTT topics will have their messages
# published with the "retain" message flat set.
TOPIC_RETAIN_MESSAGE = {
    "tree/lights/clear": False,
    "tree/lights/animation": True,
    "tree/lights/push": True,
    "tree/lights/pattern": True,
    "tree/lights/speed": True,
    "tree/lights/contrast": True,
    "tree/servo/angle": False,
    "tree/servo/sweep": False
}

