"""
File: chapter14/tree_api_service/main.py

Program entry point.

This program publishes a RESTFul API for controlling the IoTree circuit.

Dependencies:
  pip3 install pigpio flask-restful luma.led_matrix

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""
import logging
from flask import Flask, request, render_template
from flask_restful import Api, reqparse, inputs
import config
from apa102 import APA102
from servo import Servo
import apa102_api, servo_api

logging.basicConfig(level=logging.INFO)


# Flask & Flask-RESTful instance variables
app = Flask(__name__) # Core Flask app.
api = Api(app) # Flask-RESTful extension wrapper

# @app.route applies to the core Flask instance (app).
# Here we are serving a simple web page.
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# APA102 instance and configuration.
apa102 = APA102(num_leds=config.APA102_NUM_LEDS,
                port=config.APA102_PORT,
                device=config.APA102_DEVICE,
                bus_speed_hz=config.APA102_BUS_SPEED_HZ)

# Set default LED contrast.
apa102.set_contrast(config.APA102_DEFAULT_CONTRAST)

# APA102 Flask-RESTFul Resource setup and registration.
apa102_api.set_apa102(apa102)
api.add_resource(apa102_api.StateControl, "/lights")
api.add_resource(apa102_api.ColorControl, "/lights/color")
api.add_resource(apa102_api.ContrastControl, "/lights/contrast")
api.add_resource(apa102_api.ClearControl, "/lights/clear")
api.add_resource(apa102_api.AnimationControl, "/lights/animation")


# Servo instance and configuration.
servo = Servo(
    servo_gpio=config.SERVO_GPIO,
    pulse_left_ns=config.SERVO_PULSE_LEFT_NS,
    pulse_right_ns=config.SERVO_PULSE_RIGHT_NS)


# Servo Flask-RESTFul Resource setup and registration.
servo_api.set_config(config)
servo_api.set_servo(servo)
api.add_resource(servo_api.SweepControl, "/servo/sweep")


if __name__ == '__main__':

    # If you have debug=True and receive the error "OSError: [Errno 8] Exec format error", then:
    # remove the execuition bit on this file from a Terminal, ie:
    # chmod -x flask_api_server.py
    #
    # Flask GitHub Issue: https://github.com/pallets/flask/issues/3189

    app.run(host="0.0.0.0", debug=True)

