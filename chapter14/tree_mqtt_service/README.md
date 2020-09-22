# IoTree MQTT Service

The following is a list of MQTT topic and message formats recognise by the Tree MQTT Service.

## Clear (turn off) all LEDS on APA102 LED Strip

 * MQTT Topic: `tree/lights/clear`
 * MQTT Message Format: Pass an empty message

*Example:*

`mosquitto_pub -h "localhost" -t "tree/lights/clear" -m ""`

---

## Push color(s) into the APA102 LED Strip

 * MQTT Topic: `tree/lights/push`
 * MQTT Message Format: Space separated list of colour names or hex values

*Example:*

`mosquitto_pub -h "localhost" -t "tree/lights/push" -m "red blue black"`

---

## Set Repeating Color Pattern on the APA102 LED Strip

 * MQTT Topic: `tree/lights/pattern`
 * MQTT Message Format: Space separated list of colour names or hex values

*Example:*

`mosquitto_pub -h "localhost" -t "tree/lights/pattern" -m "red blue black"`

---

## Set LED Contrast

 * MQTT Topic: `tree/lights/contrast`
 * MQTT Message Format: A number between `0` and `255`

*Example:*

`mosquitto_pub -h "localhost" -t "tree/lights/contrast" -m "128"`

---

## Set LED Animation Mode


 * MQTT Topic: `tree/lights/animation`
 * MQTT Message Format: One of the following values:
    * stop
    * left
    * right
    * blink
    * rainbow

*Example:*

`mosquitto_pub -h "localhost" -t "tree/lights/animation" -m "blink"`

---

## Set LED Animation Speed


 * MQTT Topic: `tree/lights/speed`
 * MQTT Message Format: A number between `1` and `10`

*Example:*

`mosquitto_pub -h "localhost" -t "tree/lights/speed" -m "10"`

---

## Sweep the Servo

 * MQTT Topic: `tree/lights/sweep`
 * MQTT Message Format: Pass an empty message`

*Example:*

`mosquitto_pub -h "localhost" -t "tree/servo/sweep" -m ""`
