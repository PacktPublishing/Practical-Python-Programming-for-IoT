"""
File: chapter14/tree_api_service/apa102_api.py

Flask-RESTFul resource implementation for controlling APA102 LED Strip.

Built and tested with Python 3.7 on Raspberry Pi 4 Model B

Dependencies:
  pip3 install flask-restful
"""
import logging
from flask_restful import Resource, Api, reqparse, inputs

# Initialize Logging
logger = logging.getLogger('APA102Resources')  # Logger for this module
logger.setLevel(logging.INFO) # Debugging for this file.


apa102 = None # APA102 HAL Instance

# Mapping dictionary to convert text into APA102 animation constants.
mode_to_text = {}

def set_apa102(apa102_instance):
    """
    Set APA102 HAL Instance.
    """

    global apa102, mode_to_text

    apa102 = apa102_instance

    APA102 = apa102.__class__

    # Mapping dictionary to convert text into APA102 animation constants.
    mode_to_text = {
        APA102.MODE_NOT_ANIMATING: "off",
        APA102.MODE_ROTATE_LEFT: "left",
        APA102.MODE_ROTATE_RIGHT: "right",
        APA102.MODE_BLINK: "blink",
        APA102.MODE_RAINBOW: "rainbow"
    }


class ClearControl(Resource):
    """
    Flask-RESTFul Resource defining APA102 Clear API.
    """

    def __init__(self):
        pass

    def post(self):
        """
        POST request clears APA102 LED Strip
        """

        apa102.clear()

        return {
            "success": True
        }


class StateControl(Resource):
    """
    Flask-RESTFul Resource defining APA102 state API.
    """

    def _get_state(self):
        """
        Helper method to return current APA102 state.
        """

        return {
            "contrast":  apa102.contrast,
            "speed":     apa102.animation_speed,
            "colors" :   list(filter(None, apa102.color_buffer)), # Just colours. Empty color elements not returned.
            "animation": mode_to_text[apa102.mode]
        }

    def get(self):
        """
        GET Request returns current APA102 state.
        """

        return {
            "success": True,
            "state": self._get_state()
        }


class ColorControl(Resource):
    """
    Flask-RESTFul Resource defining APA102 color control API.
    """

    def __init__(self):
        """
        Constructor - Setup allowed arguments.
        """

        self.args_parser = reqparse.RequestParser(trim=True)
        self.args_parser.add_argument(name='colors', type=str, required=True, store_missing=False, help='Comma separated list of colors')
        self.args_parser.add_argument(name='pattern', type=str, required=False, default="n", choices=("y", "n", "yes", "no"), case_sensitive=False, store_missing=True, help='Apply colors as a repeating pattern')

    def _get_state(self):
        """
        Helper method to return current APA102 color buffer.
        """

        return {
            "colors" : list(filter(None, apa102.color_buffer)), # Just colours. Empty color elements not returned.
        }


    def get(self):
        """
        GET Request returns current APA102 color buffer.
        """

        return {
            "success": True,
            "state": self._get_state()
        }


    def post(self):
        """
        POST Request to set/update APA102 color buffer.
        """

        args = self.args_parser.parse_args()

        pattern = args['pattern'][0] == "y"
        colors = args['colors'].split(",")

        if pattern:
            apa102.set_pattern(colors)
        else:
            for color in colors:
                apa102.push_color(color)

        return {
            "success": True,
            "state": self._get_state()
        }



class ContrastControl(Resource):
    """
    Flask-RESTFul Resource defining APA102 contrast control API.
    """

    def __init__(self):
        """
        Constructor - Setup argument parser
        """

        self.args_parser = reqparse.RequestParser(trim=True)
        self.args_parser.add_argument(name='level', type=inputs.int_range(0, 255), required=False)


    def _get_state(self):
        """
        Helper method to return current APA102 contrast level.
        """

        return {
            "contrast":  apa102.contrast
        }


    def get(self):
        """
        GET Request returns current APA102 contrast level.
        """

        return {
            "success": True,
            "state": self._get_state()
        }


    def post(self):
        """
        POST Request to set APA102 contrast level.
        """

        args = self.args_parser.parse_args()

        if 'level' in args and args['level'] is not None:

            level = int(args['level'])

            apa102.set_contrast(level)

            return {
                "success": True,
                "state": self._get_state()
            }


class AnimationControl(Resource):
    """
    Flask-RESTFul Resource defining APA102 LED animation control API.
    """

    def __init__(self):
        """
        Constructor - Setup argument parser
        """

        self.args_parser = reqparse.RequestParser(trim=True)
        self.args_parser.add_argument(name='mode', type=str, required=False, choices=("stop", "blink", "left", "right", "rainbow"), case_sensitive=False, help='Mode')
        self.args_parser.add_argument(name='speed', type=inputs.int_range(1, 10), required=False)


    def _get_state(self):
        """
        Helper method to return current APA102 contrast level.
        """

        return {
            "speed":     apa102.animation_speed,
            "animation": mode_to_text[apa102.mode]
        }


    def get(self):
        """
        GET Request returns current APA102 animation mode.
        """

        return {
            "success": True,
            "state": self._get_state()
        }


    def post(self):
        """
        POST Request sets APA102 animation mode.
        """

        args = self.args_parser.parse_args()

        if 'mode' in args:
            mode = args['mode']
            self._set_mode(mode)

        if 'speed' in args and args['speed'] is not None:
            speed = int(args['speed'])
            apa102.set_animation_speed(speed)

        return {
            "success": True,
            "state": self._get_state()
        }


    def _set_mode(self, mode):
        """
        Helper method to set animation mode.
        """

        if mode == "stop":
            apa102.stop_animation()
        elif mode == "blink":
            apa102.blink()
        elif mode == "left":
            apa102.rotate_left()
        elif mode == "right":
            apa102.rotate_right()
        elif mode == "rainbow":
            apa102.rainbow()
