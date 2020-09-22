"""
File: chapter14/tree_api_service/config.py

Tree API Service configuration.

This program publishes a RESTFul API for controlling the IoTree circuit.

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
EMBEDDED FLASK WEB SERVER CONFIGURATION
"""

# 0.0.0.0 to open server up to local network.
# Hose/IP to bind server. Use 0.0.0.0 to allow access on all network interfaces.
SERVER_HOST = "0.0.0.0"

# Server Port
SERVER_PORT = 5000

# Enable development server debug mode (eg live reload on file changes)
SERVER_DEBUG_MODE = True

