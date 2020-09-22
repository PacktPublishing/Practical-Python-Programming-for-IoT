"""
File: chapter14/tree_api_service/servo_api.py

Flask-RESTFul resource implementation for controlling servo.

Built and tested with Python 3.7 on Raspberry Pi 4 Model B

Dependencies:
  pip3 install flask-restful
"""

from time import sleep
import logging
from flask_restful import Resource, Api, reqparse, inputs

logger = logging.getLogger('ServoResources')  # Logger for this module
logger.setLevel(logging.INFO) # Debugging for this file.

config = None  # Configuration (that is config.py) reference.
servo = None   # Servo HAL instance.

def set_servo(servo_instance):
    """
    Set Servo HAL Instance.
    """

    global servo
    servo = servo_instance

def set_config(config_instance):
    """
    Set Config Instance.
    """

    global config
    config = config_instance



class SweepControl(Resource):
    """
    Flask-RESTFul Resource defining Servo control API.
    """

    def __init__(self):
        pass

    def post(self):
        """
        Handle POST Request to sweep servo.
        """

        servo.sweep(count=config.SERVO_SWEEP_COUNT, degrees=config.SERVO_SWEEP_DEGREES)
        servo.center()
        sleep(1) # Give servo time to move.
        servo.idle() # Save power by making servo idle.

        return {
            "success": True
        }


