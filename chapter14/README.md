# Practical Python Programming for IoT

## Chapter 14 - Tying it Altogether - An IoT Christmas Tree

* `requirements.txt` - Python dependencies required for this chapter

* `tree_api_service`
  * `README.md` - IoTree API Documentation and Examples
  * `main.py` - Main program
  * `config.py` - Program Configuration
  * `apa102.py` - APA102 LED Strip Electronic Interface 
  * `apa102_api.py` - Flask-RESTful Resource Definitions for APA102 API.
  * `servo.py` - Servo Electronic Interface
  * `servo_api.py` - Flask-RESTful Resource Definitions for Servo API.
  * `templates/index.html` - Web App to control IoTree
  * `static/jquery.min.js` - JQuery JavaScript library for Web App
  * `static/images/color-bar.png` - Image used in Web App
  
* `tree_mqtt_service`
  * `README.md` - IoTree MQTT Topic and Message Format Documentation and Examples
  * `main.py` - Main program
  * `config.py` - Program Configuration
  * `apa102.py` - APA102 LED Strip Electronic Interface 
  * `apa102_controller.py` - Interprets PubSub messages to control APA102 LED Strip 
  * `servo.py` - Servo Electronic Interface
  * `servo_controller.py` - Interprets PubSub messages to control Servo
  * `mqtt_listener.py` - MQTT Client. Subscribes to MQTT Topic and republishes MQTT messages as PubSub messages
  
* `dweet_integration_service`
  * `README.md` - IoTree Dweet Documentation and Examples
  * `main.py` - Main program
  * `config.py` - Program Configuration
  * `dweet_listener.py` - Core Program that listens for Dweets and republished them as MQTT topic/message combinations. 
  